import argparse
import os
import time
import pickle
import pandas as pd
import numpy as np
from scipy.spatial.transform import Rotation
from scipy.optimize import minimize
from scipy.interpolate import UnivariateSpline
from math import radians, tan
from utils import get_camera_latlon_and_bearing_for_image_from_mapping, bearing_between_two_latlon_points, \
    get_aerial_lidar_road_geo_df, compute_match, create_gdf_from_df, add_lidar_x_y_from_lat_lon, \
    angle_between

from extract_lidar_3d_points import get_lidar_data_from_shp, extract_lidar_3d_points_for_camera
from get_road_boundary_points import get_image_road_points, get_image_lane_points


# indices as constants in the input camera parameter list where CAMERA_LIDAR_X/Y/Z_OFFSET indicate camera
# translation to move camera along X/Y/Z axis in world coordinate system, CMAERA_YAM, CAMERA_PITCH, CAMERA_ROLL
# indicate camera angle of rotation around Z (bearing) axis, Y axis, and X axis, respectively, in the 3D world
# coordinate system
FOCAL_LENGTH_X = FOCAL_LENGTH_Y = 2.8
BASE_CAM_PARA_COL_NAME = 'BASE_CAMERA_PARA'
OPTIMIZED_CAM_PARA_COL_NAME = 'OPTIMIZED_CAMERA_PARA'

PERSPECTIVE_NEAR, PERSPECTIVE_VFOV, CAMERA_LIDAR_X_OFFSET, CAMERA_LIDAR_Y_OFFSET, CAMERA_LIDAR_Z_OFFSET, \
    CAMERA_YAW, CAMERA_PITCH, CAMERA_ROLL = 0, 1, 2, 3, 4, 5, 6, 7
# initial camera parameter list for optimization
# INIT_CAMERA_PARAMS = [0.1, 20, 1.6, -8.3, -3.9, 1.1, -0.91, -0.53] # for route 40001001011
# INIT_CAMERA_PARAMS = [0.1, 20, 6.1, -9.1, 8.6, -4.3, 2.8, 0.17] # new test scene route 881000952181 test image
# INIT_CAMERA_PARAMS = [0.1, 20, 7.2, -7.3, 8.6, -4.3, 3.1, -0.24] # new test scene route 881000952281 test image
INIT_CAMERA_PARAMS = [0.1, 20, 5.4, -7.1, 14, -0.049, 1.7, -0.18]  # new test scene route 881000954101 test image
PREV_CAM_PARAS = None
PREV_CAM_BEARING_VEC = {'camera': {},
                        'road': {}}
NUM_ITERATIONS = 1000  # optimizer hyperparameters
# reduced the LIDAR distance threshold to get less farther away LIDAR points to align with lane lines which
# don't capture the farther away lane paint
LIDAR_DIST_THRESHOLD = (0, 156)  # (1, 154)
SPLINE_FIT_DIST_THRESHOLD = 15
SPLINE_SMOOTHING_FACTOR = 100
USE_ROAD_TANGENT_ANGLE_THRESHOLD = 30


def rotate_point(point, quaternion):
    rotated_point = quaternion.apply(point)
    return rotated_point


def interpolate_camera_z(p1_z, p2_z, p1_dist, p2_dist):
    """
    interpolate camera z value based on camera's closet points on one side of the road, (p1_dist, p1_z) and
    (p2_dist, p2_z) where p_dist is the distance from the point to camera and p_z is the LIDAR Z value
    """
    return p1_z - p1_dist * (p2_z - p1_z) / (p2_dist - p1_dist)


def init_transform_from_lidar_to_world_coordinate_system(df, cam_x, cam_y, cam_z):
    # transform LIDAR points from LIDAR projection coordinate system to world coordinate system without
    # considering camera pose parameters
    df['UPDATE_X'] = df.X - cam_x
    df['UPDATE_Y'] = df.Y - cam_y
    # Calculate the distance between the cam_x, cam_y point and the first two X, Y columns of input_3d_points
    df['CAM_DIST'] = np.sqrt(np.square(df.UPDATE_X) + np.square(df.UPDATE_Y))
    df['INITIAL_WORLD_Z'] = -df.CAM_DIST * np.cos(df.BEARING)
    df['INITIAL_WORLD_Y'] = df.Z - cam_z
    df['INITIAL_WORLD_X'] = df.CAM_DIST * np.sin(df.BEARING)
    return df


