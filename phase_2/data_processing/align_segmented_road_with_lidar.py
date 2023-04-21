import argparse
import pandas as pd
import geopandas as gpd
import numpy as np
import math
from utils import get_camera_latlon_and_bearing_for_image_from_mapping, bearing_between_two_latlon_points, \
    load_pickle_data, IMAGE_HEIGHT

FOCUS_LENGTH = 0.001
CAMERA_LIDAR_Z_OFFSET = 5

def compute_match(x, y, series_x, series_y):
    # compute match indices in (series_x, series_y) pairs based on which point in all points represented in
    # (series_x, series_y) pairs has minimal distance to point(x, y)
    distances = np.sqrt((series_x - x) ** 2 + (series_y - y) ** 2)
    return distances.idxmin()


def transform_to_world_coordinate_system(input_df, cam_x, cam_y, cam_bearing, cam_z):
    # transform X, Y, Z in LIDAR coordinate system to world coordinate system where the camera is at the origin,
    # the z-axis is pointing from the camera along the cam_bearing direction, the y-axis is perpendicular to the
    # z-axis reflecting the elevation Z pointing upwards, and the x-axis is perpendicular to both y-axis and z-axis
    # reflecting X and Y. Note that LIDAR world coordinate system origin is located at lower-left corner while
    # screen coordinate system origin is located at upper-left corner
    input_df.X = input_df.X - cam_x
    input_df.Y = input_df.Y - cam_y
    # Calculate the distance between the cam_x, cam_y point and the first two X, Y columns of input_3d_points
    input_df['CAM_DIST'] = np.sqrt(input_df.X ** 2 + input_df.Y ** 2)
    input_df['WORLD_Z'] = input_df.CAM_DIST * np.cos(input_df.BEARING)
    input_df['WORLD_Y'] = (input_df.Z - cam_z) * np.cos(math.pi - cam_bearing)
    # input_df['WORLD_X'] = input_df.CAM_DIST * np.sin(input_df.BEARING)
    input_df['WORLD_X'] = input_df.X * np.cos(math.pi - cam_bearing) - input_df.Y * np.sin(math.pi - cam_bearing) - 6
    return input_df


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Process arguments.')
    parser.add_argument('--input_3d', type=str,
                        default='data/d13_route_40001001011/oneformer/output/input_3d.pkl',
                        help='input lidar road x, y, z vertices from lidar')
    parser.add_argument('--road_input_with_path', type=str,
                        default='data/d13_route_40001001011/oneformer/output/input_2d.pkl',
                        help='input road boundary pickled 2D point file name with path')
    parser.add_argument('--input_2d_mapped_image', type=str, default='92600542024',
                        help='mapped image name corresponding to the road_input_with_path to get mapped camera info')
    parser.add_argument('--input_sensor_mapping_file_with_path', type=str,
                        default='data/d13_route_40001001011/other/mapped_2lane_sr_images_d13.csv',
                        help='input csv file that includes mapped image lat/lon info')
    parser.add_argument('--image_width', type=int, default=2748, help='image width')
    parser.add_argument('--image_height', type=int, default=2198, help='image height')
    parser.add_argument('--output_file', type=str,
                        default='/home/hongyi/ncdot-road-safety/phase_2/data_processing/data/d13_route_40001001011/'
                                'oneformer/output/road_alignment_with_lidar.csv',
                        help='output file with path for aligned road info')
    parser.add_argument('--lidar_project_output_file', type=str,
                        default='/home/hongyi/ncdot-road-safety/phase_2/data_processing/data/d13_route_40001001011/'
                                'oneformer/output/lidar_project_info.csv',
                        help='output file with path for aligned road info')

    args = parser.parse_args()
    input_3d = args.input_3d
    road_input_with_path = args.road_input_with_path
    input_2d_mapped_image = args.input_2d_mapped_image
    input_sensor_mapping_file_with_path = args.input_sensor_mapping_file_with_path
    image_width = args.image_width
    image_height = args.image_height
    output_file = args.output_file
    lidar_project_output_file = args.lidar_project_output_file

    input_2d_points = load_pickle_data(road_input_with_path)
    print(f'input 2d numpy array shape: {input_2d_points.shape}')
    input_2d_df = pd.DataFrame(data=input_2d_points, columns=['X', 'Y'])

    mapping_df = pd.read_csv(input_sensor_mapping_file_with_path,
                              usecols=['ROUTEID', 'MAPPED_IMAGE', 'LATITUDE', 'LONGITUDE'], dtype=str)
    mapping_df.sort_values(by=['ROUTEID', 'MAPPED_IMAGE'], inplace=True, ignore_index=True)
    cam_lat, cam_lon, cam_br = get_camera_latlon_and_bearing_for_image_from_mapping(mapping_df, input_2d_mapped_image,
                                                                                    is_degree=False)
    if cam_lat is None:
        # no camera location
        print(f'no camera location found for {input_2d_mapped_image}')
        exit(1)
    # LIDAR road vertices in input_3d is in NAD83(2011) / North Carolina (ftUS) CRS with EPSG:6543, and
    # the cam_lat/cam_lon is in WGS84 CRS with EPSG:4326, need to transform cam_lat/cam_lon to the same CRS as
    # input_3d
    mapped_image_df = mapping_df[mapping_df['MAPPED_IMAGE'] == input_2d_mapped_image]
    mapped_image_gdf = gpd.GeoDataFrame(mapped_image_df, geometry=gpd.points_from_xy(mapped_image_df.LONGITUDE,
                                                                                     mapped_image_df.LATITUDE),
                                        crs='EPSG:4326')
    cam_geom_df = mapped_image_gdf.geometry.to_crs(epsg=6543)
    proj_cam_x = cam_geom_df.iloc[0].x
    proj_cam_y = cam_geom_df.iloc[0].y
    print(f'cam lat-long: {cam_lat}-{cam_lon}, proj cam y-x: {proj_cam_y}-{proj_cam_x}, cam_br: {cam_br}')

    input_3d_points = load_pickle_data(input_3d)

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

    # get the lidar road vertex with closest distance to the camera location
    nearest_idx = compute_match(proj_cam_x, proj_cam_y, input_3d_gdf['X'], input_3d_gdf['Y'])

    # approximate lidar z for camera location
    if input_3d_gdf.iloc[nearest_idx+1].Z > input_3d_gdf.iloc[nearest_idx].Z:
        cam_lidar_z = input_3d_gdf.iloc[nearest_idx].Z - CAMERA_LIDAR_Z_OFFSET
    else:
        cam_lidar_z = input_3d_gdf.iloc[nearest_idx].Z + CAMERA_LIDAR_Z_OFFSET
    print(f'camera Z: {cam_lidar_z}')

    input_3d_gdf = transform_to_world_coordinate_system(input_3d_gdf, proj_cam_x, proj_cam_y, cam_br, cam_lidar_z)

    input_3d_gdf['PROJ_X'] = input_3d_gdf.apply(
        lambda row: FOCUS_LENGTH * row['WORLD_X'] / (FOCUS_LENGTH - row['WORLD_Z']),
        axis=1)
    input_3d_gdf['PROJ_Y'] = input_3d_gdf.apply(
        lambda row: FOCUS_LENGTH * row['WORLD_Y'] / (FOCUS_LENGTH - row['WORLD_Z']),
        axis=1)
    # translate lidar road vertices to be centered at the origin along the x-axis
    min_proj_x = min(input_3d_gdf['PROJ_X'])
    max_proj_x = max(input_3d_gdf['PROJ_X'])
    origin_proj_x = min_proj_x + (max_proj_x - min_proj_x) / 2
    input_3d_gdf['PROJ_X'] = input_3d_gdf['PROJ_X'] - origin_proj_x

    min_road_x = min(input_2d_df.X)
    max_road_x = max(input_2d_df.X)
    min_road_y = min(input_2d_df.Y)
    max_road_y = max(input_2d_df.Y)
    range_x = (max_road_x - min_road_x)
    range_y = (max_road_y - min_road_y)
    min_proj_y = min(input_3d_gdf['PROJ_Y'])
    min_proj_x = min(input_3d_gdf['PROJ_X'])
    scale_x = range_x / (max(input_3d_gdf['PROJ_X']) - min_proj_x)
    scale_y = range_y / (max(input_3d_gdf['PROJ_Y']) - min_proj_y)
    input_3d_gdf['PROJ_SCREEN_X'] = input_3d_gdf['PROJ_X'].apply(
        lambda x: int((x - min_proj_x) * scale_x))
    input_3d_gdf['PROJ_SCREEN_Y'] = input_3d_gdf['PROJ_Y'].apply(
        lambda y: int(IMAGE_HEIGHT - (y - min_proj_y) * scale_y))
    input_2d_df['MATCH_3D_INDEX'] = input_2d_df.apply(lambda row: compute_match(row['X'], row['Y'],
                                                                                input_3d_gdf['PROJ_SCREEN_X'],
                                                                                input_3d_gdf['PROJ_SCREEN_Y']),
                                                      axis=1)
    input_2d_df.drop(columns=['X', 'Y'], inplace=True)
    input_2d_df.to_csv(output_file, header=False)

    input_3d_gdf.to_csv(lidar_project_output_file, index=False)
