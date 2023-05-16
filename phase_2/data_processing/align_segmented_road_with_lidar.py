import argparse
import os
import pickle
import pandas as pd
import geopandas as gpd
import numpy as np
from math import dist, radians
from utils import get_camera_latlon_and_bearing_for_image_from_mapping, bearing_between_two_latlon_points, \
    get_next_road_index
from extract_lidar_3d_points import get_lidar_data_from_shp, extract_lidar_3d_points_for_camera
from get_road_boundary_points import get_image_road_boundary_points


FOCAL_LENGTH_X = 1.4
FOCAL_LENGTH_Y = 1
# camera translation to move camera along X axis in world coordinate system
CAMERA_LIDAR_X_OFFSET = 6
# camera translation to move camera along Y axis in world coordinate system
CAMERA_LIDAR_Y_OFFSET = 20
# camera translation to move camera along Z axis in world coordinate system
CAMERA_LIDAR_Z_OFFSET = 8
CAMERA_YAW = 5  # camera angle of rotation around Z (bearing) axis in the 3D world coordinate system
CAMERA_PITCH = -2  # camera angle of rotation around Y axis in the 3D world coordinate system
CAMERA_ROLL = -2  # camera angle of rotation around X axis in the 3D world coordinate system


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
    distances = np.sqrt((series_x - x) ** 2 + (series_y - y) ** 2)
    return distances.idxmin()


def transform_to_world_coordinate_system(input_df, cam_x, cam_y, cam_z):
    # transform X, Y, Z in LIDAR coordinate system to world coordinate system where the camera is at the origin,
    # the z-axis is pointing from the camera along the cam_bearing direction, the y-axis is perpendicular to the
    # z-axis reflecting the elevation Z pointing upwards, and the x-axis is perpendicular to both y-axis and z-axis
    # reflecting X and Y. Note that LIDAR world coordinate system origin is located at lower-left corner while
    # screen coordinate system origin is located at upper-left corner
    input_df.X = input_df.X - cam_x
    input_df.Y = input_df.Y - cam_y
    # Calculate the distance between the cam_x, cam_y point and the first two X, Y columns of input_3d_points
    input_df['CAM_DIST'] = np.sqrt(np.square(input_df.X) + np.square(input_df.Y))
    input_df['WORLD_Z'] = input_df.CAM_DIST * np.cos(input_df.BEARING) + CAMERA_LIDAR_Z_OFFSET
    input_df['WORLD_Y'] = input_df.Z - cam_z + CAMERA_LIDAR_Y_OFFSET
    input_df['WORLD_X'] = input_df.CAM_DIST * np.sin(input_df.BEARING) + CAMERA_LIDAR_X_OFFSET
    input_df['WORLD_X'], input_df['WORLD_Y'] = rotate_point_series(input_df['WORLD_X'], input_df['WORLD_Y'], CAMERA_YAW)
    input_df['WORLD_X'], input_df['WORLD_Z'] = rotate_point_series(input_df['WORLD_X'], input_df['WORLD_Z'],
                                                                   CAMERA_PITCH)
    input_df['WORLD_Y'], input_df['WORLD_Z'] = rotate_point_series(input_df['WORLD_Y'], input_df['WORLD_Z'],
                                                                   CAMERA_ROLL)
    return input_df


