import argparse
import os
import gc
import time
import pandas as pd
import numpy as np
import multiprocessing as mp
from scipy.spatial.transform import Rotation
from scipy.optimize import minimize
from math import radians, tan
from raycasting import find_occluded_points
from utils import get_camera_latlon_and_bearing_for_image_from_mapping, bearing_between_two_latlon_points, \
    get_aerial_lidar_road_geo_df, create_gdf_from_df, add_lidar_x_y_from_lat_lon, \
    classify_points_base_on_centerline, ROADSIDE, create_df_from_lidar_points

from extract_lidar_3d_points import extract_lidar_3d_points_for_camera
from get_road_boundary_points import get_image_lane_points, get_image_road_points, combine_lane_and_road_boundary

# indices as constants in the input object camera parameter list where OBJ_LIDAR_X/Y/Z_OFFSET indicate object
# translation along X/Y/Z axis in world coordinate system, OBJ_ROT_Z, OBJ_ROT_Y, OBJ_ROT_X
# indicate angle of rotation of the object around Z (bearing) axis, Y axis, and X axis, respectively, in the 3D world
# coordinate system. Object translations and rotations are negated as opposed to the corresponding camera translations
# and rotations
PERSPECTIVE_NEAR, PERSPECTIVE_VFOV, OBJ_LIDAR_X_OFFSET, OBJ_LIDAR_Y_OFFSET, OBJ_LIDAR_Z_OFFSET, \
    OBJ_ROT_Z, OBJ_ROT_Y, OBJ_ROT_X = 0, 1, 2, 3, 4, 5, 6, 7

LIDAR_DIST_THRESHOLD = (40, 800)  # in feet
init_cam_paras = []


def rotate_point(point, quaternion):
    rotated_point = quaternion.apply(point)
    return rotated_point


def init_transform_from_lidar_to_world_coordinate_system(df, cam1_x, cam1_y, cam1_z, cam2_x, cam2_y, cam2_z):
    # Compute the camera bearing direction vector from C1 to C2
    cam_bearing_vector = np.array([cam2_x - cam1_x, cam2_y - cam1_y, cam2_z - cam1_z])
    norm = np.linalg.norm(cam_bearing_vector)
    if norm > 0:
        cam_bearing_vector = cam_bearing_vector / np.linalg.norm(cam_bearing_vector)

    # The negative Z-axis is aligned with the camera bearing direction
    neg_z_axis = -cam_bearing_vector  # Negative Z-axis

    # Compute the other axes
    up_vector = np.array([0, 0, 1])
    y_axis = up_vector - np.dot(up_vector, neg_z_axis) * neg_z_axis # Remove any component of neg_z_axis from up_vector
    y_axis = y_axis / np.linalg.norm(y_axis)
    x_axis = np.cross(y_axis, neg_z_axis)
    # Transform each LIDAR point
    if 'CAM_DIST' not in df.columns:
        # Calculate the 2D distance (ignoring Z) between the camera and the LIDAR points
        df['CAM_DIST'] = np.sqrt(np.square(df.X - cam1_x) + np.square(df.Y - cam1_y))

    # Compute the relative positions of LIDAR points with respect to the camera
    relative_positions = np.vstack((df.X - cam1_x, df.Y - cam1_y, df.Z - cam1_z)).T

    # Project the relative positions onto the camera coordinate system
    df['INITIAL_WORLD_X'] = np.dot(relative_positions, x_axis)
    df['INITIAL_WORLD_Y'] = np.dot(relative_positions, y_axis)
    df['INITIAL_WORLD_Z'] = np.dot(relative_positions, neg_z_axis)

    return df


def transform_to_world_coordinate_system(df, cam_params):
    # transform X, Y, Z in LIDAR coordinate system to world coordinate system where the camera is at the origin,
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

    # Note that LIDAR world coordinate system origin is located at lower-left corner while
    # screen coordinate system origin is located at upper-left corner
    df['PROJ_SCREEN_X'] = (projected_points[:, 0] * half_width + half_width).astype(int)
    df['PROJ_SCREEN_Y'] = (-projected_points[:, 1] * half_height + half_height).astype(int)
    return df


