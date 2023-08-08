import argparse
import os
import time
import pickle
import pandas as pd
import geopandas as gpd
import numpy as np
from pypfm import PFMLoader
from scipy.optimize import minimize
from math import dist, radians
from utils import get_camera_latlon_and_bearing_for_image_from_mapping, bearing_between_two_latlon_points, \
    get_next_road_index, get_depth_data, get_depth_of_pixel
from extract_lidar_3d_points import get_lidar_data_from_shp, extract_lidar_3d_points_for_camera
from get_road_boundary_points import get_image_road_points


# indices as constants in the input camera parameter list where CAMERA_LIDAR_X/Y/Z_OFFSET indicate camera
# translation to move camera along X/Y/Z axis in world coordinate system, CMAERA_YAM, CAMERA_PITCH, CAMERA_ROLL
# indicate camera angle of rotation around Z (bearing) axis, Y axis, and X axis, respectively, in the 3D world
# coordinate system
FOCAL_LENGTH_X, FOCAL_LENGTH_Y, CAMERA_LIDAR_X_OFFSET, CAMERA_LIDAR_Y_OFFSET, CAMERA_LIDAR_Z_OFFSET, \
    CAMERA_YAW, CAMERA_PITCH, CAMERA_ROLL = 0, 1, 2, 3, 4, 5, 6, 7
# initial camera parameter list for optimization
INIT_CAMERA_PARAMS = [1.4, 1, 6, 20, 8, 5, -2, -2]
# gradient descent hyperparameters
NUM_ITERATIONS = 100
DEPTH_SCALING_FACTOR = 189
LIDAR_DIST_THRESHOLD = 60

def rotate_point_series(x, y, angle):
    angle = radians(angle)
    new_x = x * np.cos(angle) - y * np.sin(angle)
    new_y = x * np.sin(angle) + y * np.cos(angle)
    return new_x, new_y


def interpolate_camera_z(p1_z, p2_z, p1_dist, p2_dist):
    """
    interpolate camera z value based on camera's closet points on one side of the road, (p1_dist, p1_z) and
    (p2_dist, p2_z) where p_dist is the distance from the point to camera and p_z is the LIDAR Z value
    """
    return p1_z - p1_dist * (p2_z - p1_z) / (p2_dist - p1_dist)


def compute_match(x, y, series_x, series_y):
    # compute match indices in (series_x, series_y) pairs based on which point in all points represented in
    # (series_x, series_y) pairs has minimal distance to point(x, y)
    distances = (series_x - x) ** 2 + (series_y - y) ** 2
    min_idx = distances.idxmin()
    return [min_idx, distances[min_idx]]


def compute_match_3d(x, y, z, series_x, series_y, series_z):
    # compute match indices in (series_x, series_y, series_z) based on which point in all points represented in
    # (series_x, series_y, series_z) has minimal distance to point(x, y, z)
    distances = (series_x - x) ** 2 + (series_y - y) ** 2 + (series_z - z) ** 2
    min_idx = distances.idxmin()
    return [min_idx, distances[min_idx]]


def init_transform_from_lidar_to_world_coordinate_system(df, cam_x, cam_y, cam_z):
    # transform LIDAR points from LIDAR projection coordinate system to world coordinate system without
    # considering camera pose parameters
    df['UPDATE_X'] = df.X - cam_x
    df['UPDATE_Y'] = df.Y - cam_y
    # Calculate the distance between the cam_x, cam_y point and the first two X, Y columns of input_3d_points
    df['CAM_DIST'] = np.sqrt(np.square(df.UPDATE_X) + np.square(df.UPDATE_Y))
    df['INITIAL_WORLD_Z'] = df.CAM_DIST * np.cos(df.BEARING)
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
    df['WORLD_X'], df['WORLD_Y'] = rotate_point_series(df['WORLD_X'], df['WORLD_Y'],
                                                       cam_params[CAMERA_YAW])
    df['WORLD_X'], df['WORLD_Z'] = rotate_point_series(df['WORLD_X'], df['WORLD_Z'],
                                                       cam_params[CAMERA_PITCH])
    df['WORLD_Y'], df['WORLD_Z'] = rotate_point_series(df['WORLD_Y'], df['WORLD_Z'],
                                                       cam_params[CAMERA_ROLL])
    return df


