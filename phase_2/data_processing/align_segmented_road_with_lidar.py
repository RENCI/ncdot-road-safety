import argparse
import pandas as pd
import geopandas as gpd
import numpy as np
import pickle
from utils import get_camera_latlon_and_bearing_for_image_from_mapping, bearing_between_two_latlon_points


FOCAL_LENGTH = 1.4

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
    parser.add_argument('--output_file', type=str,
                        default='/home/hongyi/ncdot-road-safety/phase_2/data_processing/data/d13_route_40001001011/'
                                'oneformer/output/road_alignment_with_lidar.csv',
                        help='output file with path for aligned road info')

    args = parser.parse_args()
    input_3d = args.input_3d
    road_input_with_path = args.road_input_with_path
    input_2d_mapped_image = args.input_2d_mapped_image
    input_sensor_mapping_file_with_path = args.input_sensor_mapping_file_with_path
    output_file = args.output_file

    with open(road_input_with_path, 'rb') as f:
        input_2d_points = pickle.load(f)[0]
    print(f'input 2d numpy array shape: {input_2d_points.shape}')

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

    with open(input_3d, 'rb') as f:
        input_3d_points = pickle.load(f)[0]

    print(f'input 3d numpy array shape: {input_3d_points.shape}')
    input_3d_df = pd.DataFrame(data=input_3d_points, columns=['X', 'Y', 'Z'])
    input_3d_gdf = gpd.GeoDataFrame(input_3d_df, geometry=gpd.points_from_xy(input_3d_df.X, input_3d_df.Y),
                                    crs='EPSG:6543')
    input_3d_geom_df = input_3d_gdf.geometry.to_crs(epsg=4326)
    # geom_df is added as a geometry_y column in lidar_df while the initial geometry column is renamed as geometry_x
    input_3d_gdf = input_3d_gdf.merge(input_3d_geom_df, left_index=True, right_index=True)
    input_3d_gdf.X = input_3d_gdf.X - proj_cam_x
    input_3d_gdf.Y = input_3d_gdf.Y - proj_cam_y
    # Calculate the distance between the proj_cam_x, proj_cam_y point and the first two X, Y columns of input_3d_points
    input_3d_gdf.Z = np.sqrt(input_3d_gdf.X ** 2 + input_3d_gdf.Y ** 2)
    # calculate the bearing of each 3D point to the camera
    input_3d_gdf['BEARING'] = input_3d_gdf['geometry_y'].apply(lambda geom: bearing_between_two_latlon_points(
        cam_lat, cam_lon, geom.y,geom.x, is_degree=False))
    input_3d_gdf['BEARING'] = input_3d_gdf['BEARING'] - cam_br








