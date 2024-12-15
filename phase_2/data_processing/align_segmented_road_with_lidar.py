import argparse
import os
import time
import pandas as pd
import numpy as np
from scipy.spatial.transform import Rotation
from scipy.optimize import minimize
from math import radians, tan
from raycasting import find_occluded_points
from utils import get_camera_latlon_and_bearing_for_image_from_mapping, bearing_between_two_latlon_points, \
    get_aerial_lidar_road_geo_df, create_gdf_from_df, add_lidar_x_y_from_lat_lon, \
    classify_points_base_on_centerline, ROADSIDE, create_df_from_lidar_points, LIDARClass

from extract_lidar_3d_points import get_lidar_data_from_shp, extract_lidar_3d_points_for_camera
from get_road_boundary_points import get_image_lane_points, get_image_road_points, combine_lane_and_road_boundary

BASE_CAM_PARA_COL_NAME = 'BASE_CAMERA_OBJ_PARA'
OPTIMIZED_CAM_PARA_COL_NAME = 'OPTIMIZED_CAMERA_OBJ_PARA'

# indices as constants in the input object camera parameter list where OBJ_LIDAR_X/Y/Z_OFFSET indicate object
# translation along X/Y/Z axis in world coordinate system, OBJ_ROT_Z, OBJ_ROT_Y, OBJ_ROT_X
# indicate angle of rotation of the object around Z (bearing) axis, Y axis, and X axis, respectively, in the 3D world
# coordinate system. Object translations and rotations are negated as opposed to the corresponding camera translations
# and rotations
PERSPECTIVE_NEAR, PERSPECTIVE_VFOV, OBJ_LIDAR_X_OFFSET, OBJ_LIDAR_Y_OFFSET, OBJ_LIDAR_Z_OFFSET, \
    OBJ_ROT_Z, OBJ_ROT_Y, OBJ_ROT_X = 0, 1, 2, 3, 4, 5, 6, 7

CAM_NEAR = 0.1
# camera pose parameter bound constraints put on optimizer
FOV_OFFSET = 2

X_ROT_MAX = 2.15
Y_ROT_MAX = 2
Z_ROT_MAX = 1

INIT_CAM_OBJ_PARAS = None
PREV_CAM_OBJ_PARAS = None
PREV_CAM_BEARING_VEC = np.empty(3)
NUM_ITERATIONS = 1000  # optimizer hyperparameters

LIDAR_DIST_THRESHOLD = (11.5, 689)  # in feet
CAMERA_ALIGNMENT_RESET_REASONS = ['Too few LIDAR points', 'alignment error threshold exceeded']

def rotate_point(point, quaternion):
    rotated_point = quaternion.apply(point)
    return rotated_point


def init_transform_from_lidar_to_world_coordinate_system(df, cam_x, cam_y, cam_z):
    # transform LIDAR points from LIDAR projection coordinate system to world coordinate system without
    # considering camera pose parameters
    if 'CAM_DIST' not in df.columns:
        # Calculate the distance between the cam_x, cam_y point and the first two X, Y columns of input_3d_points
        df['CAM_DIST'] = np.sqrt(np.square(df.X - cam_x) + np.square(df.Y - cam_y))
    df['INITIAL_WORLD_Z'] = -df.CAM_DIST * np.cos(df.BEARING)
    df['INITIAL_WORLD_Y'] = df.Z - cam_z
    df['INITIAL_WORLD_X'] = df.CAM_DIST * np.sin(df.BEARING)
    return df


def transform_to_world_coordinate_system(df, cam_params):
    # transform X, Y, Z in LIDAR coordinate system to world coordinate system where the camera is at the origin,
    # the z-axis is pointing from the camera along the cam_bearing direction, the y-axis is perpendicular to the
    # z-axis reflecting the elevation Z pointing upwards, and the x-axis is perpendicular to both y-axis and z-axis.
    # Note that LIDAR world coordinate system origin is located at lower-left corner while
    # screen coordinate system origin is located at upper-left corner
    rotation_x = Rotation.from_euler('x', radians(cam_params[OBJ_ROT_X]))
    rotation_y = Rotation.from_euler('y', radians(cam_params[OBJ_ROT_Y]))
    rotation_z = Rotation.from_euler('z', radians(cam_params[OBJ_ROT_Z]))
    combined_rotation = rotation_z * rotation_y * rotation_x

    points = df[['INITIAL_WORLD_X', 'INITIAL_WORLD_Y', 'INITIAL_WORLD_Z']].to_numpy()
    rotated_point = np.apply_along_axis(rotate_point, axis=1, arr=points, quaternion=combined_rotation)
    rp_df = pd.DataFrame(rotated_point, columns=['WORLD_X', 'WORLD_Y', 'WORLD_Z'])
    df['WORLD_X'], df['WORLD_Y'], df['WORLD_Z'] = rp_df['WORLD_X'], rp_df['WORLD_Y'], rp_df['WORLD_Z']

    df['WORLD_Z'] = df['WORLD_Z'] + cam_params[OBJ_LIDAR_Z_OFFSET]
    df['WORLD_Y'] = df['WORLD_Y'] + cam_params[OBJ_LIDAR_Y_OFFSET]
    df['WORLD_X'] = df['WORLD_X'] + cam_params[OBJ_LIDAR_X_OFFSET]
    return df


