import argparse
import os
import time
import pickle
import pandas as pd
import geopandas as gpd
import numpy as np
from pypfm import PFMLoader
from scipy.optimize import minimize
from math import dist, radians, tan, atan2, degrees
from sklearn.preprocessing import MinMaxScaler
from utils import get_camera_latlon_and_bearing_for_image_from_mapping, bearing_between_two_latlon_points, \
    get_next_road_index, get_depth_data, get_depth_of_pixel, get_zoe_depth_data, get_zoe_depth_of_pixel, \
    get_aerial_lidar_road_geo_df, compute_match, compute_match_3d
from extract_lidar_3d_points import get_lidar_data_from_shp, extract_lidar_3d_points_for_camera
from get_road_boundary_points import get_image_road_points
from convert_and_classify_aerial_lidar import output_latlon_from_geometry


# indices as constants in the input camera parameter list where CAMERA_LIDAR_X/Y/Z_OFFSET indicate camera
# translation to move camera along X/Y/Z axis in world coordinate system, CMAERA_YAM, CAMERA_PITCH, CAMERA_ROLL
# indicate camera angle of rotation around Z (bearing) axis, Y axis, and X axis, respectively, in the 3D world
# coordinate system
PERSPECTIVE_VFOV = 20
# PERSPECTIVE_VFOV = 25
PERSPECTIVE_NEAR = 0.1
FOCAL_LENGTH_X, FOCAL_LENGTH_Y, CAMERA_LIDAR_X_OFFSET, CAMERA_LIDAR_Y_OFFSET, CAMERA_LIDAR_Z_OFFSET, \
    CAMERA_YAW, CAMERA_PITCH, CAMERA_ROLL = 0, 1, 2, 3, 4, 5, 6, 7
# initial camera parameter list for optimization
# INIT_CAMERA_PARAMS = [2.3, 2.3, 2.4, -8, -15, 0.32, -1.4, -0.77]
# INIT_CAMERA_PARAMS = [2.3, 2.3, 1.7, -8.9, 16, 0.1, -1.8, -0.56]
INIT_CAMERA_PARAMS = [2.8, 2.8, 1.6, -8.3, -3.9, 1.1, -0.91, -0.53]
# gradient descent hyperparameters
NUM_ITERATIONS = 100
DEPTH_SCALING_FACTOR = 189
LIDAR_DIST_THRESHOLD = 60
# LIDAR_DIST_THRESHOLD = 190


def rotate_point_series(v1, v2, angle, axis):
    angle = radians(angle)
    if axis == 'z' or axis == 'x':
        new_v1 = v1 * np.cos(angle) - v2 * np.sin(angle)
        new_v2 = v1 * np.sin(angle) + v2 * np.cos(angle)
    elif axis == 'y':
        new_v1 = v1 * np.cos(angle) + v2 * np.sin(angle)
        new_v2 = -v1 * np.sin(angle) + v2 * np.cos(angle)
    else:
        print('input axis parameter is invalid - it must be x, y, or z')
        return v1, v2
    return new_v1, new_v2


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
    df['WORLD_Z'] = df['INITIAL_WORLD_Z'] + cam_params[CAMERA_LIDAR_Z_OFFSET]
    df['WORLD_Y'] = df['INITIAL_WORLD_Y'] + cam_params[CAMERA_LIDAR_Y_OFFSET]
    df['WORLD_X'] = df['INITIAL_WORLD_X'] + cam_params[CAMERA_LIDAR_X_OFFSET]
    df['WORLD_Y'], df['WORLD_Z'] = rotate_point_series(df['WORLD_Y'], df['WORLD_Z'],
                                                       cam_params[CAMERA_ROLL], 'x')
    df['WORLD_X'], df['WORLD_Z'] = rotate_point_series(df['WORLD_X'], df['WORLD_Z'],
                                                       cam_params[CAMERA_PITCH], 'y')
    df['WORLD_X'], df['WORLD_Y'] = rotate_point_series(df['WORLD_X'], df['WORLD_Y'],
                                                       cam_params[CAMERA_YAW], 'z')

    return df


