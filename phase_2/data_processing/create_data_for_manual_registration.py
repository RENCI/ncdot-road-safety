import argparse
import os
import sys
import pandas as pd
import numpy as np
from utils import bearing_between_two_latlon_points, get_aerial_lidar_road_geo_df, haversine, create_gdf_from_df
from get_road_boundary_points import get_image_road_points
from align_segmented_road_with_lidar import init_transform_from_lidar_to_world_coordinate_system, compute_match, \
    get_mapping_data, get_input_file_with_images, extract_lidar_3d_points_for_camera, LIDAR_DIST_THRESHOLD


def create_data(image_name_with_path, input_lidar_file, input_mapping_file, out_file, input_loc=None,
                input_road_intersect=None):
    # get input image base name
    input_2d_mapped_image = os.path.basename(image_name_with_path)[:-5]
    img_width, img_height, input_list, _ = get_image_road_points(image_name_with_path)

    input_2d_points = input_list[0]

    np.savetxt(os.path.join(os.path.dirname(out_file), f'input_2d_{input_2d_mapped_image}1.csv'),
               input_2d_points, delimiter=',', header='X,Y', comments='', fmt='%d')

    ldf = get_aerial_lidar_road_geo_df(input_lidar_file)

    cam_lat, cam_lon, proj_cam_x, proj_cam_y, cam_br, cam_lat2, cam_lon2, eor = get_mapping_data(
        input_mapping_file, input_2d_mapped_image)

    # get the lidar road vertex with the closest distance to the camera location
    nearest_idx = compute_match(proj_cam_x, proj_cam_y, ldf['X'], ldf['Y'])[0]
    cam_lidar_z = ldf.iloc[nearest_idx].Z
    print(f'camera Z: {cam_lidar_z}, eor: {eor}, dist_th: {LIDAR_DIST_THRESHOLD}')

    input_3d_gdf, cam_br, _ = extract_lidar_3d_points_for_camera(ldf, [cam_lat, cam_lon], [cam_lat2, cam_lon2],
                                                                 dist_th=LIDAR_DIST_THRESHOLD,
                                                                 end_of_route=eor,
                                                                 include_all_cols=True)
    input_3d_gdf['BEARING'] = input_3d_gdf['geometry_y'].apply(lambda geom: bearing_between_two_latlon_points(
        cam_lat, cam_lon, geom.y, geom.x, is_degree=False) - cam_br)
    print(input_3d_gdf.shape)
    print(input_3d_gdf.columns)
    input_3d_gdf = init_transform_from_lidar_to_world_coordinate_system(input_3d_gdf, proj_cam_x, proj_cam_y,
                                                                        cam_lidar_z)
    print(input_3d_gdf.shape)
    print(input_3d_gdf.columns)

    if input_loc:
        input_3d_gdf['DISTANCE_TO_POLE'] = input_3d_gdf.apply(lambda row: haversine(input_loc[1], input_loc[0],
                                                                                    row['geometry_y']), axis=1)
    if input_road_intersect:
        road_ldf = pd.read_csv(input_road_intersect)
        input_3d_gdf = input_3d_gdf.merge(road_ldf, on=['X', 'Y', 'Z'], how='left')
        input_3d_gdf['I'].fillna(0, inplace=True)
        input_3d_gdf['I'] = input_3d_gdf['I'].astype(int)
    if input_loc:
        input_3d_gdf.to_csv(out_file,
                            columns=['X', 'Y', 'Z', 'C', 'INITIAL_WORLD_X', 'INITIAL_WORLD_Y', 'INITIAL_WORLD_Z',
                                     'DISTANCE_TO_POLE'], float_format='%.3f', index=False)
    elif input_road_intersect:
        input_3d_gdf.to_csv(out_file,
                            columns=['X', 'Y', 'Z', 'C', 'INITIAL_WORLD_X', 'INITIAL_WORLD_Y', 'INITIAL_WORLD_Z', 'I'],
                            float_format='%.3f', index=False)
    else:
        input_3d_gdf.to_csv(out_file,
                            columns=['X', 'Y', 'Z', 'C', 'INITIAL_WORLD_X', 'INITIAL_WORLD_Y', 'INITIAL_WORLD_Z'],
                            float_format='%.3f', index=False)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Process arguments.')
    parser.add_argument('--input_lidar_with_path', type=str,
                        # default='data/d13_route_40001001011/lidar/test_scene_all_raster_10.csv',
                        default='data/new_test_scene/new_test_scene_all_raster_10_with_road_bounds.csv',
                        help='input file that contains x, y, z vertices from lidar')
    parser.add_argument('--obj_base_image_dir', type=str,
                        # default='data/d13_route_40001001011/oneformer',
                        default='data/new_test_scene/segmentation',
                        help='base directory to retrieve images')
    parser.add_argument('--obj_image_input', type=str,
                        # default='../object_mapping/data/pole_input.csv.rep',
                        default='../object_mapping/data/new_test_route.csv',
                        help='input csv file that contains image base names with objects detected along with other '
                             'inputs for mapping')
    parser.add_argument('--input_sensor_mapping_file_with_path', type=str,
                        default='data/d13_route_40001001011/other/mapped_2lane_sr_images_d13.csv',
                        help='input csv file that includes mapped image lat/lon info')
    parser.add_argument('--input_landmark_loc', type=str,
                        # default=(35.7134730, -82.73446760),
                        default='',
                        help='input landmark location to compute distance from each LIDAR point')
    parser.add_argument('--input_road_lidar_with_intersection', type=str,
                        # default='data/new_test_scene/new_test_scene_road_raster_10.csv',
                        default='',
                        help='input file that contains road x, y, z vertices from lidar along with a I column '
                             'indicating whether the vertex is part of crossroad intersection or not')
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
    input_road_lidar_with_intersection = args.input_road_lidar_with_intersection

    # load input file to get the image names for alignment
    input_df = get_input_file_with_images(obj_image_input)
    input_df['imageBaseName'].apply(lambda img: create_data(os.path.join(obj_base_image_dir, f'{img}.png'),
                                                            input_lidar, input_sensor_mapping_file_with_path,
                                                            f'{output_lidar_file_base}_{img}.csv',
                                                            input_loc=input_landmark_loc,
                                                            input_road_intersect=input_road_lidar_with_intersection))
    sys.exit()