def apply_matrix4(x, y, z, e, return_axis='x'):
    w = 1 / (e[3] * x + e[7] * y + e[11] * z + e[15])
    new_x = (e[0] * x + e[4] * y + e[8] * z + e[12] ) * w
    new_y = (e[1] * x + e[5] * y + e[9] * z + e[13] ) * w
    new_z = (e[2] * x + e[6] * y + e[10] * z + e[14] ) * w
    if return_axis == 'x':
        return new_x
    elif return_axis == 'y':
        return new_y
    else:
        return new_x, new_y, new_z


def meet_camera_parameter_constraint(cam_params):
    if cam_params[PERSPECTIVE_NEAR] < 0.005:
        return False
    return True


def transform_3d_points(df, cam_params, img_width, img_hgt):
    if not meet_camera_parameter_constraint(cam_params):
        return df

    df = transform_to_world_coordinate_system(df, cam_params)

    aspect = img_width / img_hgt
    far = df['INITIAL_WORLD_Z'].abs().max() * 1.5

    top = cam_params[PERSPECTIVE_NEAR] * tan(radians(0.5 * cam_params[PERSPECTIVE_VFOV]))
    height = 2 * top
    width = aspect * height
    left = -0.5 * width
    right = left + width
    bottom = top - height

    # precompute matrix elements
    x = 2 * cam_params[PERSPECTIVE_NEAR] / (right - left)
    y = 2 * cam_params[PERSPECTIVE_NEAR] / (top - bottom)
    a = (right + left) / (right - left)
    b = (top + bottom) / (top - bottom)
    c = - (far + cam_params[PERSPECTIVE_NEAR]) / (far - cam_params[PERSPECTIVE_NEAR])
    d = (- 2 * far * cam_params[PERSPECTIVE_NEAR]) / (far - cam_params[PERSPECTIVE_NEAR])

    # construct projection matrix
    matrix = np.array([
        [x, 0, a, 0],
        [0, y, b, 0],
        [0, 0, c, d],
        [0, 0, -1, 1]
    ])

    # Convert DataFrame to numpy array for vectorized operations
    world_points = df[['WORLD_X', 'WORLD_Y', 'WORLD_Z']].values
    ones = np.ones((len(world_points), 1))
    points_4d = np.hstack((world_points, ones))

    # apply projection matrix to project to 2D camera coordinate system
    projected_points = points_4d @ matrix.T

    # handle invalid points before normalization
    with np.errstate(invalid='ignore', divide='ignore'):
        projected_points /= projected_points[:, 3].reshape(-1, 1)

    # replace NaNs with a large off-screen value
    projected_points[np.isnan(projected_points)] = -99999

    # Map to screen coordinates
    half_width = img_width / 2
    half_height = img_hgt / 2

    df['PROJ_SCREEN_X'] = (projected_points[:, 0] * half_width + half_width).astype(int)
    df['PROJ_SCREEN_Y'] = (-projected_points[:, 1] * half_height + half_height).astype(int)
    return df


class SkipOptimizationException(Exception):
    """
    Custom exception to indicate that the optimization initial condition should be reset.
    """
    def __init__(self, exception_reason, exception_value):
        # Initialize with custom reason and value
        self.exception_reason = exception_reason
        self.exception_value = exception_value
        # Call the base class constructor with the message
        super().__init__(f"{exception_reason}: {exception_value}")

    def __str__(self):
        # Custom string representation for this exception
        return f"SkipOptimizationException({self.exception_reason}: {self.exception_value})"

    pass


def _filter_dataframe_within_screen_bounds(df, screen_width, screen_height):
    return df[
        (df['PROJ_SCREEN_X'] >= 0) &
        (df['PROJ_SCREEN_X'] <= screen_width) &
        (df['PROJ_SCREEN_Y'] >= 0) &
        (df['PROJ_SCREEN_Y'] <= screen_height)
    ]