def transform_3d_points(df, cam_params, img_width, img_hgt):
    df = transform_to_world_coordinate_system(df, cam_params)

    # project to 2D camera coordinate system
    df['PROJ_X'] = df.apply(
        lambda row: cam_params[FOCAL_LENGTH_X] * row['WORLD_X'] / (row['WORLD_Z'] - cam_params[FOCAL_LENGTH_X]),
        axis=1)
    df['PROJ_Y'] = df.apply(
        lambda row: cam_params[FOCAL_LENGTH_Y] * row['WORLD_Y'] / (row['WORLD_Z'] - cam_params[FOCAL_LENGTH_Y]),
        axis=1)
    # max_x = max(df['PROJ_X'])
    # min_x = min(df['PROJ_X'])
    # if max_x > 1 or min_x < -1:
    #     # projected points are out of range, need to reduce FOCAL_LENGTH to make them within (-1, 1) range
    #     max_val = max(max_x, -min_x)
    #     update_focal_length = cam_params[FOCAL_LENGTH_X] / max_val
    #     print(f'min_x-max_x: {min_x}-{max_x}, reduced focal length from {cam_params[FOCAL_LENGTH_X]} to '
    #           f'{update_focal_length}')
    #     df['PROJ_X'] = df.apply(
    #         lambda row: update_focal_length * row['WORLD_X'] / row['WORLD_Z'],
    #         axis=1)
    # max_y = max(df['PROJ_Y'])
    # min_y = min(df['PROJ_Y'])
    # if max_y > 1 or min_y < -1:
    #     # projected points are out of range, need to reduce FOCAL_LENGTH to make them within (-1, 1) range
    #     max_val = max(max_y, -min_y)
    #     update_focal_length = cam_params[FOCAL_LENGTH_Y] / max_val
    #     print(f'min_y-max_y: {min_y}-{max_y}, reduced focal length from {cam_params[FOCAL_LENGTH_Y]} to '
    #           f'{update_focal_length}')
    #     df['PROJ_Y'] = df.apply(
    #         lambda row: update_focal_length * row['WORLD_Y'] / row['WORLD_Z'],
    #         axis=1)

    half_width = img_width / 2
    half_height = img_hgt / 2
    df['PROJ_SCREEN_X'] = df['PROJ_X'].apply(
        lambda x: int((x + 1) * half_width))
    df['PROJ_SCREEN_Y'] = df['PROJ_Y'].apply(
        lambda y: int((y + 1) * half_height))
    return df