def transform_camera_position(cam_x, cam_y, cam_z, cam_params):
    initial_camera_position = np.array([cam_x, cam_y, cam_z])
    # Apply inverse translation
    transformed_camera_position = initial_camera_position - np.array([
        cam_params[OBJ_LIDAR_X_OFFSET],
        cam_params[OBJ_LIDAR_Y_OFFSET],
        cam_params[OBJ_LIDAR_Z_OFFSET]
    ])

    return transformed_camera_position


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


def compute_distance(proj_x_3d, proj_y_3d, x_2d, y_2d):
    """
    Compute distance between 3D projected coordinates and 2D coordinates.
    Returns:
        x_diff: Absolute differences in X (shape: n_3d x n_2d).
        y_diff: Absolute differences in Y (shape: n_3d x n_2d).
    """
    x_diff = np.abs(proj_x_3d[:, np.newaxis] - x_2d[np.newaxis, :])  # Shape: (n_3d, n_2d)
    y_diff = np.abs(proj_y_3d[:, np.newaxis] - y_2d[np.newaxis, :])  # Shape: (n_3d, n_2d)

    return x_diff, y_diff


def get_left_right_side_df_and_values(df):
    df_l = df[df['SIDE'] == ROADSIDE.LEFT.value]
    df_r = df[df['SIDE'] == ROADSIDE.RIGHT.value]
    return df_l, df_r



def compute_grid_minimum_distances(x_3d, y_3d, x_2d, y_2d, x_grid_th, y_grid_th):
    """
    Function to compute minimum distances between each point in (x_3d, y_3d) and (x_2d, y_2d)
    leveraging numpy broadcasting and vectorization
    """
    if len(x_3d) == 0 or len(y_3d) == 0 or len(x_2d) == 0 or len(y_2d) == 0:
        return 1e6  # No points to compare, return large penalty

    # Compute the absolute differences in x and y directions
    diff_x, diff_y = compute_distance(x_3d, y_3d, x_2d, y_2d)
    max_grid_x = np.max(diff_x, axis=1)
    max_grid_y = np.max(diff_y, axis=1)

    # Apply the grid threshold filter: Only keep points within grid_th in both x and y directions
    within_grid_mask = (diff_x < x_grid_th) & (diff_y < y_grid_th)

    if not np.any(within_grid_mask):
        # If no points are within the grid, return a large penalty for stability
        return 1e6

    # For points outside the grid, set the distances to a large value to exclude them from being chosen
    dist_squared = np.where(within_grid_mask, diff_x ** 2 + diff_y ** 2, np.inf)
    min_distances = np.min(dist_squared, axis=1)
    no_match_mask = np.isinf(min_distances)
    # Initialize fallback distances with max distances in x and y direction (in case no valid match is found)
    min_distances[no_match_mask] = np.maximum(max_grid_x[no_match_mask], max_grid_y[no_match_mask])
    # Find the minimum distance for each 3D point in the filtered data
    return np.mean(min_distances)