def objective_function_2d(cam_params, df_3d, df_2d, img_wd, img_ht, align_errors):
    # compute alignment error corresponding to the cam_params using the sum of squared distances between projected
    # LIDAR vertices and the road boundary pixels
    full_cam_params = get_full_camera_parameters(cam_params)
    df_3d = transform_3d_points(df_3d, full_cam_params, img_wd, img_ht)

    # get transformed dataframe within projected screen bounds
    filtered_df_3d = _filter_dataframe_within_screen_bounds(df_3d, img_wd, img_ht)

    if len(filtered_df_3d) < len(df_3d) / 20:
        # most points are projected out of the bound, need to reset initial condition
        raise SkipOptimizationException(CAMERA_ALIGNMENT_RESET_REASONS[0], len(filtered_df_3d))

    # split df_2d and df_3d based on SIDE
    df_2d_l = df_2d[df_2d['SIDE'] == ROADSIDE.LEFT.value]
    df_2d_r = df_2d[df_2d['SIDE'] == ROADSIDE.RIGHT.value]
    df_3d_l = df_3d[df_3d['SIDE'] == ROADSIDE.LEFT.value]
    df_3d_r = df_3d[df_3d['SIDE'] == ROADSIDE.RIGHT.value]

    def compute_grid_minimum_distances(x_3d, y_3d, x_2d, y_2d, grid_th=300):
        """
        Function to compute minimum distances between each point in (x_3d, y_3d) and (x_2d, y_2d)
        leveraging numpy broadcasting and vectorization
        """
        # Compute the absolute differences in x and y directions
        diff_x = np.abs(x_3d[:, np.newaxis] - x_2d[np.newaxis, :])  # Shape: (n_3d, n_2d)
        diff_y = np.abs(y_3d[:, np.newaxis] - y_2d[np.newaxis, :])  # Shape: (n_3d, n_2d)

        # Apply the grid threshold filter: Only keep points within grid_th in both x and y directions
        within_grid_mask = (diff_x < grid_th) & (diff_y < grid_th)

        # Initialize fallback distances with max distances in x and y direction (in case no valid match is found)
        max_grid_x = np.max(diff_x, axis=1)
        max_grid_y = np.max(diff_y, axis=1)

        # For points outside the grid, set the distances to a large value to exclude them from being chosen
        dist_squared = np.where(within_grid_mask, diff_x ** 2 + diff_y ** 2, np.inf)
        min_distances = np.min(dist_squared, axis=1)
        # Handle cases where no point is found within the grid (where all distances are inf) - this is very
        # important to set these values with the maximum grid distance instead of larger value of inf to avoid
        # harsh penalty of infinite distance for more stable optimization results
        no_match_mask = np.isinf(min_distances)
        min_distances[no_match_mask] = np.maximum(max_grid_x[no_match_mask], max_grid_y[no_match_mask])
        # Find the minimum distance for each 3D point in the filtered data
        return min_distances

    # compute grid-based distances for both left and right sides
    x_3d_l = df_3d_l['PROJ_SCREEN_X'].values
    y_3d_l = df_3d_l['PROJ_SCREEN_Y'].values
    x_3d_r = df_3d_r['PROJ_SCREEN_X'].values
    y_3d_r = df_3d_r['PROJ_SCREEN_Y'].values
    dists_l = compute_grid_minimum_distances(x_3d_l, y_3d_l, df_2d_l['X'].values, df_2d_l['Y'].values)
    dists_r = compute_grid_minimum_distances(x_3d_r, y_3d_r, df_2d_r['X'].values, df_2d_r['Y'].values)

    # Combine results back into a single array
    df_3d.loc[df_3d['SIDE'] == ROADSIDE.LEFT.value, 'MATCH_2D_DIST'] = dists_l
    df_3d.loc[df_3d['SIDE'] == ROADSIDE.RIGHT.value, 'MATCH_2D_DIST'] = dists_r

    alignment_error = df_3d['MATCH_2D_DIST'].sum() / len(df_3d)
    align_errors.append(alignment_error)
    return alignment_error


def transform_2d_points_to_3d(df, fl_x, fl_y, img_width, img_hgt, x_header='X', y_header='Y', z_header='Z'):
    cx = img_width // 2
    cy = img_hgt // 2
    # project to 2D camera coordinate system
    df['X_3D'] = df.apply(
        lambda row:  (row[x_header] - cx) * row[z_header] / (cx * fl_x),
        axis=1)
    df['Y_3D'] = df.apply(
        lambda row: (row[y_header] - cy) * row[z_header] / (cy * fl_y),
        axis=1)

    return df