def apply_matrix4(x, y, z, e, return_axis='x'):
    w = 1 / (e[3] * x + e[7] * y + e[11] * z + e[15])
    new_x = (e[0] * x + e[4] * y + e[8] * z + e[12] ) * w
    new_y = (e[1] * x + e[5] * y + e[9] * z + e[13] ) * w
    new_z = (e[2] * x + e[6] * y + e[10] * z + e[14] ) * w
    if return_axis == 'x':
        return new_x / new_z
    elif return_axis == 'y':
        return new_y / new_z
    else:
        return new_x, new_y, new_z


def transform_3d_points(df, cam_params, img_width, img_hgt):
    df = transform_to_world_coordinate_system(df, cam_params)
    aspect = img_width / img_hgt
    print(f'img_width: {img_width}, img_hgt: {img_hgt}, aspect: {aspect}')
    far = max(df['INITIAL_WORLD_X'].max(), df['INITIAL_WORLD_Y'].max(), df['INITIAL_WORLD_Z'].max()) * 10
    top = PERSPECTIVE_NEAR * tan(radians(0.5 * PERSPECTIVE_VFOV))
    height = 2 * top
    width = aspect * height
    left = -0.5 * width
    right = left + width
    bottom = top - height
    print(f'hfov: {degrees(atan2(width/2, PERSPECTIVE_NEAR)) * 2}')
    x = 2 * PERSPECTIVE_NEAR / (right - left)
    y = 2 * PERSPECTIVE_NEAR / (top - bottom)
    a = (right + left) / (right - left)
    b = (top + bottom) / (top - bottom)
    c = - (far + PERSPECTIVE_NEAR) / (far - PERSPECTIVE_NEAR)
    d = (- 2 * far * PERSPECTIVE_NEAR) / (far - PERSPECTIVE_NEAR)
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
    # df['PROJ_X'] = df.apply(
    #     lambda row: cam_params[FOCAL_LENGTH_X] * row['WORLD_X'] / row['WORLD_Z'],
    #     axis=1)
    # df['PROJ_Y'] = df.apply(
    #     lambda row: cam_params[FOCAL_LENGTH_Y] * row['WORLD_Y'] / row['WORLD_Z'],
    #     axis=1)

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


def objective_function_2d(cam_params, df_3d, df_2d, img_wd, img_ht, align_errors):
    # compute alignment error corresponding to the cam_params using the sum of squared distances between projected
    # LIDAR vertices and the road boundary pixels
    full_cam_params = get_full_camera_parameters(cam_params)
    df_3d = transform_3d_points(df_3d, full_cam_params, img_wd, img_ht)
    if 'Z' in df_2d.columns:
        df_3d['MATCH_2D_DIST'] = df_3d.apply(lambda row: compute_match(
            row['PROJ_SCREEN_X'], row['PROJ_SCREEN_Y'],
            get_2d_road_points_by_z(df_2d[df_2d.Boundary == row['Boundary']], 'Z', row['INITIAL_WORLD_Z'])['X'],
            get_2d_road_points_by_z(df_2d[df_2d.Boundary == row['Boundary']], 'Z', row['INITIAL_WORLD_Z'])['Y'])[1],
                                             axis=1)
    else:
        df_3d['MATCH_2D_DIST'] = df_3d.apply(lambda row: compute_match(
            row['PROJ_SCREEN_X'], row['PROJ_SCREEN_Y'],
            df_2d[df_2d.Boundary == row['Boundary']]['X'],
            df_2d[df_2d.Boundary == row['Boundary']]['Y'])[1],
                                             axis=1)

    alignment_error = df_3d['MATCH_2D_DIST'].sum()/len(df_3d)
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