def objective_function_2d(cam_params, df_3d, df_2d, img_wd, img_ht, grid_th_x, grid_th_y):
    # compute alignment error corresponding to the cam_params using the sum of squared distances between projected
    # LIDAR vertices and the road boundary pixels
    full_cam_params = get_full_camera_parameters(cam_params)
    try:
        df_3d = transform_3d_points(df_3d, full_cam_params, img_wd, img_ht)
    except SkipOptimizationException as e:
        raise SkipOptimizationException(e.exception_reason, e.exception_value)

    if df_2d.empty or df_3d.empty:
        raise SkipOptimizationException("Input dataframes are empty. Cannot compute alignment error.")

    # split df_2d and df_3d based on SIDE
    df_2d_l, df_2d_r = get_left_right_side_df_and_values(df_2d)
    df_3d_l, df_3d_r = get_left_right_side_df_and_values(df_3d)

    # compute grid-based distances for both left and right sides
    x_3d_l = df_3d_l['PROJ_SCREEN_X'].values
    y_3d_l = df_3d_l['PROJ_SCREEN_Y'].values
    x_3d_r = df_3d_r['PROJ_SCREEN_X'].values
    y_3d_r = df_3d_r['PROJ_SCREEN_Y'].values
    dists_l = compute_grid_minimum_distances(x_3d_l, y_3d_l, df_2d_l['X'].values, df_2d_l['Y'].values,
                                             grid_th_x, grid_th_y)
    dists_r = compute_grid_minimum_distances(x_3d_r, y_3d_r, df_2d_r['X'].values, df_2d_r['Y'].values,
                                             grid_th_x, grid_th_y)

    alignment_error = dists_l + dists_r
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
    full_cam_para_len = len(init_cam_paras)
    if len(cam_p) < full_cam_para_len:
        combined = init_cam_paras[:len(init_cam_paras)-len(cam_p)]
        combined.extend(cam_p)
    else:
        combined = cam_p

    return combined


# def derive_next_camera_params(v1, v2, cam_para1):
#    v1_norm = v1 / np.linalg.norm(v1)
#    v2_norm = v2 / np.linalg.norm(v2)
#    if np.allclose(v1_norm, v2_norm):
#        # parallel vectors
#        return cam_para1  # No rotation needed

#   # Use robust alignment to derive rotation matrix
#    quaternion = Rotation.align_vectors([v2_norm], [v1_norm])[0]
#    rot_mat12 = quaternion.as_matrix()
#    rot_mat1 = Rotation.from_euler('xyz', np.array([cam_para1[OBJ_ROT_X], cam_para1[OBJ_ROT_Y],
#                                                    cam_para1[OBJ_ROT_Z]]), degrees=True).as_matrix()
#    rot_mat2 = np.matmul(rot_mat1, rot_mat12)
#    # Regularize rotation matrix to ensure orthonormality
#    u, _, vh = np.linalg.svd(rot_mat2)
#    rot_mat2 = np.dot(u, vh)

#    cam_para2 = cam_para1.copy()
#    cam_para2[OBJ_ROT_X], cam_para2[OBJ_ROT_Y], cam_para2[OBJ_ROT_Z] = \
#        Rotation.from_matrix(rot_mat2).as_euler('xyz', degrees=True)

#    return cam_para2


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