def get_mapping_data(df, input_image_name):
    cam_lat, cam_lon, cam_br, cam_lat2, cam_lon2, base_img2, eor = get_camera_latlon_and_bearing_for_image_from_mapping(
        df, input_image_name, is_degree=False)
    if cam_lat is None:
        # no camera location
        print(f'no camera location found for {input_image_name}')
        exit(1)
    # LIDAR road vertices in input_3d is in NAD83(2011) / North Carolina (ftUS) CRS with EPSG:6543, and
    # the cam_lat/cam_lon is in WGS84 CRS with EPSG:4326, need to transform cam_lat/cam_lon to the same CRS as
    # input_3d
    cam_geom_df = add_lidar_x_y_from_lat_lon(df[df['MAPPED_IMAGE'] == input_image_name])
    proj_cam_x = cam_geom_df.iloc[0].x
    proj_cam_y = cam_geom_df.iloc[0].y
    print(f'cam lat-long: {cam_lat}-{cam_lon}, proj cam y-x: {proj_cam_y}-{proj_cam_x}, cam_br: {cam_br}')
    return cam_lat, cam_lon, proj_cam_x, proj_cam_y, cam_br, cam_lat2, cam_lon2, eor


def get_input_file_with_images(input_file):
    # load input file to get the image names for alignment
    df = pd.read_csv(input_file)
    df['imageBaseName'] = df['imageBaseName'].astype(str)
    print(f'input df shape: {df.shape}')
    df.drop_duplicates(subset=['imageBaseName'], inplace=True)
    print(f'input df shape after removing duplicates: {df.shape}')
    return df


def get_full_camera_parameters(cam_p):
    if len(cam_p) < len(INIT_CAM_OBJ_PARAS):
        combined = INIT_CAM_OBJ_PARAS[:len(INIT_CAM_OBJ_PARAS)-len(cam_p)]
        combined.extend(cam_p)
    else:
        combined = cam_p
    return combined


def derive_next_camera_params(v1, v2, cam_para1):
    rot_mat1 = Rotation.from_euler('xyz', np.array([cam_para1[OBJ_ROT_X], cam_para1[OBJ_ROT_Y],
                                                    cam_para1[OBJ_ROT_Z]]), degrees=True).as_matrix()

    v1_norm = v1 / np.linalg.norm(v1)
    v2_norm = v2 / np.linalg.norm(v2)
    # compute the rotation axis
    rot_axis = np.cross(v1_norm, v2_norm)

    # compute the cosine of the rotation angle
    cos_theta = np.dot(v1_norm, v2_norm)
    rot_mat12 = np.eye(3) + np.sin(np.arccos(cos_theta)) * np.array([[0, -rot_axis[2], rot_axis[1]],
                                                                     [rot_axis[2], 0, -rot_axis[0]],
                                                                     [-rot_axis[1], rot_axis[0], 0]])
    rot_mat2 = np.matmul(rot_mat1, rot_mat12)

    cam_para2 = cam_para1.copy()
    cam_para2[OBJ_ROT_X], cam_para2[OBJ_ROT_Y], cam_para2[OBJ_ROT_Z] = \
        Rotation.from_matrix(rot_mat2).as_euler('xyz', degrees=True)

    return cam_para2