def transform_to_world_coordinate_system(df, cam_params):
    # transform X, Y, Z in LIDAR coordinate system to world coordinate system where the camera is at the origin,
    # the z-axis is pointing from the camera along the cam_bearing direction, the y-axis is perpendicular to the
    # z-axis reflecting the elevation Z pointing upwards, and the x-axis is perpendicular to both y-axis and z-axis
    # reflecting X and Y. Note that LIDAR world coordinate system origin is located at lower-left corner while
    # screen coordinate system origin is located at upper-left corner
    rotation_x = Rotation.from_euler('x', radians(cam_params[CAMERA_ROLL]))
    rotation_y = Rotation.from_euler('y', radians(cam_params[CAMERA_PITCH]))
    rotation_z = Rotation.from_euler('z', radians(cam_params[CAMERA_YAW]))
    combined_rotation = rotation_z * rotation_y * rotation_x

    points = df[['INITIAL_WORLD_X', 'INITIAL_WORLD_Y', 'INITIAL_WORLD_Z']].to_numpy()
    rotated_point = np.apply_along_axis(rotate_point, axis=1, arr=points, quaternion=combined_rotation)
    rp_df = pd.DataFrame(rotated_point, columns=['WORLD_X', 'WORLD_Y', 'WORLD_Z'])
    df['WORLD_X'], df['WORLD_Y'], df['WORLD_Z'] = rp_df['WORLD_X'], rp_df['WORLD_Y'], rp_df['WORLD_Z']

    df['WORLD_Z'] = df['WORLD_Z'] + cam_params[CAMERA_LIDAR_Z_OFFSET]
    df['WORLD_Y'] = df['WORLD_Y'] + cam_params[CAMERA_LIDAR_Y_OFFSET]
    df['WORLD_X'] = df['WORLD_X'] + cam_params[CAMERA_LIDAR_X_OFFSET]
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
    far = max(df['INITIAL_WORLD_X'].max(), df['INITIAL_WORLD_Y'].max(), df['INITIAL_WORLD_Z'].max()) * 10
    top = cam_params[PERSPECTIVE_NEAR] * tan(radians(0.5 * cam_params[PERSPECTIVE_VFOV]))
    height = 2 * top
    width = aspect * height
    left = -0.5 * width
    right = left + width
    bottom = top - height
    # print(f'hfov: {degrees(atan2(width/2, cam_params[PERSPECTIVE_NEAR])) * 2}')
    x = 2 * cam_params[PERSPECTIVE_NEAR] / (right - left)
    y = 2 * cam_params[PERSPECTIVE_NEAR] / (top - bottom)
    a = (right + left) / (right - left)
    b = (top + bottom) / (top - bottom)
    c = - (far + cam_params[PERSPECTIVE_NEAR]) / (far - cam_params[PERSPECTIVE_NEAR])
    d = (- 2 * far * cam_params[PERSPECTIVE_NEAR]) / (far - cam_params[PERSPECTIVE_NEAR])
    matrix_elements = [
        x, 0, 0, 0,
        0, y, 0, 0,
        a, b, c, -1,
        0, 0, d, 0
    ]
    # project to 2D camera coordinate system
    df['PROJ_X'] = df.apply(
        lambda row: apply_matrix4(row['WORLD_X'], row['WORLD_Y'], row['WORLD_Z'], matrix_elements, return_axis='x'),
        axis=1)
    df['PROJ_Y'] = df.apply(
        lambda row: apply_matrix4(row['WORLD_X'], row['WORLD_Y'], row['WORLD_Z'], matrix_elements, return_axis='y'),
        axis=1)

    half_width = img_width / 2
    half_height = img_hgt / 2
    df['PROJ_SCREEN_X'] = df['PROJ_X'].apply(
        lambda x: int(x * half_width + half_width))
    df['PROJ_SCREEN_Y'] = df['PROJ_Y'].apply(
        lambda y: int(-(y * half_height) + half_height))
    return df