def compute_offsets(row_no, init_error, x_diff, y_diff):
    """
    Compute translation and rotation offsets based on accumulative dissimilarity.
    Arguments:
        row_no: the frame number to compute offsets for.
        init_error: initial alignment error
        x_diff: minimal difference along X between projected LIDAR data and image segmentation
        y_diff: minimal difference along Y between projected LIDAR data and image segmentation
    Returns:
        dict: Offsets for LIDAR data translation and rotation.
    """
    x_trans_base = y_trans_base = z_trans_base = 1.1
    rot_base = 0.11

    if row_no > 11 and init_error > 2000:
        rot_base = 0.2 if init_error < 3000 else 0.5

    if row_no <= 11 or (x_diff < 100 and y_diff < 100):
        use_base = True
    else:
        use_base = False

    if use_base:
        offsets = {
            "x_trans_offset": (init_cam_paras[OBJ_LIDAR_X_OFFSET] - x_trans_base,
                               init_cam_paras[OBJ_LIDAR_X_OFFSET] + x_trans_base),
            "y_trans_offset": (init_cam_paras[OBJ_LIDAR_Y_OFFSET] - y_trans_base,
                               init_cam_paras[OBJ_LIDAR_Y_OFFSET] + y_trans_base),
            "z_trans_offset": (init_cam_paras[OBJ_LIDAR_Z_OFFSET] - z_trans_base,
                               init_cam_paras[OBJ_LIDAR_Z_OFFSET] + z_trans_base),
            "x_rot_offset": (init_cam_paras[OBJ_ROT_X] - rot_base,
                             init_cam_paras[OBJ_ROT_X] + rot_base),
            "y_rot_offset": (init_cam_paras[OBJ_ROT_Y] - rot_base,
                             init_cam_paras[OBJ_ROT_Y] + rot_base),
            "z_rot_offset": (init_cam_paras[OBJ_ROT_Z] - rot_base,
                             init_cam_paras[OBJ_ROT_Z] + rot_base)
        }
    else:
        offsets = {
            "x_trans_offset": (-10, 10) if x_diff > 90 else (init_cam_paras[OBJ_LIDAR_X_OFFSET] - x_trans_base,
                                                              init_cam_paras[OBJ_LIDAR_X_OFFSET] + x_trans_base),
            "y_trans_offset": (-11, 11) if y_diff > 90 else (init_cam_paras[OBJ_LIDAR_Y_OFFSET] - y_trans_base,
                                                              init_cam_paras[OBJ_LIDAR_Y_OFFSET] + y_trans_base),
            "z_trans_offset": (-18, 18) if y_diff > 90 else (init_cam_paras[OBJ_LIDAR_Z_OFFSET] - z_trans_base,
                                                              init_cam_paras[OBJ_LIDAR_Z_OFFSET] + z_trans_base),
            "x_rot_offset": (-2, 2) if y_diff > 90 else (init_cam_paras[OBJ_ROT_X] - rot_base,
                                                          init_cam_paras[OBJ_ROT_X] + rot_base),
            "y_rot_offset": (-3, 3) if y_diff > 90 else (init_cam_paras[OBJ_ROT_Y] - rot_base,
                                                          init_cam_paras[OBJ_ROT_Y] + rot_base),
            "z_rot_offset": (-2, 2) if y_diff > 90 else (init_cam_paras[OBJ_ROT_Z] - rot_base,
                                                          init_cam_paras[OBJ_ROT_Z] + rot_base)
        }

    return offsets