def objective_function_2d(cam_params, df_3d, df_2d, img_wd, img_ht, align_errors):
    # compute alignment error corresponding to the cam_params using the sum of squared distances between projected
    # LIDAR vertices and the road boundary pixels
    df_3d = transform_3d_points(df_3d, cam_params, img_wd, img_ht)
    df_3d['MATCH_2D_DIST'] = df_3d.apply(lambda row: compute_match(row['PROJ_SCREEN_X'], row['PROJ_SCREEN_Y'],
                                                                   df_2d['X'], df_2d['Y'])[1],
                                         axis=1)
    # df_3d['MATCH_2D_INDEX'] = df_3d.apply(lambda row: compute_match(row['PROJ_SCREEN_X'], row['PROJ_SCREEN_Y'],
    #                                                                 df_2d['X'], df_2d['Y'])[0],
    #                                       axis=1)
    # df_3d['MATCH_2D_X_DIST'] = df_3d.apply(lambda row: (row['PROJ_SCREEN_X'] -
    #                                                     df_2d.iloc[row['MATCH_2D_INDEX']]['X']) ** 2, axis=1)
    # df_3d['MATCH_2D_Y_DIST'] = df_3d.apply(lambda row: (row['PROJ_SCREEN_Y'] -
    #                                                     df_2d.iloc[row['MATCH_2D_INDEX']]['Y']) ** 2, axis=1)
    # df_3d['MATCH_2D_DIST'] = df_3d['MATCH_2D_X_DIST'] + df_3d['MATCH_2D_Y_DIST']
    # df_2d['MATCH_3D_DIST'] = df_2d.apply(lambda row: compute_match(row['X'], row['Y'],
    #                                                                df_3d['PROJ_SCREEN_X'], df_3d['PROJ_SCREEN_Y'])[1],
    #                                      axis=1)
    # alignment_error = df_2d['MATCH_3D_DIST'].sum() / len(df_2d)
    alignment_error = df_3d['MATCH_2D_DIST'].sum()/len(df_3d)
    align_errors.append(alignment_error)
    # print(f'cam_params: {cam_params}, alignment error: {alignment_error}')
    # # compute gradients
    # der = np.zeros_like(cam_params)
    # half_width = img_wd / 2
    # half_ht = img_ht / 2
    # ratio = 2 / len(df_3d)
    # der[FOCAL_LENGTH_X] = ratio * np.sum(half_width * df_3d['MATCH_2D_X_DIST'] * df_3d['WORLD_X'] / df_3d['WORLD_Z'])
    # der[FOCAL_LENGTH_Y] = ratio * np.sum(half_ht * df_3d['MATCH_2D_Y_DIST'] * df_3d['WORLD_Y'] / df_3d['WORLD_Z'])
    # # translation derivates may need to be further refined since WORLD_Z is dependent on WORLD_X via rotations
    # der[CAMERA_LIDAR_X_OFFSET] = ratio * np.sum(half_width * df_3d['MATCH_2D_X_DIST'] * cam_params[FOCAL_LENGTH_X] *
    #                                             np.cos(radians(cam_params[CAMERA_PITCH])) *
    #                                             np.cos(radians(cam_params[CAMERA_YAW])) / df_3d['WORLD_Z'])
    # der[CAMERA_LIDAR_Y_OFFSET] = ratio * np.sum(half_ht * df_3d['MATCH_2D_Y_DIST'] * cam_params[FOCAL_LENGTH_Y] *
    #                                             np.cos(radians(cam_params[CAMERA_ROLL])) *
    #                                             np.cos(radians(cam_params[CAMERA_YAW])) / df_3d['WORLD_Z'])
    # # use quotient role to compute derivative of cost function relative to CAMERA_LIDAR_Z_OFFSET reflected in WORLD_Z
    # constants_num = half_width * cam_params[FOCAL_LENGTH_X] * df_3d['WORLD_X'] * \
    #     np.cos(radians(cam_params[CAMERA_ROLL])) * np.cos(radians(cam_params[CAMERA_PITCH]))
    # constants_dem = (df_3d['WORLD_Y'] * np.sin(radians(cam_params[CAMERA_ROLL])) +
    #                  np.cos(radians(cam_params[CAMERA_ROLL])) *
    #                  (df_3d['WORLD_X'] * np.sin(radians(cam_params[CAMERA_PITCH])) +
    #                   (df_3d['CAM_DIST'] * np.cos(df_3d['BEARING']) + cam_params[CAMERA_LIDAR_Z_OFFSET]) *
    #                  np.cos(radians(cam_params[CAMERA_PITCH])))) ** 2
    # der[CAMERA_LIDAR_Z_OFFSET] = ratio * np.sum(df_3d['MATCH_2D_X_DIST'] * (constants_num / constants_dem))
    # der[CAMERA_YAW] = ratio * np.sum(df_3d['MATCH_2D_X_DIST'] *
    #                                  (-half_width * cam_params[FOCAL_LENGTH_X] *
    #                                   (df_3d['WORLD_X'] * np.sin(radians(cam_params[CAMERA_YAW])) +
    #                                    df_3d['WORLD_Y'] * np.cos(radians(cam_params[CAMERA_YAW])))) +
    #                                  df_3d['MATCH_2D_Y_DIST'] * half_ht * cam_params[FOCAL_LENGTH_Y] *
    #                                  (df_3d['WORLD_X'] * np.cos(radians(cam_params[CAMERA_YAW])) -
    #                                   df_3d['WORLD_Y'] * np.sin(radians(cam_params[CAMERA_YAW]))))
    # der_pitch = (-df_3d['WORLD_X'] * np.sin(radians(cam_params[CAMERA_PITCH])) +
    #              df_3d['WORLD_Z'] * np.cos(radians(cam_params[CAMERA_PITCH]))) * \
    #     (df_3d['WORLD_X'] * np.sin(radians(cam_params[CAMERA_PITCH])) +
    #      df_3d['WORLD_Z'] * np.cos(radians(cam_params[CAMERA_PITCH]))) - \
    #     (df_3d['WORLD_X'] * np.cos(radians(cam_params[CAMERA_PITCH])) -
    #      df_3d['WORLD_Z'] * np.sin(radians(cam_params[CAMERA_PITCH]))) * \
    #     (df_3d['WORLD_X'] * np.cos(radians(cam_params[CAMERA_PITCH])) -
    #      df_3d['WORLD_Z'] * np.sin(radians(cam_params[CAMERA_PITCH]))) / \
    #             (df_3d['WORLD_X'] * np.sin(radians(cam_params[CAMERA_PITCH])) +
    #              df_3d['WORLD_Z'] * np.cos(radians(cam_params[CAMERA_PITCH]))) ** 2
    # der[CAMERA_PITCH] = ratio * np.sum(df_3d['MATCH_2D_X_DIST'] * half_width * cam_params[FOCAL_LENGTH_X] * der_pitch)
    # der_roll = (-df_3d['WORLD_Y'] * np.sin(radians(cam_params[CAMERA_ROLL])) +
    #             df_3d['WORLD_Z'] * np.cos(radians(cam_params[CAMERA_ROLL]))) * \
    #     (df_3d['WORLD_Y'] * np.sin(radians(cam_params[CAMERA_ROLL])) +
    #      df_3d['WORLD_Z'] * np.cos(radians(cam_params[CAMERA_ROLL]))) - \
    #     (df_3d['WORLD_Y'] * np.cos(radians(cam_params[CAMERA_ROLL])) -
    #      df_3d['WORLD_Z'] * np.sin(radians(cam_params[CAMERA_ROLL]))) * \
    #     (df_3d['WORLD_Y'] * np.cos(radians(cam_params[CAMERA_ROLL])) -
    #      df_3d['WORLD_Z'] * np.sin(radians(cam_params[CAMERA_ROLL]))) / \
    #             (df_3d['WORLD_Y'] * np.sin(radians(cam_params[CAMERA_ROLL])) +
    #              df_3d['WORLD_Z'] * np.cos(radians(cam_params[CAMERA_ROLL]))) ** 2
    # der[CAMERA_ROLL] = ratio * np.sum(df_3d['MATCH_2D_X_DIST'] * half_ht * cam_params[FOCAL_LENGTH_Y] * der_roll)
    # return alignment_error, der
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