def get_2d_road_points_by_z(idf, filter_col, compare_val, threshold_val=30):
    """
    get road points from idf in which the difference between its filter_col value and compare_val is less than a
    threshold
    :param idf: input dataframe that includes filter_col
    :param filter_col: filter column included in the input dataframe
    :param compare_val: the value to compare difference with in idf[filter_col]
    :param threshold_val: the threshold value for comparing the absolute difference from for filtering
    :return: a filtered dataframe that meets the filtering condition
    """
    if filter_col not in idf.columns:
        print(f'{filter_col} not in input dataframe {idf}, return the input dataframe without filtering')
        return idf
    return idf[abs(idf[filter_col] - compare_val) < threshold_val]


def _compute_mse(df, x_col1, x_col2, y_col1, y_col2):
    """
    compute mean square error between (x_col1, y_col1) and (x_col2, y_col2)
    :param df: input dataframe that contains four columns to compute MSE from
    :param x_col1: the first x column
    :param x_col2: the second x column
    :param y_col1: the first y column
    :param y_col2: the second y column
    :return: mean square error
    """
    # Calculate squared differences for X and Y columns
    squared_diff_x = (df[x_col1] - df[x_col2]) ** 2
    squared_diff_y = (df[y_col1] - df[y_col2]) ** 2

    # Calculate mean squared error
    return np.mean(squared_diff_x + squared_diff_y)


def mean_squared_error(points1, points2_df, points2_df_x_col, points2_df_y_col):
    """
    calculate the mean squared error between points1 and points2. The given points1 and points2 are assumed
    to be in the corresponding order for computing the squared difference
    :param points1: a list of points with each point represented as a tuple (x, y)
    :param points2_df: a dataframe of points with each row represented as a point
    with points2_df_x_col, points2_df_y_col columns
    :param points2_df_x_col: the x column in points2_df
    :param points2_df_y_col: the y column in points2_df
    :return: MSE between points1 and points2 in the given order
    """
    # Convert the list of tuples to a DataFrame for easier manipulation
    df1 = pd.DataFrame(points1, columns=['X1', 'Y1'])

    # Merge the df1 DataFrame and given points2_df on the index
    merged_df = pd.concat([df1, points2_df], axis=1)

    # only keep the first and last rows to test out only aligning the corner points
    merged_df = merged_df.iloc[[0, -1]]
    print(f'merged_df: {merged_df}')
    return _compute_mse(merged_df, 'X1', points2_df_x_col, 'Y1', points2_df_y_col)


def objective_function_2d(cam_params, df_3d, df_2d, img_wd, img_ht, align_errors):
    # compute alignment error corresponding to the cam_params using the sum of squared distances between projected
    # LIDAR vertices and the road boundary pixels
    full_cam_params = get_full_camera_parameters(cam_params)
    df_3d = transform_3d_points(df_3d, full_cam_params, img_wd, img_ht)
    df_3d['MATCH_2D_DIST'] = df_3d.apply(lambda row: compute_match(
        row['PROJ_SCREEN_X'], row['PROJ_SCREEN_Y'],
        df_2d['X'], df_2d['Y'], grid=True)[1], axis=1)
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


def linear_interpolation(point1, point2, n):
    """
    Lindarly interpolate n points between two given points
    :param point1: first given point as Tuple (x1, y1)
    :param point2: second given point as Tuple (x2, y2)
    :param n: number of points in total including interpolated points and the given two end points
    :return: list of tuples representing the interpolated points enclosed by the given two end points
    """
    x1, y1 = point1
    x2, y2 = point2

    # Calculate the step size for interpolation
    step_size = 1.0 / (n - 1)
    print(f'step_size: {step_size}, n: {n}')
    # Perform linear interpolation
    return [(round(x1 + i * step_size * (x2 - x1)), round(y1 + i * step_size * (y2 - y1))) for i in range(0, n)]