def align_image_to_lidar(row_index, row, seg_image_dir, seg_lane_dir, out_proj_file_path):
    """
    :param row_index: the index of the row in the original dataframe
    :param row: the image metadata dataframe row as a dict to be processed
    :param seg_image_dir: path in which segmentation images are located
    :param seg_lane_dir: path in which road lanes segmentation images are located
    :param out_proj_file_path: output path for aligned road info which will be appended with
    lidar_project_info_{image name} to have lidar projection info for each input image
    :return: the computed base camera parameters and optimized camera parameters
    """
    global init_cam_paras

    if len(row['imageBaseName']) == 11:
        image_name_with_path = os.path.join(seg_image_dir, f'{row["imageBaseName"]}1.png')
        # get input image base name
        input_2d_mapped_image = row['imageBaseName']
    else:
        image_name_with_path = os.path.join(seg_image_dir, f'{row["imageBaseName"]}.png')
        # get input image base name
        input_2d_mapped_image = row['imageBaseName'][:-1]

    if not row['OBJ_BASE_TRANS_LIST']:
        print(f'Initial camera parameters for image {input_2d_mapped_image} must be specified to perform camera '
              f'parameter optimization on the route. Exiting')
        exit(1)

    init_cam_paras = row['OBJ_BASE_TRANS_LIST']
    if row['camImageBaseName'] == row['imageBaseName']:
        do_optimize = False # does not do optimization for the first image obtained from manual registration
    else:
        do_optimize = True

    grid_threshold_x = grid_threshold_y = 300
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
        return init_cam_paras, -1

    # compute bearing
    cam_br = bearing_between_two_latlon_points(cam_lat, cam_lon, cam_lat2, cam_lon2, is_degree=False)

    proj_cam_x = row['geometry'].x
    proj_cam_y = row['geometry'].y

    cam_lidar_z = row['CAM_Z']
    ldf = row['filtered_lidar']
    t1 = time.time()
    vertices, cam_br, cols = extract_lidar_3d_points_for_camera(ldf, [cam_lat, cam_lon], [cam_lat2, cam_lon2],
                                                                dist_th=LIDAR_DIST_THRESHOLD,
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

    cam_df = pd.DataFrame(data={'LATITUDE': [cam_lat2], 'LONGITUDE': [cam_lon2]})
    cam_gdf = add_lidar_x_y_from_lat_lon(cam_df)
    proj_cam_x2 = cam_gdf.iloc[0].x
    proj_cam_y2 = cam_gdf.iloc[0].y
    proj_cam_z2 = row['CAM_Z_next'] if pd.notna(row['CAM_Z_next']) else row['CAM_Z']
    print(f'proj_cam_z2: {proj_cam_z2}')

    input_3d_gdf = init_transform_from_lidar_to_world_coordinate_system(input_3d_gdf, proj_cam_x, proj_cam_y,
                                                                        cam_lidar_z, proj_cam_x2, proj_cam_y2,
                                                                        proj_cam_z2)

    # output base lidar project info to base_lidar_project_info_{image_base_name}.csv file since the base
    # camera orientation/bearing info is updated from the optimized version of its previous image using
    # road tangent info. The optimization is based on updated camera base parameters
    input_3d_gdf = transform_3d_points(input_3d_gdf, init_cam_paras, img_width, img_height)
    seg_image_name = os.path.join(seg_image_dir, f'{input_2d_mapped_image}1.png')
    img_width, img_height, input_road_img, input_list = get_image_road_points(seg_image_name)
    if len(input_2d_points) > 0 and len(input_list[0]) > 0:
        input_2d_points = combine_lane_and_road_boundary(input_2d_points, lane_image, input_road_img,
                                                         seg_image_name, image_height=img_height)
    elif len(input_list[0]) > 0:
        input_2d_points = input_list[0]

    if m_points is None:
        # no middle lane axis and centroid can be computed from segmented road lanes, which indicates a
        # complicated road scene such as 4-way intersection, need to skip this image and return without optimization
        return init_cam_paras, -1

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
            return init_cam_paras, -1

        input_2d_df = pd.DataFrame({
            'X': input_2d_points[:, 0],
            'Y': input_2d_points[:, 1],
            'SIDE': input_2d_sides
        })
        input_2d_df.to_csv(os.path.join(out_proj_file_path, f'input_2d_{input_2d_mapped_image}.csv'), index=False)
    else:
        print(f'input_2d_points.shape[1] must be 2, but it is {input_2d_points.shape[1]}, skip this image '
              f'and return without optimization')
        return init_cam_paras, -1

    input_3d_gdf = find_occluded_points(input_3d_gdf,
                                        transform_camera_position(proj_cam_x, proj_cam_y, cam_lidar_z, init_cam_paras),
                                        img_width, img_height, ground_only=True, lowest_hit=False)
    input_3d_road_bound_gdf = input_3d_gdf[(input_3d_gdf.OCCLUDED == False) &
                                           (input_3d_gdf.BOUND == 1)].reset_index(drop=True).copy()
    if 'SIDE' in cols:
        input_3d_road_bound_gdf['SIDE'] = input_3d_road_bound_gdf['SIDE'].astype(int)
    print(f'after occlusion filtering, input_3d_road_bound_gdf.shape: {input_3d_road_bound_gdf.shape}')
    input_3d_road_bound_gdf.to_csv(os.path.join(out_proj_file_path,
                                                f'base_lidar_project_info_{row["imageBaseName"]}_non_occluded.csv'),
                                   index=False)
    if not do_optimize:
        input_3d_gdf.to_csv(out_proj_file, index=False)
        return init_cam_paras, -1

    # check alignment error to see whether constraints need to be reduced
    align_error = objective_function_2d(init_cam_paras[2:], input_3d_road_bound_gdf,
                                        input_2d_df, img_width, img_height,50, 50)

    filtered_ldf = _filter_dataframe_within_screen_bounds(input_3d_road_bound_gdf, img_width, img_height)
    max_y_diff = abs(input_2d_points[:, 1].min() - filtered_ldf['PROJ_SCREEN_Y'].min())

    # find the max_x_diff on the lowest overlapping row or y
    common_y_values = np.intersect1d(input_2d_points[:, 1], filtered_ldf['PROJ_SCREEN_Y'])
    common_y_values = np.sort(common_y_values)[::-1]  # Sort in descending order
    max_x_diff = filtered_ldf['PROJ_SCREEN_X'].min() - input_2d_points[:, 0].min()
    for y in common_y_values:
        # Get rows corresponding to the current Y value in each array
        input_x_values = input_2d_points[input_2d_points[:, 1] == y][:, 0]
        filtered_x_values = filtered_ldf[filtered_ldf['PROJ_SCREEN_Y'] == y]['PROJ_SCREEN_X'].to_numpy()
        # Check if both arrays have at least 2 points for this Y value
        if len(input_x_values) >= 2 and len(filtered_x_values) >= 2:
            # Check if the points in each array are at least 500 pixels apart
            input_x_range = input_x_values.max() - input_x_values.min()
            filtered_x_range = filtered_x_values.max() - filtered_x_values.min()
            if input_x_range >= 500 and filtered_x_range >= 500:
                # Find the smallest and largest X values for this Y value in both arrays
                input_min_x = input_x_values.min()
                input_max_x = input_x_values.max()
                filtered_min_x = filtered_x_values.min()
                filtered_max_x = filtered_x_values.max()

                # Compute the differences
                min_x_diff = abs(input_min_x - filtered_min_x)
                max_x_diff_for_y = abs(input_max_x - filtered_max_x)

                # Take the larger of the two differences
                max_diff_for_y = max(min_x_diff, max_x_diff_for_y)

                # Update the overall maximum X difference and record the chosen Y
                max_x_diff = max_diff_for_y
                print(
                    f"Lowest common Y value: {y}, input_min_x: {input_min_x}, input_max_x: {input_max_x}, "
                    f"filtered_min_x: {filtered_min_x}, filtered_max_x: {filtered_max_x}")
                # Break the loop as we found the largest Y that satisfies the conditions
                break

    print(f'max_x_diff: {max_x_diff}, max_y_diff: {max_y_diff}')
    if align_error < 1400 and max_x_diff < 150 and max_y_diff < 150:
        print(f'current alignment error: {align_error}, base is sufficient')
        # no need to do optimization, using base alignment is good enough
        input_3d_gdf.to_csv(out_proj_file, index=False)
        return init_cam_paras, align_error

    print(f'current alignment error: {align_error}')
    offset = compute_offsets(row_index, align_error, max_x_diff, max_y_diff)
    print(f'offset: {offset}')
    if max_y_diff > grid_threshold_y:
        grid_threshold_y = max_y_diff + 200
        print(f'grid_threshold_y is changed to {grid_threshold_y}  since max_y_diff is {max_y_diff}')

    if max_x_diff > grid_threshold_x:
        grid_threshold_x = max_x_diff + 200
        print(f'grid_threshold_x is changed to {grid_threshold_x}  since max_x_diff is {max_x_diff}')

    start_idx = 2
    cam_para_bounds = [offset['x_trans_offset'],
                       offset['y_trans_offset'],
                       offset['z_trans_offset'],
                       offset['z_rot_offset'],
                       offset['y_rot_offset'],
                       offset['x_rot_offset']]

    cam_output_columns = ['translation_x', 'translation_y', 'translation_z',
                          'rotation_z', 'rotation_y', 'rotation_x']

    t1 = time.time()
    try:
        result = minimize(objective_function_2d, init_cam_paras[start_idx:],
                          args=(input_3d_road_bound_gdf,
                                input_2d_df, img_width, img_height, grid_threshold_x, grid_threshold_y),
                          method='Nelder-Mead',
                          # bounds in the order of OBJ_LIDAR_X_OFFSET, OBJ_LIDAR_Y_OFFSET, OBJ_LIDAR_Z_OFFSET, \
                          # OBJ_ROT_Z, OBJ_ROT_Y, OBJ_ROT_X
                          bounds=cam_para_bounds,
                          options={'maxiter': 1000, 'disp': True})
    except SkipOptimizationException as ex:
        print(ex)
        return init_cam_paras, align_error

    optimized_cam_params = result.x
    print(f'optimizing result for image {input_2d_mapped_image}: {result}')
    print(f'Status: {result.message}, total evaluations: {result.nfev}')
    print(f'optimized_cam_params for image {image_name_with_path}: {optimized_cam_params}, '
          f'time spend: {time.time() - t1}')

    full_optimized_cam_paras = get_full_camera_parameters(optimized_cam_params)
    input_3d_gdf = transform_3d_points(input_3d_gdf, full_optimized_cam_paras,
                                       img_width, img_height)

    input_3d_gdf.to_csv(out_proj_file, index=False)
    proj_base, proj_ext = os.path.splitext(out_proj_file)
    # output optimized camera parameter for the image
    cam_para_df = pd.DataFrame(data=[optimized_cam_params.tolist()], columns=cam_output_columns)
    cam_para_df.to_csv(f'{proj_base}_cam_paras.csv', index=False)

    return optimized_cam_params, align_error


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Process arguments.')
    parser.add_argument('--input_lidar_with_path', type=str,
                        default='/projects/ncdot/NC_2018_Secondary_2/d13_route_40001001012/'
                        #default='data/d13_route_40001001012/'
                                'route_40001001012_voxel_raster_norm_highest_20240113_sides.csv',
                        help='input file that contains road x, y, z vertices from lidar')
    parser.add_argument('--image_seg_dir', type=str,
                        default='/projects/ncdot/NC_2018_Secondary_2/segmentations/d13/881',
                        #default='data/d13_route_40001001012/segmentation',
                        help='directory to retrieve segmentation images')
    parser.add_argument('--lane_seg_dir', type=str,
                        default='/projects/ncdot/NC_2018_Secondary_2/lanes/d13/881',
                        #default='data/d13_route_40001001012/segmentation',
                        help='directory to retrieve segmented road lane images')
    parser.add_argument('--obj_image_input', type=str,
                        default='/projects/ncdot/NC_2018_Secondary_2/d13_route_40001001012/route_40001001012_input_corrected_updated.csv',
                        #default='data/d13_route_40001001012/route_input.csv',
                        help='input csv file that contains image base names with objects detected along with other '
                             'inputs for mapping')
    parser.add_argument('--input_init_cam_param_file_with_path', type=str,
                        default='/projects/ncdot/NC_2018_Secondary_2/d13_route_40001001012/route_40001001012_initial_camera_params.csv',
                        #default='data/d13_route_40001001012/initial_camera_params.csv',
                        help='input csv file that includes initial camera parameters for manually registered images')
    parser.add_argument('--lidar_proj_output_file_path', type=str,
                        default='/projects/ncdot/NC_2018_Secondary_2/d13_route_40001001012/route_40001001012_geotagging_output',
                        #default='data/d13_route_40001001012/test',
                        help='output file path path where projected LIDAR data will be saved')

    args = parser.parse_args()
    input_lidar = args.input_lidar_with_path
    image_seg_dir = args.image_seg_dir
    lane_seg_dir = args.lane_seg_dir
    obj_image_input = args.obj_image_input
    input_init_cam_param_file_with_path = args.input_init_cam_param_file_with_path
    lidar_proj_output_file_path = args.lidar_proj_output_file_path

    lidar_df = get_aerial_lidar_road_geo_df(input_lidar)

    input_df = get_input_file_with_images(obj_image_input)
    init_cam_param_df = pd.read_csv(input_init_cam_param_file_with_path,
                                    usecols=['routeID', 'imageBaseName', 'vFOV', 'posX', 'posY', 'posZ',
                                             'rotX', 'rotY', 'rotZ'],
                                    dtype={'routeID': int, 'imageBaseName': str, 'vFOV': float, 'posX': float,
                                           'posY': float, 'posZ': float, 'rotX': float, 'rotY': float,
                                           'rotZ': float})
    if len(init_cam_param_df['imageBaseName'].iloc[0]) == 12:
        init_cam_param_df['imageBaseName'] = init_cam_param_df['imageBaseName'].str[:-1]

    # create a CAM_PARA_LIST column for each row by combining columns of camera parameters with negation as needed
    # in the order of PERSPECTIVE_NEAR, PERSPECTIVE_VFOV, OBJ_LIDAR_X_OFFSET, OBJ_LIDAR_Y_OFFSET, OBJ_LIDAR_Z_OFFSET,
    # OBJ_ROT_Z, OBJ_ROT_Y, OBJ_ROT_X
    init_cam_param_df['OBJ_BASE_TRANS_LIST'] = init_cam_param_df.apply(lambda row:
                                                                       [0.1, row['vFOV'], -row['posX'],
                                                                        -row['posY'], -row['posZ'], -row['rotZ'],
                                                                        -row['rotY'], -row['rotX']], axis=1)
    init_cam_param_df.drop(columns=['vFOV', 'posX', 'posY', 'posZ', 'rotX', 'rotY', 'rotZ'], inplace=True)
    print(init_cam_param_df)
    input_df = input_df.merge(init_cam_param_df, left_on='ROUTEID', right_on='routeID', how='left')
    input_df.rename(columns={'imageBaseName_x': 'imageBaseName'}, inplace=True)
    input_df.rename(columns={'imageBaseName_y': 'camImageBaseName'}, inplace=True)
    input_df['OBJ_BASE_TRANS_LIST'] = input_df['OBJ_BASE_TRANS_LIST'].apply(lambda x: x if isinstance(x, list) else [])
    start_time = time.time()

    # Shift CAM_Z, LATITUDE, and LONGITUDE columns to get the next row's value
    input_df['CAM_Z_next'] = input_df['CAM_Z'].shift(-1)
    input_df['LATITUDE_next'] = input_df['LATITUDE'].shift(-1)
    input_df['LONGITUDE_next'] = input_df['LONGITUDE'].shift(-1)

    num_workers = mp.cpu_count()
    print(f'num_workers: {num_workers}')

    # reduce numpy/OpenBLAS threads to 1 per process to prevent numpy/scipy from spawning extra
    # threads inside each worker
    os.environ["OMP_NUM_THREADS"] = "1"
    os.environ["OPENBLAS_NUM_THREADS"] = "1"
    os.environ["MKL_NUM_THREADS"] = "1"
    os.environ["VECLIB_MAXIMUM_THREADS"] = "1"
    os.environ["NUMEXPR_NUM_THREADS"] = "1"

    # Precompute relevant lidar subsets for each row
    input_df['geometry'] = add_lidar_x_y_from_lat_lon(input_df)
    input_df["filtered_lidar"] = input_df.apply(
        lambda row: lidar_df[
            ((lidar_df.X - row.geometry.x).abs() < LIDAR_DIST_THRESHOLD[1]) &
            ((lidar_df.Y - row.geometry.y).abs() < LIDAR_DIST_THRESHOLD[1])
            ].copy(deep=True),
        axis=1
    )
    # force garbage collection to conserve memory
    del lidar_df
    gc.collect()

    # Convert DataFrame rows to a list of tuples for multiprocessing
    rows = zip(input_df.index,
               input_df.to_dict(orient="records"),
               [image_seg_dir] * len(input_df),
               [lane_seg_dir] * len(input_df),
               [lidar_proj_output_file_path] * len(input_df))

    with mp.Pool(num_workers, maxtasksperchild=10) as pool:
        results = pool.starmap(align_image_to_lidar, rows)

    optimized_params, base_align_errors = zip(*results)
    input_df['OPTIMIZED_CAMERA_OBJ_PARA'] = optimized_params
    input_df['BASE_ALIGN_ERROR'] = base_align_errors

    input_df.drop(columns=['CAM_Z', 'CAM_Z_next', 'LATITUDE_next', 'LONGITUDE_next'], inplace=True)
    input_df.to_csv(f'{os.path.splitext(obj_image_input)[0]}_with_cam_paras.csv', index=False)
    print(f'execution time: {time.time() - start_time}')