def get_mapping_data(input_file, input_image_name):
    df = pd.read_csv(input_file,
                             usecols=['ROUTEID', 'MAPPED_IMAGE', 'LATITUDE', 'LONGITUDE'], dtype=str)
    df.sort_values(by=['ROUTEID', 'MAPPED_IMAGE'], inplace=True, ignore_index=True)

    cam_lat, cam_lon, cam_br, cam_lat2, cam_lon2, eor = get_camera_latlon_and_bearing_for_image_from_mapping(
        df, input_image_name, is_degree=False)
    if cam_lat is None:
        # no camera location
        print(f'no camera location found for {input_image_name}')
        exit(1)
    # LIDAR road vertices in input_3d is in NAD83(2011) / North Carolina (ftUS) CRS with EPSG:6543, and
    # the cam_lat/cam_lon is in WGS84 CRS with EPSG:4326, need to transform cam_lat/cam_lon to the same CRS as
    # input_3d
    mapped_image_df = df[df['MAPPED_IMAGE'] == input_image_name]
    mapped_image_gdf = gpd.GeoDataFrame(mapped_image_df, geometry=gpd.points_from_xy(mapped_image_df.LONGITUDE,
                                                                                     mapped_image_df.LATITUDE),
                                        crs='EPSG:4326')
    cam_geom_df = mapped_image_gdf.geometry.to_crs(epsg=6543)
    proj_cam_x = cam_geom_df.iloc[0].x
    proj_cam_y = cam_geom_df.iloc[0].y
    print(f'cam lat-long: {cam_lat}-{cam_lon}, proj cam y-x: {proj_cam_y}-{proj_cam_x}, cam_br: {cam_br}')

    return cam_lat, cam_lon, proj_cam_x, proj_cam_y, cam_br, cam_lat2, cam_lon2, eor


def get_input_file_with_images(input_file):
    # load input file to get the image names for alignment
    df = pd.read_csv(input_file, usecols=['imageBaseName'], dtype=str)
    # make sure only use the front image (ending with 1) for alignment
    df['imageBaseName'] = df['imageBaseName'].str[:-1] + '1'
    print(f'input df shape: {df.shape}')
    df.drop_duplicates(subset=['imageBaseName'], inplace=True)
    print(f'input df shape after removing duplicates: {df.shape}')
    return df


def get_image_depth(depth_filename, image_base_name, idf, wth, hgt, min_dep, max_dep):
    if depth_filename.endswith('.pfm'):
        loader = PFMLoader((wth, hgt), color=False, compress=False)
        input_pfm = get_depth_data(loader, depth_filename.format(
            image_base_name=f'{image_base_name}1'))
        min_depth = input_pfm.min()
        max_depth = input_pfm.max()
        idf['Z'] = idf.apply(lambda row: get_depth_of_pixel(row['Y'], row['X'],
                                                            input_pfm, min_depth, max_depth,
                                                            scaling=DEPTH_SCALING_FACTOR), axis=1)
    elif depth_filename.endswith('.png'):
        input_depth_data = get_zoe_depth_data(depth_filename.format(
            image_base_name=f'{image_base_name}1'))
        idf['Z'] = idf.apply(lambda row: get_zoe_depth_of_pixel(row['Y'], row['X'], input_depth_data), axis=1)
    # scale the estimated depth column Z to match the real LIDAR depth range (min_dep, max_dep)
    min_max_scaler = MinMaxScaler(feature_range=(min_dep, max_dep))
    idf['Z'] = min_max_scaler.fit_transform(idf[['Z']])
    return idf


def get_full_camera_parameters(cam_p):
    if len(cam_p) < len(INIT_CAMERA_PARAMS):
        combined = INIT_CAMERA_PARAMS[:len(INIT_CAMERA_PARAMS)-len(cam_p)]
        combined.extend(cam_p)
    else:
        combined = cam_p
    return combined