def align_image_to_lidar(row, seg_image_dir, seg_lane_dir, ldf, out_proj_file_path, do_fov_optimize):
    """
    :param row: the image metadata dataframe row to be processed
    :param seg_image_dir: path in which segmentation images are located
    :param seg_lane_dir: path in which road lanes segmentation images are located
    :param ldf: lidar 3D point geodataframe
    :param out_proj_file_path: output path for aligned road info which will be appended with
    lidar_project_info_{image name} to have lidar projection info for each input image
    :param do_fov_optimize: whether to do FOV in the optimizer
    :return: the computed base camera parameters and optimized camera parameters
    """
    global INIT_CAM_OBJ_PARAS, PREV_CAM_OBJ_PARAS, PREV_CAM_BEARING_VEC, \
        X_TRAN_MIN, X_TRAN_MAX, Y_TRAN_MIN, Y_TRAN_MAX, Z_TRAN_MIN, Z_TRAN_MAX

    if len(row["imageBaseName"]) == 11:
        image_name_with_path = os.path.join(seg_image_dir, f'{row["imageBaseName"]}1.png')
        # get input image base name
        input_2d_mapped_image = row["imageBaseName"]
    else:
        image_name_with_path = os.path.join(seg_image_dir, f'{row["imageBaseName"]}.png')
        # get input image base name
        input_2d_mapped_image = row["imageBaseName"][:-1]

    if INIT_CAM_OBJ_PARAS is None and not row['OBJ_BASE_TRANS_LIST']:
        print(f'Initial camera parameters for image {input_2d_mapped_image} must be specified to perform camera '
              f'parameter optimization on the route. Exiting')
        exit(1)

    if row['OBJ_BASE_TRANS_LIST']:
        INIT_CAM_OBJ_PARAS = row['OBJ_BASE_TRANS_LIST']
        PREV_CAM_OBJ_PARAS = None
        PREV_CAM_BEARING_VEC = np.empty(3)
        do_optimize = False # does not do optimization for the first image obtained from manual registration
    else:
        do_optimize = True


    out_proj_file = os.path.join(out_proj_file_path, f'lidar_project_info_{input_2d_mapped_image}.csv')
    print(f'image_name_with_path: {image_name_with_path}, input_2d_mapped_image: {input_2d_mapped_image}')
    lane_image_name = os.path.join(seg_lane_dir, f'{input_2d_mapped_image}1_lanes.png')
    print(f'lane_image_name: {lane_image_name}')
    img_width, img_height, lane_image, input_list, m_points = get_image_lane_points(lane_image_name)
    input_2d_points = input_list[0]

    # compute base camera parameters
    cam_lat = float(row['LATITUDE'])
    cam_lon = float(row['LONGITUDE'])

    if pd.notna(row['LATITUDE_next']) and pd.notna(row['LONGITUDE_next']):
        cam_lat2 = float(row['LATITUDE_next'])
        cam_lon2 = float(row['LONGITUDE_next'])
    else:
        # end of the route, skip alignment and return
        return PREV_CAM_OBJ_PARAS, PREV_CAM_OBJ_PARAS

    # compute bearing
    cam_br = bearing_between_two_latlon_points(cam_lat, cam_lon, cam_lat2, cam_lon2, is_degree=False)

    # LIDAR road vertices in input_3d is in NAD83(2011) / North Carolina (ftUS) CRS with EPSG:6543, and
    # the cam_lat/cam_lon is in WGS84 CRS with EPSG:4326, need to transform cam_lat/cam_lon to the same CRS as
    # input_3d
    cam_geom_df = add_lidar_x_y_from_lat_lon(pd.DataFrame(data={'LONGITUDE': [cam_lon], 'LATITUDE': [cam_lat]}))
    proj_cam_x = cam_geom_df.iloc[0].x
    proj_cam_y = cam_geom_df.iloc[0].y

    cam_lidar_z = row['CAM_Z']

    # filter out LIDAR points approximately by distance for performance improvement
    ldf = ldf[((ldf.X - proj_cam_x).abs() < LIDAR_DIST_THRESHOLD[1]) &
              ((ldf.Y - proj_cam_y).abs() < LIDAR_DIST_THRESHOLD[1])]

    t1 = time.time()
    vertices, cam_br, cols = extract_lidar_3d_points_for_camera(ldf, [cam_lat, cam_lon], [cam_lat2, cam_lon2],
                                                                dist_th=LIDAR_DIST_THRESHOLD,
                                                                end_of_route=False,
                                                                fov=90,
                                                                proj_cam_x=proj_cam_x,
                                                                proj_cam_y=proj_cam_y)
    input_3d_points = vertices[0]
    print(f'len(input_3d_points): {len(input_3d_points)}, cols: {cols}')
    print(f'time taken for extracting lidar points for camera: {time.time() - t1}s')
    input_3d_df = create_df_from_lidar_points(input_3d_points, cols)
    input_3d_gdf = create_gdf_from_df(input_3d_df)
    # calculate the bearing of each 3D point to the camera
    input_3d_gdf['BEARING'] = input_3d_gdf['geometry_y'].apply(lambda geom: bearing_between_two_latlon_points(
        cam_lat, cam_lon, geom.y, geom.x, is_degree=False) - cam_br)

    input_3d_gdf = init_transform_from_lidar_to_world_coordinate_system(input_3d_gdf, proj_cam_x, proj_cam_y,
                                                                        cam_lidar_z)

    cam_df = pd.DataFrame(data={'LATITUDE': [cam_lat2], 'LONGITUDE': [cam_lon2]})
    cam_gdf = add_lidar_x_y_from_lat_lon(cam_df)
    proj_cam_x2 = cam_gdf.iloc[0].x
    proj_cam_y2 = cam_gdf.iloc[0].y
    proj_cam_z2 = row['CAM_Z_next'] if pd.notna(row['CAM_Z_next']) else row['CAM_Z']
    print(f'proj_cam_z2: {proj_cam_z2}')
    cam_v = np.array([proj_cam_x2 - proj_cam_x, proj_cam_y2 - proj_cam_y, proj_cam_z2 - cam_lidar_z])
    cam_v = cam_v / np.linalg.norm(cam_v)

    if PREV_CAM_OBJ_PARAS is not None:
        prev_v = PREV_CAM_BEARING_VEC
        v = cam_v
        init_cam_paras = derive_next_camera_params(prev_v, v, PREV_CAM_OBJ_PARAS)
        print(f'derived camera parameters: {init_cam_paras}')
    else:
        init_cam_paras = INIT_CAM_OBJ_PARAS

    # update global variables to prepare for the next image row iteration
    PREV_CAM_OBJ_PARAS = init_cam_paras
    PREV_CAM_BEARING_VEC = cam_v

    # output base lidar project info to base_lidar_project_info_{image_base_name}.csv file since the base
    # camera orientation/bearing info is updated from the optimized version of its previous image using
    # road tangent info. The optimization is based on updated camera base parameters
    input_3d_gdf = transform_3d_points(input_3d_gdf, init_cam_paras, img_width, img_height)

    seg_image_name = os.path.join(seg_image_dir, f'{input_2d_mapped_image}1.png')
    img_width, img_height, input_road_img, input_list = get_image_road_points(seg_image_name)
    input_2d_points = combine_lane_and_road_boundary(input_2d_points, lane_image, input_road_img,
                                                     seg_image_name, image_height=img_height)

    if do_optimize:
        output_lidar_proj_filename = f'base_lidar_project_info_{row["imageBaseName"]}.csv'
    else:
        output_lidar_proj_filename = f'lidar_project_info_{row["imageBaseName"]}.csv'
    input_3d_gdf.to_csv(os.path.join(out_proj_file_path, output_lidar_proj_filename),
                        index=False)

    if m_points is None:
        # no middle lane axis and centroid can be computed from segmented road lanes, which indicates a
        # complicated road scene such as 4-way intersection, need to skip this image and return without optimization
        if input_2d_points.shape[1] == 2:
            input_2d_df = pd.DataFrame({
                'X': input_2d_points[:, 0],
                'Y': input_2d_points[:, 1]
            })
            input_2d_df.to_csv(os.path.join(out_proj_file_path, f'input_2d_{input_2d_mapped_image}.csv'), index=False)
        return PREV_CAM_OBJ_PARAS, PREV_CAM_OBJ_PARAS

    # use combined lane and road boundary for better matching with LIDAR road edges
    # insert the top point in filtered_contour to m_points to account of the far end
    # curved segment that is not part of the segmented lane but part of the road segmentation boundary
    min_y_index = np.argmin(input_2d_points[:, 1])
    if m_points[0, 1] - input_2d_points[min_y_index, 1] > 10:
        m_points = np.vstack((input_2d_points[min_y_index, :], m_points))

    if input_2d_points.shape[1] == 2:
        # classify each point as left or right side
        m_points_df = pd.DataFrame({'x': m_points[:, 0], 'y': m_points[:, 1]})
        try:
            input_2d_sides = classify_points_base_on_centerline(input_2d_points, m_points_df)
        except Exception as ex:
            print(f'segmentation points cannot be classified into sides due to exception: {ex}, '
                  f'skip this image {row["imageBaseName"]}')
            input_2d_df = pd.DataFrame({
                'X': input_2d_points[:, 0],
                'Y': input_2d_points[:, 1]
            })
            input_2d_df.to_csv(os.path.join(out_proj_file_path, f'input_2d_{input_2d_mapped_image}.csv'), index=False)
            return PREV_CAM_OBJ_PARAS, PREV_CAM_OBJ_PARAS

        input_2d_df = pd.DataFrame({
            'X': input_2d_points[:, 0],
            'Y': input_2d_points[:, 1],
            'SIDE': input_2d_sides
        })
        input_2d_df.to_csv(os.path.join(out_proj_file_path, f'input_2d_{input_2d_mapped_image}.csv'), index=False)
    else:
        print(f'input_2d_points.shape[1] must be 2, but it is {input_2d_points.shape[1]}, skip this image '
              f'and return without optimization')
        return PREV_CAM_OBJ_PARAS, PREV_CAM_OBJ_PARAS

    if not do_optimize:
        return PREV_CAM_OBJ_PARAS, PREV_CAM_OBJ_PARAS

    input_3d_gdf = find_occluded_points(input_3d_gdf, np.array([proj_cam_x, proj_cam_y, cam_lidar_z]),
                                                   img_width, img_height, ground_only=True, lowest_hit=False)
    input_3d_road_bound_gdf = input_3d_gdf[(input_3d_gdf.OCCLUDED == False) &
                                           (input_3d_gdf.BOUND == 1)].reset_index(drop=True).copy()
    if 'SIDE' in cols:
        input_3d_road_bound_gdf['SIDE'] = input_3d_road_bound_gdf['SIDE'].astype(int)
    print(f'after occlusion filtering, input_3d_road_bound_gdf.shape: {input_3d_road_bound_gdf.shape}')
    input_3d_road_bound_gdf.to_csv(os.path.join(out_proj_file_path,
                                                f'base_lidar_project_info_{row["imageBaseName"]}_non_occluded.csv'),
                                   index=False)
    if do_fov_optimize:
        start_idx = 1
        cam_para_bounds = [((PREV_CAM_OBJ_PARAS[PERSPECTIVE_VFOV] - FOV_OFFSET),
                            (PREV_CAM_OBJ_PARAS[PERSPECTIVE_VFOV] + FOV_OFFSET)),
                           (INIT_CAM_OBJ_PARAS[OBJ_LIDAR_X_OFFSET] - 1, INIT_CAM_OBJ_PARAS[OBJ_LIDAR_X_OFFSET] + 1),
                           (INIT_CAM_OBJ_PARAS[OBJ_LIDAR_Y_OFFSET] - 1, INIT_CAM_OBJ_PARAS[OBJ_LIDAR_Y_OFFSET] + 1),
                           (INIT_CAM_OBJ_PARAS[OBJ_LIDAR_Z_OFFSET] - 1, INIT_CAM_OBJ_PARAS[OBJ_LIDAR_Z_OFFSET] + 1),
                           (-Z_ROT_MAX, Z_ROT_MAX),
                           (-Y_ROT_MAX, Y_ROT_MAX),
                           (-X_ROT_MAX, X_ROT_MAX)]
        cam_output_columns = ['fov', 'translation_x', 'translation_y', 'translation_z',
                              'rotation_z', 'rotation_y', 'rotation_x']
    else:
        start_idx = 2
        cam_para_bounds = [(INIT_CAM_OBJ_PARAS[OBJ_LIDAR_X_OFFSET] - 1, INIT_CAM_OBJ_PARAS[OBJ_LIDAR_X_OFFSET] + 1),
                           (INIT_CAM_OBJ_PARAS[OBJ_LIDAR_Y_OFFSET] - 1, INIT_CAM_OBJ_PARAS[OBJ_LIDAR_Y_OFFSET] + 1),
                           (INIT_CAM_OBJ_PARAS[OBJ_LIDAR_Z_OFFSET] - 5, INIT_CAM_OBJ_PARAS[OBJ_LIDAR_Z_OFFSET] + 5),
                           (-Z_ROT_MAX, Z_ROT_MAX),
                           (-Y_ROT_MAX, Y_ROT_MAX),
                           (-X_ROT_MAX, X_ROT_MAX)]
        cam_output_columns = ['translation_x', 'translation_y', 'translation_z',
                              'rotation_z', 'rotation_y', 'rotation_x']

    align_errors = []
    t1 = time.time()
    try:
        result = minimize(objective_function_2d, init_cam_paras[start_idx:],
                          args=(input_3d_road_bound_gdf,
                                input_2d_df, img_width, img_height, align_errors),
                          method='Nelder-Mead',
                          # bounds in the order of OBJ_LIDAR_X_OFFSET, OBJ_LIDAR_Y_OFFSET, OBJ_LIDAR_Z_OFFSET, \
                          # OBJ_ROT_Z, OBJ_ROT_Y, OBJ_ROT_X
                          bounds=cam_para_bounds,
                          options={'maxiter': NUM_ITERATIONS, 'disp': True})
    except SkipOptimizationException as ex:
        print(ex)
        if ex.exception_reason == CAMERA_ALIGNMENT_RESET_REASONS[0]:
            # reset to initial condition does not work for this image
            print(f'Too few LIDAR points ({ex.exception_value}) remain for alignment, skip this image')
        return PREV_CAM_OBJ_PARAS, PREV_CAM_OBJ_PARAS

    optimized_cam_params = result.x
    print(f'optimizing result for image {input_2d_mapped_image}: {result}')
    print(f'Status: {result.message}, total evaluations: {result.nfev}')
    print(f'alignment errors: {align_errors}')
    print(f'optimized_cam_params for image {image_name_with_path}: {optimized_cam_params}, '
          f'time spend: {time.time() - t1}')

    full_optimized_cam_paras = get_full_camera_parameters(optimized_cam_params)
    input_3d_gdf = transform_3d_points(input_3d_gdf, full_optimized_cam_paras,
                                       img_width, img_height)
    # update PREV_CAM_OBJ_PARAS to be used in the next image row iteration
    PREV_CAM_OBJ_PARAS = full_optimized_cam_paras

    input_3d_gdf.to_csv(out_proj_file, index=False)
    proj_base, proj_ext = os.path.splitext(out_proj_file)
    # output optimized camera parameter for the image

    cam_para_df = pd.DataFrame(data=[optimized_cam_params.tolist()], columns=cam_output_columns)
    cam_para_df.to_csv(f'{proj_base}_cam_paras.csv', index=False)

    return init_cam_paras, optimized_cam_params


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Process arguments.')
    parser.add_argument('--input_lidar_with_path', type=str,
                        default='data/d13_route_40001001012/'
                                'route_40001001012_voxel_raster_1ft_with_edges_normalized_sr_sides.csv',
                        help='input file that contains road x, y, z vertices from lidar')
    parser.add_argument('--image_seg_dir', type=str,
                        default='data/d13_route_40001001012/segmentation',
                        help='directory to retrieve segmentation images')
    parser.add_argument('--lane_seg_dir', type=str,
                        default='data/d13_route_40001001012/segmentation',
                        help='directory to retrieve segmented road lane images')
    parser.add_argument('--obj_image_input', type=str,
                        default='data/d13_route_40001001012/route_input.csv',
                        help='input csv file that contains image base names with objects detected along with other '
                             'inputs for mapping')
    parser.add_argument('--input_init_cam_param_file_with_path', type=str,
                        default='data/d13_route_40001001012/initial_camera_params.csv',
                        help='input csv file that includes mapped image lat/lon info')
    parser.add_argument('--lidar_proj_output_file_path', type=str,
                        default='data/d13_route_40001001012/test',
                        help='output file base with path for aligned road info which will be appended with image name '
                             'to have lidar projection info for each input image')
    parser.add_argument('--optimize_fov', action="store_true",
                        help='optimize FOV in the camera parameter optimizer if set to True')

    args = parser.parse_args()
    input_lidar = args.input_lidar_with_path
    image_seg_dir = args.image_seg_dir
    lane_seg_dir = args.lane_seg_dir
    obj_image_input = args.obj_image_input
    input_init_cam_param_file_with_path = args.input_init_cam_param_file_with_path
    lidar_proj_output_file_path = args.lidar_proj_output_file_path
    optimize_fov = args.optimize_fov

    if input_lidar.endswith('.shp'):
        lidar_df = get_lidar_data_from_shp(input_lidar)
    else:
        lidar_df = get_aerial_lidar_road_geo_df(input_lidar)

    input_df = get_input_file_with_images(obj_image_input)
    init_cam_param_df = pd.read_csv(input_init_cam_param_file_with_path,
                                    usecols=['imageBaseName', 'vFOV', 'posX', 'posY', 'posZ',
                                             'rotX', 'rotY', 'rotZ'],
                                    dtype={'imageBaseName': str, 'vFOV': float, 'posX': float,
                                           'posY': float, 'posZ': float, 'rotX': float, 'rotY': float,
                                           'rotZ': float})
    if len(init_cam_param_df['imageBaseName'].iloc[0]) == 12:
        init_cam_param_df['imageBaseName'] = init_cam_param_df['imageBaseName'].str[:-1]

    # create a CAM_PARA_LIST column for each row by combining columns of camera parameters with negation as needed
    # in the order of PERSPECTIVE_NEAR, PERSPECTIVE_VFOV, OBJ_LIDAR_X_OFFSET, OBJ_LIDAR_Y_OFFSET, OBJ_LIDAR_Z_OFFSET,
    # OBJ_ROT_Z, OBJ_ROT_Y, OBJ_ROT_X
    init_cam_param_df['OBJ_BASE_TRANS_LIST'] = init_cam_param_df.apply(lambda row:
                                                                       [CAM_NEAR, row['vFOV'], -row['posX'],
                                                                        -row['posY'], -row['posZ'], -row['rotZ'],
                                                                        -row['rotY'], -row['rotX']], axis=1)
    init_cam_param_df.drop(columns=['vFOV', 'posX', 'posY', 'posZ', 'rotX', 'rotY', 'rotZ'], inplace=True)
    print(init_cam_param_df)
    input_df = input_df.merge(init_cam_param_df, left_on='imageBaseName', right_on='imageBaseName', how='left')
    input_df['OBJ_BASE_TRANS_LIST'] = input_df['OBJ_BASE_TRANS_LIST'].apply(lambda x: x if isinstance(x, list) else [])
    start_time = time.time()

    # Shift CAM_Z, LATITUDE, and LONGITUDE columns to get the next row's value
    input_df['CAM_Z_next'] = input_df['CAM_Z'].shift(-1)
    input_df['LATITUDE_next'] = input_df['LATITUDE'].shift(-1)
    input_df['LONGITUDE_next'] = input_df['LONGITUDE'].shift(-1)
    input_df[[BASE_CAM_PARA_COL_NAME, OPTIMIZED_CAM_PARA_COL_NAME]] = input_df.apply(lambda row: align_image_to_lidar(
        row,
        image_seg_dir,
        lane_seg_dir,
        lidar_df,
        lidar_proj_output_file_path, optimize_fov), axis=1, result_type='expand')

    input_df.drop(columns=['CAM_Z', 'CAM_Z_next', 'LATITUDE_next', 'LONGITUDE_next'], inplace=True)
    input_df.to_csv(f'{os.path.splitext(obj_image_input)[0]}_with_cam_paras.csv', index=False)
    print(f'execution time: {time.time() - start_time}')