def get_mapping_data(input_file, input_image_name):
    df = pd.read_csv(input_file, usecols=['ROUTEID', 'MAPPED_IMAGE', 'LATITUDE', 'LONGITUDE'], dtype=str)
    df.sort_values(by=['ROUTEID', 'MAPPED_IMAGE'], inplace=True, ignore_index=True)

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
    df = pd.read_csv(input_file, dtype=str)
    # make sure only use the front image (ending with 1) for alignment
    # df['imageBaseName'] = df['imageBaseName'].str[:-1] + '1'
    print(f'input df shape: {df.shape}')
    df.drop_duplicates(subset=['imageBaseName'], inplace=True)
    print(f'input df shape after removing duplicates: {df.shape}')
    return df


def get_full_camera_parameters(cam_p):
    if len(cam_p) < len(INIT_CAMERA_PARAMS):
        combined = INIT_CAMERA_PARAMS[:len(INIT_CAMERA_PARAMS)-len(cam_p)]
        combined.extend(cam_p)
    else:
        combined = cam_p
    return combined


def get_updated_z_axis_from_rotation_angles(x_angle, y_angle, z_angle, v_initial):
    rot_mat = Rotation.from_euler('xyz', np.array([x_angle, y_angle, z_angle]), degrees=True).as_matrix()
    return np.dot(rot_mat, v_initial)


def derive_next_camera_params(v1, v2, cam_para1):
    rot_mat1 = Rotation.from_euler('xyz', np.array([cam_para1[CAMERA_ROLL], cam_para1[CAMERA_PITCH],
                                                    cam_para1[CAMERA_YAW]]), degrees=True).as_matrix()

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
    cam_para2[CAMERA_ROLL], cam_para2[CAMERA_PITCH], cam_para2[CAMERA_YAW] = \
        Rotation.from_matrix(rot_mat2).as_euler('xyz', degrees=True)

    return cam_para2