def align_image_to_lidar(image_name_with_path, ldf, mdf, out_match_file, out_proj_file):
    """
    :param image_name_with_path: image file name with whole path
    :param ldf: lidar 3D point geodataframe
    :param mdf: mapping df to extract camera location and its next camera location for determining bearing direction
    :param out_match_file: file base name for aligned road info which will be appended with image name to
    have an alignment output file for each input image
    :param out_proj_file: output file base with path for aligned road info which will be appended with image name
    to have lidar projection info for each input image
    :return:
    """
    # get input image base name

    input_2d_mapped_image = os.path.basename(image_name_with_path)[:-5]
    img_width, img_height, input_list = get_image_road_boundary_points(image_name_with_path)
    # output 2d road boundary points for showing alignment overlay plot
    with open(os.path.join(os.path.dirname(out_proj_file), f'input_2d_{input_2d_mapped_image}.pkl'), 'wb') as f:
        pickle.dump(input_list, f)
    input_2d_points = input_list[0]
    print(f'input 2d numpy array shape: {input_2d_mapped_image}: {input_2d_points.shape}')
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
    print(f'cam lat-long: {cam_lat}-{cam_lon}, proj cam y-x: {proj_cam_y}-{proj_cam_x}, cam_br: {cam_br}')

    vertices, cam_br = extract_lidar_3d_points_for_camera(ldf, [cam_lat, cam_lon], [cam_lat2, cam_lon2],
                                                          end_of_route=eor)
    input_3d_points = vertices[0]
    print(f'input 3d numpy array shape: {input_3d_points.shape}')
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
    nearest_idx = compute_match(proj_cam_x, proj_cam_y, input_3d_gdf['X'], input_3d_gdf['Y'])
    next_idx = get_next_road_index(nearest_idx, input_3d_gdf, 'BEARING')
    cam_lidar_z = interpolate_camera_z(input_3d_gdf.iloc[nearest_idx].Z, input_3d_gdf.iloc[next_idx].Z,
                                       dist([input_3d_gdf.iloc[nearest_idx].X, input_3d_gdf.iloc[nearest_idx].Y],
                                            [proj_cam_x, proj_cam_y]),
                                       dist([input_3d_gdf.iloc[next_idx].X, input_3d_gdf.iloc[next_idx].Y],
                                            [proj_cam_x, proj_cam_y]))

    print(f'camera Z: {cam_lidar_z}')

    input_3d_gdf = transform_to_world_coordinate_system(input_3d_gdf, proj_cam_x, proj_cam_y, cam_lidar_z)

    # project to 2D camera coordinate system
    input_3d_gdf['PROJ_X'] = input_3d_gdf.apply(
        lambda row: FOCAL_LENGTH_X * row['WORLD_X'] / (row['WORLD_Z'] - FOCAL_LENGTH_X),
        axis=1)
    input_3d_gdf['PROJ_Y'] = input_3d_gdf.apply(
        lambda row: FOCAL_LENGTH_Y * row['WORLD_Y'] / (row['WORLD_Z'] - FOCAL_LENGTH_Y),
        axis=1)
    max_x = max(input_3d_gdf['PROJ_X'])
    min_x = min(input_3d_gdf['PROJ_X'])
    if max_x > 1 or min_x < -1:
        # projected points are out of range, need to reduce FOCAL_LENGTH to make them within (-1, 1) range
        max_val = max(max_x, -min_x)
        update_focal_length = FOCAL_LENGTH_X / max_val
        input_3d_gdf['PROJ_X'] = input_3d_gdf.apply(
            lambda row: update_focal_length * row['WORLD_X'] / row['WORLD_Z'],
            axis=1)
    max_y = max(input_3d_gdf['PROJ_Y'])
    min_y = min(input_3d_gdf['PROJ_Y'])
    if max_y > 1 or min_y < -1:
        # projected points are out of range, need to reduce FOCAL_LENGTH to make them within (-1, 1) range
        max_val = max(max_y, -min_y)
        update_focal_length = FOCAL_LENGTH_Y / max_val
        input_3d_gdf['PROJ_Y'] = input_3d_gdf.apply(
            lambda row: update_focal_length * row['WORLD_Y'] / row['WORLD_Z'],
            axis=1)

    half_width = img_width / 2
    half_height = img_height / 2
    input_3d_gdf['PROJ_SCREEN_X'] = input_3d_gdf['PROJ_X'].apply(
        lambda x: int((x + 1) * half_width))
    input_3d_gdf['PROJ_SCREEN_Y'] = input_3d_gdf['PROJ_Y'].apply(
        lambda y: int((y + 1) * half_height))
    input_2d_df['MATCH_3D_INDEX'] = input_2d_df.apply(lambda row: compute_match(row['X'], row['Y'],
                                                                                input_3d_gdf['PROJ_SCREEN_X'],
                                                                                input_3d_gdf['PROJ_SCREEN_Y']),
                                                      axis=1)
    input_2d_df.drop(columns=['X', 'Y'], inplace=True)
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
                                'oneformer/output/route_batch/road_alignment_with_lidar',
                        help='output file base with path for aligned road info which will be appended with image name '
                             'to have an alignment output file for each input image')
    parser.add_argument('--lidar_proj_output_file_base', type=str,
                        default='/home/hongyi/ncdot-road-safety/phase_2/data_processing/data/d13_route_40001001011/'
                                'oneformer/output/route_batch/lidar_project_info',
                        help='output file base with path for aligned road info which will be appended with image name '
                             'to have lidar projection info for each input image')

    args = parser.parse_args()
    input_lidar_shp_with_path = args.input_lidar_shp_with_path
    obj_base_image_dir = args.obj_base_image_dir
    obj_image_input = args.obj_image_input
    input_sensor_mapping_file_with_path = args.input_sensor_mapping_file_with_path
    output_file_base = args.output_file_base
    lidar_proj_output_file_base = args.lidar_proj_output_file_base

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
    input_df['imageBaseName'].apply(lambda img: align_image_to_lidar(os.path.join(obj_base_image_dir, f'{img}.png'),
                                                                     lidar_df,
                                                                     mapping_df,
                                                                     f'{output_file_base}_{img}.csv',
                                                                     f'{lidar_proj_output_file_base}_{img}.csv'))