def align_image_to_lidar(image_name_with_path, ldf, mdf, out_match_file, out_proj_file, to_output_csv, align_in_3d,
                         input_depth_filename_pattern):
    """
    :param image_name_with_path: image file name with whole path
    :param ldf: lidar 3D point geodataframe
    :param mdf: mapping df to extract camera location and its next camera location for determining bearing direction
    :param out_match_file: file base name for aligned road info which will be appended with image name to
    have an alignment output file for each input image
    :param out_proj_file: output file base with path for aligned road info which will be appended with image name
    to have lidar projection info for each input image
    :param to_output_csv: whether to output data in csv format for external alignment
    :param align_in_3d: whether to align road in 3D world coordinate system or in 2D screen coordinate system
    :return:
    """
    # get input image base name

    input_2d_mapped_image = os.path.basename(image_name_with_path)[:-5]
    img_width, img_height, input_list = get_image_road_points(image_name_with_path)

    input_2d_points = input_list[0]
    # print(f'input 2d numpy array shape: {input_2d_mapped_image}: {input_2d_points.shape}')
    if to_output_csv:
        np.savetxt(os.path.join(os.path.dirname(out_proj_file), f'input_2d_{input_2d_mapped_image}1.csv'),
                   input_2d_points, delimiter=',', header='X,Y', comments='', fmt='%d')
    else:
        # output 2d road boundary points for showing alignment overlay plot
        with open(os.path.join(os.path.dirname(out_proj_file), f'input_2d_{input_2d_mapped_image}.pkl'), 'wb') as f:
            pickle.dump(input_list, f)

    input_2d_df = pd.DataFrame(data=input_2d_points, columns=['X', 'Y'])
    cam_lat, cam_lon, cam_br, cam_lat2, cam_lon2, eor = get_camera_latlon_and_bearing_for_image_from_mapping(
        mdf, input_2d_mapped_image, is_degree=False)
    if cam_lat is None:
        # no camera location
        print(f'no camera location found for {input_2d_mapped_image}')
        exit(1)
    # LIDAR road vertices in input_3d is in NAD83(2011) / North Carolina (ftUS) CRS with EPSG:6543, and
    # the cam_lat/cam_lon is in WGS84 CRS with EPSG:4326, need to transform cam_lat/cam_lon to the same CRS as
    # input_3d
    mapped_image_df = mdf[mdf['MAPPED_IMAGE'] == input_2d_mapped_image]
    mapped_image_gdf = gpd.GeoDataFrame(mapped_image_df, geometry=gpd.points_from_xy(mapped_image_df.LONGITUDE,
                                                                                     mapped_image_df.LATITUDE),
                                        crs='EPSG:4326')
    cam_geom_df = mapped_image_gdf.geometry.to_crs(epsg=6543)
    proj_cam_x = cam_geom_df.iloc[0].x
    proj_cam_y = cam_geom_df.iloc[0].y
    # print(f'cam lat-long: {cam_lat}-{cam_lon}, proj cam y-x: {proj_cam_y}-{proj_cam_x}, cam_br: {cam_br}')

    vertices, cam_br = extract_lidar_3d_points_for_camera(ldf, [cam_lat, cam_lon], [cam_lat2, cam_lon2],
                                                          dist_th=LIDAR_DIST_THRESHOLD,
                                                          end_of_route=eor)
    input_3d_points = vertices[0]
    print(f'len(input_3d_points): {len(input_3d_points)}')
    # print(f'input 3d numpy array shape: {input_3d_points.shape}')
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
    next_idx = get_next_road_index(nearest_idx, input_3d_gdf, 'BEARING')
    cam_lidar_z = interpolate_camera_z(input_3d_gdf.iloc[nearest_idx].Z, input_3d_gdf.iloc[next_idx].Z,
                                       dist([input_3d_gdf.iloc[nearest_idx].X, input_3d_gdf.iloc[nearest_idx].Y],
                                            [proj_cam_x, proj_cam_y]),
                                       dist([input_3d_gdf.iloc[next_idx].X, input_3d_gdf.iloc[next_idx].Y],
                                            [proj_cam_x, proj_cam_y]))

    # print(f'camera Z: {cam_lidar_z}')
    input_3d_gdf = init_transform_from_lidar_to_world_coordinate_system(input_3d_gdf, proj_cam_x, proj_cam_y,
                                                                        cam_lidar_z)
    if align_in_3d:
        input_3d_gdf = transform_to_world_coordinate_system(input_3d_gdf, INIT_CAMERA_PARAMS)
        loader = PFMLoader((img_width, img_height), color=False, compress=False)
        input_pfm = get_depth_data(loader, input_depth_filename_pattern.format(
            image_base_name=f'{input_2d_mapped_image}1'))
        min_depth = input_pfm.min()
        max_depth = input_pfm.max()
        input_2d_df['Z'] = input_2d_df.apply(lambda row: get_depth_of_pixel(row['Y'], row['X'],
                                                                            input_pfm, min_depth, max_depth,
                                                                            scaling=DEPTH_SCALING_FACTOR), axis=1)
        input_2d_df = transform_2d_points_to_3d(input_2d_df, INIT_CAMERA_PARAMS[FOCAL_LENGTH_X],
                                                INIT_CAMERA_PARAMS[FOCAL_LENGTH_Y], img_width, img_height)
        input_2d_df['MATCH_3D_INDEX'] = input_2d_df.apply(lambda row: compute_match_3d(row['X_3D'], row['Y_3D'],
                                                                                       row['Z'],
                                                                                       input_3d_gdf['WORLD_X'],
                                                                                       input_3d_gdf['WORLD_Y'],
                                                                                       input_3d_gdf['WORLD_Z'])[0],
                                                          axis=1)
        input_2d_df.to_csv(out_match_file, index=False)
        input_3d_gdf.to_csv(out_proj_file, index=False)
    else:
        align_errors = []
        # terminate if gradient norm is less than gtol
        gtol = 1e-6
        # eps specifies the absolute step size used for numerical approximation of the jacobian via forward differences
        eps = 0.01
        result = minimize(objective_function_2d, INIT_CAMERA_PARAMS,
                          args=(input_3d_gdf, input_2d_df, img_width, img_height, align_errors),
                          method='BFGS',
                          # method='CG',
                          # jac=True,
                          options={'gtol': gtol, 'eps': eps, 'maxiter': NUM_ITERATIONS, 'disp': True})
        optimized_cam_params = result.x
        updated_eps = eps
        while (optimized_cam_params[0] < INIT_CAMERA_PARAMS[0]/2 or optimized_cam_params[1] < INIT_CAMERA_PARAMS[1]/2) \
                and (updated_eps > 1e-8):
            # if focal length along X and/or Y is too small, the result is not acceptable, reducing eps and trying again
            print(f'focal length too small: {optimized_cam_params} for image {input_2d_mapped_image}, '
                  f'reduce eps and try again.')
            updated_eps = updated_eps/10.0
            result = minimize(objective_function_2d, INIT_CAMERA_PARAMS,
                              args=(input_3d_gdf, input_2d_df, img_width, img_height, align_errors),
                              method='BFGS',
                              # method='CG',
                              # jac=True,
                              options={'gtol': gtol, 'eps': updated_eps, 'maxiter': NUM_ITERATIONS, 'disp': True})
            optimized_cam_params = result.x
        print(f'optimizing result for image {input_2d_mapped_image}: {result}')
        print(f'alignment errors: {align_errors}')
        print(f'optimized_cam_params: {optimized_cam_params}')
        # input_3d_gdf = transform_3d_points(input_3d_gdf, optimized_cam_params, img_width, img_height)
        input_3d_gdf = transform_3d_points(input_3d_gdf, INIT_CAMERA_PARAMS, img_width, img_height)

        input_2d_df['MATCH_3D_INDEX'] = input_2d_df.apply(lambda row: compute_match(row['X'], row['Y'],
                                                                                    input_3d_gdf['PROJ_SCREEN_X'],
                                                                                    input_3d_gdf['PROJ_SCREEN_Y'])[0],
                                                          axis=1)
        input_2d_df.drop(columns=['X', 'Y'], inplace=True)
        if to_output_csv:
            input_3d_gdf.to_csv(out_proj_file,
                                columns=['X', 'Y', 'Z', 'INITIAL_WORLD_X', 'INITIAL_WORLD_Y', 'INITIAL_WORLD_Z',
                                         'WORLD_X', 'WORLD_Y', 'WORLD_Z', 'PROJ_X', 'PROJ_Y',
                                         'PROJ_SCREEN_X', 'PROJ_SCREEN_Y'],
                                float_format='%.3f',
                                index=False)
        else:
            input_2d_df.to_csv(out_match_file, header=False)
            input_3d_gdf.to_csv(out_proj_file, index=False)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Process arguments.')
    parser.add_argument('--input_lidar_shp_with_path', type=str,
                        default='/home/hongyi/Downloads/NCRouteArcs_and_LiDAR_Road_Edge/'
                                'RoadEdge_40001001011_vertices.shp',
                        help='input shp file that contains road x, y, z vertices from lidar')
    parser.add_argument('--obj_base_image_dir', type=str,
                        default='data/d13_route_40001001011/oneformer',
                        help='base directory to retrieve images')
    parser.add_argument('--obj_image_input', type=str,
                        default='../object_mapping/data/pole_input.csv',
                        help='input csv file that contains image base names with objects detected along with other '
                             'inputs for mapping')
    parser.add_argument('--input_sensor_mapping_file_with_path', type=str,
                        default='data/d13_route_40001001011/other/mapped_2lane_sr_images_d13.csv',
                        help='input csv file that includes mapped image lat/lon info')
    parser.add_argument('--output_file_base', type=str,
                        default='/home/hongyi/ncdot-road-safety/phase_2/data_processing/data/d13_route_40001001011/'
                                'oneformer/output/route_batch_3d/road_alignment_with_lidar',
                        help='output file base with path for aligned road info which will be appended with image name '
                             'to have an alignment output file for each input image')
    parser.add_argument('--lidar_proj_output_file_base', type=str,
                        default='/home/hongyi/ncdot-road-safety/phase_2/data_processing/data/d13_route_40001001011/'
                                'oneformer/output/route_batch_3d/lidar_project_info',
                        help='output file base with path for aligned road info which will be appended with image name '
                             'to have lidar projection info for each input image')
    parser.add_argument('--output_2d_3d_points_for_external_alignment', action="store_true",
                        help='output 2d road edge boundary pixels and 3d lidar points in world coordinate system for '
                             'alignment using external tools')
    parser.add_argument('--input_depth_image_filename_pattern', type=str,
                        help='the image pfm depth file pattern with image_base_name to be passed in via string format',
                        default='../midas/images/output/d13_route_40001001011/{image_base_name}-dpt_beit_large_512.pfm')
    parser.add_argument('--align_road_in_3d', action="store_true",
                        help='align road in 3D world coordinate system by projecting road boundary pixels to 3D '
                             'world coordinate system using predicted depth')

    args = parser.parse_args()
    input_lidar_shp_with_path = args.input_lidar_shp_with_path
    obj_base_image_dir = args.obj_base_image_dir
    obj_image_input = args.obj_image_input
    input_sensor_mapping_file_with_path = args.input_sensor_mapping_file_with_path
    output_file_base = args.output_file_base
    lidar_proj_output_file_base = args.lidar_proj_output_file_base
    output_2d_3d_points_for_external_alignment = args.output_2d_3d_points_for_external_alignment
    align_road_in_3d = args.align_road_in_3d
    input_depth_image_filename_pattern = args.input_depth_image_filename_pattern

    lidar_df = get_lidar_data_from_shp(input_lidar_shp_with_path)

    mapping_df = pd.read_csv(input_sensor_mapping_file_with_path,
                             usecols=['ROUTEID', 'MAPPED_IMAGE', 'LATITUDE', 'LONGITUDE'], dtype=str)
    mapping_df.sort_values(by=['ROUTEID', 'MAPPED_IMAGE'], inplace=True, ignore_index=True)

    # load input file to get the image names for alignment
    input_df = pd.read_csv(obj_image_input, usecols=['imageBaseName'], dtype=str)
    # make sure only use the front image (ending with 1) for alignment
    input_df['imageBaseName'] = input_df['imageBaseName'].str[:-1] + '1'
    print(f'input df shape: {input_df.shape}')
    input_df.drop_duplicates(subset=['imageBaseName'], inplace=True)
    print(f'input df shape after removing duplicates: {input_df.shape}')
    start_time = time.time()
    input_df['imageBaseName'].apply(lambda img: align_image_to_lidar(os.path.join(obj_base_image_dir, f'{img}.png'),
                                                                     lidar_df,
                                                                     mapping_df,
                                                                     f'{output_file_base}_{img}.csv',
                                                                     f'{lidar_proj_output_file_base}_{img}.csv',
                                                                     output_2d_3d_points_for_external_alignment,
                                                                     align_road_in_3d,
                                                                     input_depth_image_filename_pattern))
    print(f'execution time: {time.time() - start_time}')