def align_image_to_lidar(row, base_image_dir, ldf, input_mapping_file, out_proj_file_path, is_optimize):
    """
    :param row: the image metadata dataframe row to be processed
    :param base_image_dir: base path in which images are located
    :param ldf: lidar 3D point geodataframe
    :param input_mapping_file: input_mapping_file to read and extract camera location and its next camera location
    for determining bearing direction
    :param out_proj_file_path: output path for aligned road info which will be appended with
    lidar_project_info_{image name} to have lidar projection info for each input image
    :param is_optimize: whether to optimize camera parameter or not
    :return: the computed base camera parameters and optimized camera parameters; if is_optimize is False, optimized
    camera parameters will be an empty list
    """
    global PREV_CAM_PARAS, PREV_CAM_BEARING_VEC

    if len(row["imageBaseName"]) == 11:
        image_name_with_path = os.path.join(base_image_dir, f'{row["imageBaseName"]}1.png')
        # get input image base name
        input_2d_mapped_image = row["imageBaseName"]
    else:
        image_name_with_path = os.path.join(base_image_dir, f'{row["imageBaseName"]}.png')
        # get input image base name
        input_2d_mapped_image = row["imageBaseName"][:-1]

    out_proj_file = os.path.join(out_proj_file_path, f'lidar_project_info_{input_2d_mapped_image}.csv') \
        if is_optimize else os.path.join(out_proj_file_path, f'base_lidar_project_info_{input_2d_mapped_image}.csv')
    print(f'image_name_with_path: {image_name_with_path}, input_2d_mapped_image: {input_2d_mapped_image}')
    lane_image_name = f'{os.path.dirname(image_name_with_path)}/{input_2d_mapped_image}1_lanes.png'
    print(f'lane_image_name: {lane_image_name}')
    img_width, img_height, input_list, intersect_points = get_image_lane_points(lane_image_name)
    input_2d_points = input_list[0]

    # output 2d road boundary points for showing alignment overlay plot
    with open(os.path.join(os.path.dirname(out_proj_file), f'input_2d_{input_2d_mapped_image}.pkl'), 'wb') as f:
        pickle.dump(input_list, f)

    if input_2d_points.shape[1] == 2:
        input_2d_df = pd.DataFrame(data=input_2d_points, columns=['X', 'Y'])
    else:
        print(f'input_2d_points.shape[1] must be 2, but it is {input_2d_points.shape[1]}, exiting')
        exit(1)

    # compute base camera parameters
    cam_lat, cam_lon, proj_cam_x, proj_cam_y, cam_br, cam_lat2, cam_lon2, eor = \
        get_mapping_data(input_mapping_file, input_2d_mapped_image)
    # get the lidar road vertex with the closest distance to the camera location
    cam_nearest_lidar_idx = compute_match(proj_cam_x, proj_cam_y, ldf['X'], ldf['Y'])[0][0]
    # next_idx = get_next_road_index(cam_nearest_lidar_idx, input_3d_gdf, 'BEARING')
    # cam_lidar_z = interpolate_camera_z(input_3d_gdf.iloc[cam_nearest_lidar_idx].Z, input_3d_gdf.iloc[next_idx].Z,
    #                                    dist([input_3d_gdf.iloc[cam_nearest_lidar_idx].X,
    #                                    input_3d_gdf.iloc[cam_nearest_lidar_idx].Y],
    #                                         [proj_cam_x, proj_cam_y]),
    #                                    dist([input_3d_gdf.iloc[next_idx].X, input_3d_gdf.iloc[next_idx].Y],
    #                                         [proj_cam_x, proj_cam_y]))
    cam_lidar_z = ldf.iloc[cam_nearest_lidar_idx].Z
    print(f'camera Z: {cam_lidar_z}')

    vertices, cam_br, cols = extract_lidar_3d_points_for_camera(ldf, [cam_lat, cam_lon], [cam_lat2, cam_lon2],
                                                                dist_th=LIDAR_DIST_THRESHOLD,
                                                                end_of_route=eor)
    input_3d_points = vertices[0]
    print(f'len(input_3d_points): {len(input_3d_points)}, {cols}')
    input_3d_df = pd.DataFrame(data=input_3d_points, columns=cols)

    if 'BOUND' in cols:
        input_3d_df['BOUND'] = input_3d_df['BOUND'].astype(int)

    input_3d_df['X'] = input_3d_df['X'].astype(float)
    input_3d_df['Y'] = input_3d_df['Y'].astype(float)
    input_3d_df['Z'] = input_3d_df['Z'].astype(float)
    if 'C' in cols:
        input_3d_df['C'] = input_3d_df['C'].astype(int)
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
    cam2_nearest_lidar_idx = compute_match(proj_cam_x2, proj_cam_y2, ldf['X'], ldf['Y'])[0][0]
    proj_cam_z2 = ldf.iloc[cam2_nearest_lidar_idx].Z
    cam_v = np.array([proj_cam_x2 - proj_cam_x, proj_cam_y2 - proj_cam_y, proj_cam_z2 - cam_lidar_z])
    cam_v = cam_v / np.linalg.norm(cam_v)

    # fit a spline to the LIDAR road points in the radius of SPLINE_FIT_DIST_THRESHOLD along camera bearing direction
    filtered_road_bound_ldf = input_3d_gdf[input_3d_gdf.BOUND == 1]
    filtered_road_ldf = filtered_road_bound_ldf[filtered_road_bound_ldf.CAM_DIST < SPLINE_FIT_DIST_THRESHOLD]
    if filtered_road_ldf.CAM_DIST.min() > 4:
        # road bound points are too far away from the camera location to be used to compute road tangent
        no_points_for_spline = True
    elif len(filtered_road_ldf) > 4:
        no_points_for_spline = False
        filtered_road_ldf.sort_values(by=['CAM_DIST'], inplace=True)
        x = filtered_road_ldf['X'].values
        y = filtered_road_ldf['Y'].values
        z = filtered_road_ldf['Z'].values
        unique_x, unique_indices = np.unique(x, return_index=True)
        unique_y = y[unique_indices]
        unique_z = z[unique_indices]
        spline_xy = UnivariateSpline(unique_x, unique_y, s=SPLINE_SMOOTHING_FACTOR)
        spline_xz = UnivariateSpline(unique_x, unique_z, s=SPLINE_SMOOTHING_FACTOR)
        cam_tan_x = spline_xy.derivative()(filtered_road_ldf['X'].iloc[0])
        cam_tan_y = spline_xy.derivative()(filtered_road_ldf['Y'].iloc[0])
        cam_tan_z = spline_xz.derivative()(filtered_road_ldf['Z'].iloc[0])
        road_v = np.array([cam_tan_x, cam_tan_y, cam_tan_z])
        road_v = road_v / np.linalg.norm(road_v)
        print(f'cam_v: {cam_v}, road_v: {road_v}, image: {row["imageBaseName"]}, PREV_CAM_VEC: {PREV_CAM_BEARING_VEC}')
    else:
        no_points_for_spline = True

    if no_points_for_spline is True:
        # use camera vector since there are not enough LIDAR road edge points to get the road vector
        prev_v = PREV_CAM_BEARING_VEC['camera']
        v = cam_v
        road_v = np.zeros(3)
        print('use camera vector')

    if PREV_CAM_PARAS is not None:
        if no_points_for_spline is False:
            bet_angle = angle_between(cam_v, road_v)
            if bet_angle < USE_ROAD_TANGENT_ANGLE_THRESHOLD and not np.all(PREV_CAM_BEARING_VEC['road'] == 0):
                prev_v = PREV_CAM_BEARING_VEC['road']
                v = road_v
                print('use road tangent')
            else:
                prev_v = PREV_CAM_BEARING_VEC['camera']
                v = cam_v
                print('use camera vector')
        init_cam_paras = derive_next_camera_params(prev_v, v, PREV_CAM_PARAS)
        print(f'derived camera parameters: {init_cam_paras}')
    else:
        init_cam_paras = INIT_CAMERA_PARAMS

    # update global variables to prepare for the next image row iteration
    PREV_CAM_PARAS = init_cam_paras
    PREV_CAM_BEARING_VEC['camera'] = cam_v
    PREV_CAM_BEARING_VEC['road'] = road_v

    if is_optimize:
        # output base lidar project info to base_lidar_project_info_{image_base_name}.csv file since the base
        # camera orientation/bearing info is updated from the optimized version of its previous image using
        # road tangent info. The optimization is based on updated camera base parameters
        input_3d_gdf = transform_3d_points(input_3d_gdf, init_cam_paras, img_width, img_height)
        input_3d_gdf.to_csv(os.path.join(out_proj_file_path, f'base_lidar_project_info_{row["imageBaseName"]}.csv'),
                            index=False)
        input_3d_road_bound_gdf = input_3d_gdf[input_3d_gdf.BOUND == 1].reset_index(drop=True).copy()
        align_errors = []
        # terminate if gradient norm is less than gtol
        # gtol = 1e-6
        # eps specifies the absolute step size used for numerical approximation of the jacobian via forward
        # differences
        # eps = 0.1
        result = minimize(objective_function_2d, init_cam_paras[2:],
                          args=(input_3d_road_bound_gdf,
                                input_2d_df, img_width, img_height, align_errors),
                          method='Nelder-Mead',
                          options={'maxiter': NUM_ITERATIONS, 'disp': True})
                          # method='SLSQP',
                          # method='TNC',
                          # method='BFGS',
                          # method='CG',
                          # jac=True,
                          # options={'gtol': gtol, 'ftol': gtol, 'eps': eps, 'maxiter': NUM_ITERATIONS, 'disp': True})
        optimized_cam_params = result.x
        print(f'optimizing result for image {input_2d_mapped_image}: {result}')
        print(f'Status: {result.message}, total evaluations: {result.nfev}')
        print(f'alignment errors: {align_errors}')
        print(f'optimized_cam_params for image {image_name_with_path}: {optimized_cam_params}')

        full_optimized_cam_paras = get_full_camera_parameters(optimized_cam_params)
        input_3d_gdf = transform_3d_points(input_3d_gdf, full_optimized_cam_paras,
                                           img_width, img_height)
        # update PREV_CAM_PARAS to be used in the next image row iteration
        PREV_CAM_PARAS = full_optimized_cam_paras
    else:
        optimized_cam_params = []
        input_3d_gdf = transform_3d_points(input_3d_gdf, init_cam_paras, img_width, img_height)
        # update NEXT_CAM_PARAS with next camera's parameter to be used in the next image row iteration

    input_3d_gdf.to_csv(out_proj_file, index=False)
    proj_base, proj_ext = os.path.splitext(out_proj_file)
    if is_optimize:
        # output optimized camera parameter for the image
        cam_para_df = pd.DataFrame(data=[optimized_cam_params.tolist()], columns=['translation_x',
                                                                                  'translation_y',
                                                                                  'translation_z',
                                                                                  'rotation_z',
                                                                                  'rotation_y',
                                                                                  'rotation_x'])
        cam_para_df.to_csv(f'{proj_base}_cam_paras.csv', index=False)
        # output_latlon_from_geometry(input_3d_gdf, 'geometry_y', f'{proj_base}_latlon{proj_ext}')
        # if 'I' in input_3d_gdf.columns:
        #     cr_ldf = input_3d_gdf[input_3d_gdf['I'] > 0].reset_index(drop=True)
        #     output_latlon_from_geometry(cr_ldf, 'geometry_y',
        #                                 f'{proj_base}_crossroad_intersect_latlon{proj_ext}')

    return init_cam_paras, optimized_cam_params


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Process arguments.')
    parser.add_argument('--input_lidar_with_path', type=str,
                        # default='data/d13_route_40001001011/lidar/test_scene_all_raster_10_classified.csv',
                        # default='data/d13_route_40001001011/lidar/route_40001001011_all.csv',
                        default='data/new_test_scene/new_test_scene_all_lidar_with_road_bounds.csv',
                        help='input file that contains road x, y, z vertices from lidar')
    parser.add_argument('--obj_base_image_dir', type=str,
                        # default='data/d13_route_40001001011/oneformer',
                        default='data/new_test_scene/segmentation',
                        help='base directory to retrieve images')
    parser.add_argument('--obj_image_input', type=str,
                        # default='../object_mapping/data/pole_input.csv.rep2',
                        default='../object_mapping/data/new_test_route.csv',
                        help='input csv file that contains image base names with objects detected along with other '
                             'inputs for mapping')
    parser.add_argument('--input_sensor_mapping_file_with_path', type=str,
                        default='data/d13_route_40001001011/other/mapped_2lane_sr_images_d13.csv',
                        help='input csv file that includes mapped image lat/lon info')
    parser.add_argument('--lidar_proj_output_file_path', type=str,
                        # default='data/d13_route_40001001011/oneformer/output/all_lidar_vertices/lidar_project_info',
                        default='data/new_test_scene/lane_test',
                        help='output file base with path for aligned road info which will be appended with image name '
                             'to have lidar projection info for each input image')
    parser.add_argument('--optimize', action="store_true",
                        help='whether to optimize camera parameters')

    args = parser.parse_args()
    input_lidar = args.input_lidar_with_path
    obj_base_image_dir = args.obj_base_image_dir
    obj_image_input = args.obj_image_input
    input_sensor_mapping_file_with_path = args.input_sensor_mapping_file_with_path
    lidar_proj_output_file_path = args.lidar_proj_output_file_path
    optimize = args.optimize

    if input_lidar.endswith('.shp'):
        lidar_df = get_lidar_data_from_shp(input_lidar)
    else:
        lidar_df = get_aerial_lidar_road_geo_df(input_lidar)

    input_df = get_input_file_with_images(obj_image_input)

    start_time = time.time()
    compute_base_cam_paras = False if BASE_CAM_PARA_COL_NAME in input_df.columns else True

    if compute_base_cam_paras:
        # initialize the column with the first camera's base camera parameters
        input_df[BASE_CAM_PARA_COL_NAME] = input_df.apply(lambda _: INIT_CAMERA_PARAMS, axis=1)

    input_df[[BASE_CAM_PARA_COL_NAME, OPTIMIZED_CAM_PARA_COL_NAME]] = input_df.apply(lambda row: align_image_to_lidar(
        row,
        obj_base_image_dir,
        lidar_df,
        input_sensor_mapping_file_with_path,
        lidar_proj_output_file_path,
        optimize), axis=1, result_type='expand')

    input_df.to_csv(f'{os.path.splitext(obj_image_input)[0]}_with_cam_paras.csv', index=False)
    print(f'execution time: {time.time() - start_time}')
