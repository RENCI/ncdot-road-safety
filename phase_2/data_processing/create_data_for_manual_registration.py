import argparse
import os
import pandas as pd
import geopandas as gpd
import numpy as np
from utils import bearing_between_two_latlon_points, get_aerial_lidar_road_geo_df, haversine
from get_road_boundary_points import get_image_road_points
from align_segmented_road_with_lidar import init_transform_from_lidar_to_world_coordinate_system, compute_match, \
    get_mapping_data, get_input_file_with_images


def create_data(image_name_with_path, input_lidar_file, input_mapping_file, out_file, input_loc=None):
    # get input image base name
    input_2d_mapped_image = os.path.basename(image_name_with_path)[:-5]
    img_width, img_height, input_list = get_image_road_points(image_name_with_path, boundary_only=False)

    input_2d_points = input_list[0]

    np.savetxt(os.path.join(os.path.dirname(out_file), f'input_2d_{input_2d_mapped_image}1.csv'),
               input_2d_points, delimiter=',', header='X,Y', comments='', fmt='%d')

    ldf = get_aerial_lidar_road_geo_df(input_lidar_file, road_only=False)

    cam_lat, cam_lon, proj_cam_x, proj_cam_y, cam_br, cam_lat2, cam_lon2, eor = get_mapping_data(
        input_mapping_file, input_2d_mapped_image)

    input_3d_points = ldf[['X', 'Y', 'Z']].to_numpy()
    print(f'len(input_3d_points): {len(input_3d_points)}')
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
    cam_lidar_z = input_3d_gdf.iloc[nearest_idx].Z
    print(f'camera Z: {cam_lidar_z}')
    input_3d_gdf = init_transform_from_lidar_to_world_coordinate_system(input_3d_gdf, proj_cam_x, proj_cam_y,
                                                                        cam_lidar_z)
    if input_loc:
        input_3d_gdf['DISTANCE_TO_POLE'] = input_3d_gdf.apply(lambda row: haversine(input_loc[1], input_loc[0],
                                                                                    row['geometry_y']), axis=1)
    joined_df = pd.concat([input_3d_gdf, ldf[['C']]], axis=1)
    joined_df.to_csv(out_file,
                     columns=['X', 'Y', 'Z', 'C', 'INITIAL_WORLD_X', 'INITIAL_WORLD_Y', 'INITIAL_WORLD_Z',
                              'DISTANCE_TO_POLE'],
                     float_format='%.3f', index=False)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Process arguments.')
    parser.add_argument('--input_lidar_with_path', type=str,
                        default='data/d13_route_40001001011/lidar/test_scene_all_raster_10.csv',
                        help='input file that contains road x, y, z vertices from lidar')
    parser.add_argument('--obj_base_image_dir', type=str,
                        default='data/d13_route_40001001011/oneformer',
                        help='base directory to retrieve images')
    parser.add_argument('--obj_image_input', type=str,
                        default='../object_mapping/data/pole_input.csv.rep',
                        help='input csv file that contains image base names with objects detected along with other '
                             'inputs for mapping')
    parser.add_argument('--input_sensor_mapping_file_with_path', type=str,
                        default='data/d13_route_40001001011/other/mapped_2lane_sr_images_d13.csv',
                        help='input csv file that includes mapped image lat/lon info')
    parser.add_argument('--input_landmark_loc', type=str,
                        default=(35.7134730, -82.73446760),
                        help='input landmark location to compute distance from each LIDAR point')
    parser.add_argument('--output_lidar_file_base', type=str,
                        default='/home/hongyi/ncdot-registration/data/lidar_info',
                        help='output lidar file base with path which will be appended with image name '
                             'to have lidar INITIAL WORLD coordinate info for each input image')

    args = parser.parse_args()
    input_lidar = args.input_lidar_with_path
    obj_base_image_dir = args.obj_base_image_dir
    obj_image_input = args.obj_image_input
    input_sensor_mapping_file_with_path = args.input_sensor_mapping_file_with_path
    input_landmark_loc = args.input_landmark_loc
    output_lidar_file_base = args.output_lidar_file_base

    # load input file to get the image names for alignment
    input_df = get_input_file_with_images(obj_image_input)
    input_df['imageBaseName'].apply(lambda img: create_data(os.path.join(obj_base_image_dir, f'{img}.png'),
                                                            input_lidar, input_sensor_mapping_file_with_path,
                                                            f'{output_lidar_file_base}_{img}.csv',
                                                            input_loc=input_landmark_loc))