def align_image_to_lidar(image_name_with_path, ldf, input_mapping_file, out_match_file, out_proj_file, to_output_csv,
                         align_in_3d, input_depth_filename_pattern, is_optimize, is_road_boundary_only):
    """
    :param image_name_with_path: image file name with whole path
    :param ldf: lidar 3D point geodataframe
    :param input_mapping_file: input_mapping_file to read and extract camera location and its next camera location
    for determining bearing direction
    :param out_match_file: file base name for aligned road info which will be appended with image name to
    have an alignment output file for each input image
    :param out_proj_file: output file base with path for aligned road info which will be appended with image name
    to have lidar projection info for each input image
    :param to_output_csv: whether to output data in csv format for external alignment
    :param align_in_3d: whether to align road in 3D world coordinate system or in 2D screen coordinate system
    :param input_depth_filename_pattern: input depth filename pattern which could end with either pfm indicating
    MiDAS model depth prediction file or png indicating ZoeDepth prediction file
    :param is_optimize: whether to optimize camera parameter or not
    :param is_road_boundary_only: whether to only use road boundary only for alignment
    :return:
    """
    # get input image base name
    input_2d_mapped_image = os.path.basename(image_name_with_path)[:-5]
    img_width, img_height, input_list = get_image_road_points(image_name_with_path, boundary_only=is_road_boundary_only)

    input_2d_points = input_list[0]

    if to_output_csv:
        if input_2d_points.shape[1] == 2:
            np.savetxt(os.path.join(os.path.dirname(out_proj_file), f'input_2d_{input_2d_mapped_image}1.csv'),
                       input_2d_points, delimiter=',', header='X,Y', comments='', fmt='%d')
        elif input_2d_points.shape[1] == 3:
            np.savetxt(os.path.join(os.path.dirname(out_proj_file), f'input_2d_{input_2d_mapped_image}1.csv'),
                       input_2d_points, delimiter=',', header='X,Y,Boundary', comments='', fmt='%d')
        else:
            print(f'input_2d_points.shape[1] must be either 2, or 3, but it is {input_2d_points.shape[1]}, exiting')
            exit(1)
    else:
        # output 2d road boundary points for showing alignment overlay plot
        with open(os.path.join(os.path.dirname(out_proj_file), f'input_2d_{input_2d_mapped_image}.pkl'), 'wb') as f:
            pickle.dump(input_list, f)

    if input_2d_points.shape[1] == 2:
        input_2d_df = pd.DataFrame(data=input_2d_points, columns=['X', 'Y'])
    elif input_2d_points.shape[1] == 3:
        input_2d_df = pd.DataFrame(data=input_2d_points, columns=['X', 'Y', 'Boundary'])
    else:
        print(f'input_2d_points.shape[1] must be either 2, or 3, but it is {input_2d_points.shape[1]}, exiting')
        exit(1)

    cam_lat, cam_lon, proj_cam_x, proj_cam_y, cam_br, cam_lat2, cam_lon2, eor = get_mapping_data(
        input_mapping_file, input_2d_mapped_image)

    vertices, cam_br = extract_lidar_3d_points_for_camera(ldf, [cam_lat, cam_lon], [cam_lat2, cam_lon2],
                                                          dist_th=LIDAR_DIST_THRESHOLD,
                                                          end_of_route=eor)
    input_3d_points = vertices[0]
    print(f'len(input_3d_points): {len(input_3d_points)}')
    # print(f'input 3d numpy array shape: {input_3d_points.shape}')
    if input_3d_points.shape[1] == 4:
        input_3d_df = pd.DataFrame(data=input_3d_points, columns=['X', 'Y', 'Z', 'Boundary'])
    else:
        input_3d_df = pd.DataFrame(data=input_3d_points, columns=['X', 'Y', 'Z'])
    input_3d_gdf = gpd.GeoDataFrame(input_3d_df, geometry=gpd.points_from_xy(input_3d_df.X, input_3d_df.Y),
                                    crs='EPSG:6543')
    input_3d_geom_df = input_3d_gdf.geometry.to_crs(epsg=4326)
    # geom_df is added as a geometry_y column in lidar_df while the initial geometry column is renamed as geometry_x
    input_3d_gdf = input_3d_gdf.merge(input_3d_geom_df, left_index=True, right_index=True)
    # calculate the bearing of each 3D point to the camera
    input_3d_gdf['BEARING'] = input_3d_gdf['geometry_y'].apply(lambda geom: bearing_between_two_latlon_points(
        cam_lat, cam_lon, geom.y, geom.x, is_degree=False))
    input_3d_gdf['BEARING'] = input_3d_gdf['BEARING'] - cam_br

    # get the lidar road vertex with the closest distance to the camera location
    nearest_idx = compute_match(proj_cam_x, proj_cam_y, input_3d_gdf['X'], input_3d_gdf['Y'])[0]
    if is_road_boundary_only:
        next_idx = get_next_road_index(nearest_idx, input_3d_gdf, 'BEARING')
        cam_lidar_z = interpolate_camera_z(input_3d_gdf.iloc[nearest_idx].Z, input_3d_gdf.iloc[next_idx].Z,
                                           dist([input_3d_gdf.iloc[nearest_idx].X, input_3d_gdf.iloc[nearest_idx].Y],
                                                [proj_cam_x, proj_cam_y]),
                                           dist([input_3d_gdf.iloc[next_idx].X, input_3d_gdf.iloc[next_idx].Y],
                                                [proj_cam_x, proj_cam_y]))
    else:
        cam_lidar_z = input_3d_gdf.iloc[nearest_idx].Z

    print(f'camera Z: {cam_lidar_z}')
    input_3d_gdf = init_transform_from_lidar_to_world_coordinate_system(input_3d_gdf, proj_cam_x, proj_cam_y,
                                                                        cam_lidar_z)
    if input_depth_filename_pattern:
        input_2d_df = get_image_depth(input_depth_filename_pattern, input_2d_mapped_image, input_2d_df, img_width,
                                      img_height, input_3d_gdf['INITIAL_WORLD_Z'].min(),
                                      input_3d_gdf['INITIAL_WORLD_Z'].max())
    if align_in_3d and input_depth_filename_pattern:
        input_3d_gdf = transform_to_world_coordinate_system(input_3d_gdf, INIT_CAMERA_PARAMS)
        input_2d_df = transform_2d_points_to_3d(input_2d_df, INIT_CAMERA_PARAMS[FOCAL_LENGTH_X],
                                                INIT_CAMERA_PARAMS[FOCAL_LENGTH_Y], img_width, img_height)
        if road_boundary_only:
            input_2d_df['MATCH_3D_INDEX'] = input_2d_df.apply(lambda row: compute_match_3d(row['X_3D'], row['Y_3D'],
                                                                                           row['Z'],
                                                                                           input_3d_gdf['WORLD_X'],
                                                                                           input_3d_gdf['WORLD_Y'],
                                                                                           input_3d_gdf['WORLD_Z'])[0],
                                                              axis=1)
        else:
            print(f'{input_depth_filename_pattern} is not valid - it must end with .pfm or .png')
            exit(1)

        input_2d_df.to_csv(out_match_file, index=False)
        input_3d_gdf.to_csv(out_proj_file, index=False)
    else:
        if is_optimize:
            align_errors = []
            # terminate if gradient norm is less than gtol
            gtol = 1e-6
            # eps specifies the absolute step size used for numerical approximation of the jacobian via forward differences
            eps = 0.01
            result = minimize(objective_function_2d, INIT_CAMERA_PARAMS[5:],
                              args=(input_3d_gdf, input_2d_df, img_width, img_height, align_errors),
                              method='BFGS',
                              # method='CG',
                              # jac=True,
                              options={'gtol': gtol, 'eps': eps, 'maxiter': NUM_ITERATIONS, 'disp': True})
            optimized_cam_params = result.x
            print(f'optimizing result for image {input_2d_mapped_image}: {result}')
            print(f'alignment errors: {align_errors}')
            print(f'optimized_cam_params: {optimized_cam_params}')
            input_3d_gdf = transform_3d_points(input_3d_gdf, get_full_camera_parameters(optimized_cam_params),
                                               img_width, img_height)
        else:
            input_3d_gdf = transform_3d_points(input_3d_gdf, INIT_CAMERA_PARAMS, img_width, img_height)

        input_3d_gdf['MATCH_2D_INDEX'] = input_3d_gdf.apply(lambda row: compute_match(row['PROJ_SCREEN_X'],
                                                                                      row['PROJ_SCREEN_Y'],
                                                                                      input_2d_df['X'],
                                                                                      input_2d_df['Y'])[0],
                                                            axis=1)
        input_3d_gdf['ROAD_X'] = input_3d_gdf['MATCH_2D_INDEX'].apply(lambda x: input_2d_df.iloc[x]['X'])
        input_3d_gdf['ROAD_Y'] = input_3d_gdf['MATCH_2D_INDEX'].apply(lambda x: input_2d_df.iloc[x]['Y'])
        if to_output_csv:
            input_3d_gdf.to_csv(out_proj_file,
                                columns=['X', 'Y', 'Z', 'INITIAL_WORLD_X', 'INITIAL_WORLD_Y', 'INITIAL_WORLD_Z',
                                         'WORLD_X', 'WORLD_Y', 'WORLD_Z', 'PROJ_X', 'PROJ_Y',
                                         'PROJ_SCREEN_X', 'PROJ_SCREEN_Y'],
                                float_format='%.3f',
                                index=False)
        else:
            input_3d_gdf.to_csv(out_proj_file, index=False)
            proj_base, proj_ext = os.path.splitext(out_proj_file)
            input_3d_gdf.Boundary = input_3d_gdf.Boundary.apply(lambda x: True if x > 0 else False)
            output_latlon_from_geometry(input_3d_gdf, 'geometry_y', f'{proj_base}_latlon{proj_ext}')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Process arguments.')
    parser.add_argument('--input_lidar_with_path', type=str,
                        # default='/home/hongyi/Downloads/NCRouteArcs_and_LiDAR_Road_Edge/'
                        #        'RoadEdge_40001001011_vertices.shp',
                        # default='data/d13_route_40001001011/lidar/test_scene_all_raster_10_classified.csv',
                        default='data/new_test_scene/new_test_scene_road_raster_10_classified.csv',
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
    parser.add_argument('--output_file_base', type=str,
                        # default='data/d13_route_40001001011/oneformer/output/aerial_lidar_test/road_alignment_with_lidar',
                        default='data/new_test_scene/output/road_alignment_with_lidar',
                        help='output file base with path for aligned road info which will be appended with image name '
                             'to have an alignment output file for each input image')
    parser.add_argument('--lidar_proj_output_file_base', type=str,
                        # default='data/d13_route_40001001011/oneformer/output/aerial_lidar_test/lidar_project_info',
                        default='data/new_test_scene/output/lidar_project_info',
                        help='output file base with path for aligned road info which will be appended with image name '
                             'to have lidar projection info for each input image')
    parser.add_argument('--output_2d_3d_points_for_external_alignment', action="store_true",
                        help='output 2d road edge boundary pixels and 3d lidar points in world coordinate system for '
                             'alignment using external tools')
    parser.add_argument('--input_depth_image_filename_pattern', type=str,
                        help='the image pfm depth file pattern with image_base_name to be passed in via string format '
                             'or the zoedepth predicted depth file pattern',
                        # default='../midas/images/output/d13_route_40001001011/{image_base_name}-dpt_beit_large_512.pfm')
                        # default='data/d13_route_40001001011/zoedepth_output/m12_nk/{image_base_name}.png')
                        default='')
    parser.add_argument('--align_road_in_3d', action="store_true",
                        help='align road in 3D world coordinate system by projecting road boundary pixels to 3D '
                             'world coordinate system using predicted depth')
    parser.add_argument('--optimize', action="store_true",
                        help='whether to optimize camera parameters')

    args = parser.parse_args()
    input_lidar = args.input_lidar_with_path
    obj_base_image_dir = args.obj_base_image_dir
    obj_image_input = args.obj_image_input
    input_sensor_mapping_file_with_path = args.input_sensor_mapping_file_with_path
    output_file_base = args.output_file_base
    lidar_proj_output_file_base = args.lidar_proj_output_file_base
    output_2d_3d_points_for_external_alignment = args.output_2d_3d_points_for_external_alignment
    input_depth_image_filename_pattern = args.input_depth_image_filename_pattern
    align_road_in_3d = args.align_road_in_3d
    optimize = args.optimize

    road_boundary_only = True
    if input_lidar.endswith('.shp'):
        lidar_df = get_lidar_data_from_shp(input_lidar)
    else:
        lidar_df = get_aerial_lidar_road_geo_df(input_lidar)
        road_boundary_only = False

    input_df = get_input_file_with_images(obj_image_input)
    start_time = time.time()
    input_df['imageBaseName'].apply(lambda img: align_image_to_lidar(os.path.join(obj_base_image_dir, f'{img}.png'),
                                                                     lidar_df,
                                                                     input_sensor_mapping_file_with_path,
                                                                     f'{output_file_base}_{img}.csv',
                                                                     f'{lidar_proj_output_file_base}_{img}.csv',
                                                                     output_2d_3d_points_for_external_alignment,
                                                                     align_road_in_3d,
                                                                     input_depth_image_filename_pattern, optimize,
                                                                     road_boundary_only))
    print(f'execution time: {time.time() - start_time}')
