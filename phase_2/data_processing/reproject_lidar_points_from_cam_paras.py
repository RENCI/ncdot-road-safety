import argparse
import os
import pandas as pd
from extract_lidar_3d_points import extract_lidar_3d_points_for_camera
from align_segmented_road_with_lidar import (get_mapping_data, transform_3d_points, get_input_file_with_images,
                                             init_transform_from_lidar_to_world_coordinate_system)
from utils import (get_mapping_dataframe, get_aerial_lidar_road_geo_df, create_gdf_from_df,
                   bearing_between_two_latlon_points, create_df_from_lidar_points)

LIDAR_DIST_THRESHOLD = (3.5, 210)


def reproject_points_from_cam_paras(df_row, mapping_df, ldf, img_wd, img_hgt, out_path):
    image_base_name = df_row['imageBaseName']

    cam_lat, cam_lon, proj_cam_x, proj_cam_y, cam_br, cam_lat2, cam_lon2, eor = \
        get_mapping_data(mapping_df, image_base_name)
    cam_lidar_z = df_row['CAM_Z']
    vertices, cam_br, cols = extract_lidar_3d_points_for_camera(ldf, [cam_lat, cam_lon], [cam_lat2, cam_lon2],
                                                                dist_th=LIDAR_DIST_THRESHOLD,
                                                                end_of_route=eor,
                                                                fov=90)
    input_3d_df = create_df_from_lidar_points(vertices[0], cols)
    input_3d_gdf = create_gdf_from_df(input_3d_df)
    # calculate the bearing of each 3D point to the camera
    input_3d_gdf['BEARING'] = input_3d_gdf['geometry_y'].apply(lambda geom: bearing_between_two_latlon_points(
        cam_lat, cam_lon, geom.y, geom.x, is_degree=False) - cam_br)

    input_3d_gdf = init_transform_from_lidar_to_world_coordinate_system(input_3d_gdf, proj_cam_x, proj_cam_y,
                                                                        cam_lidar_z)
    input_3d_gdf = transform_3d_points(input_3d_gdf, df_row['CAM_PARA_LIST'],
                                       img_wd, img_hgt)
    input_3d_gdf.to_csv(os.path.join(out_path, f'lidar_project_info_{image_base_name}.csv'),
                        index=False)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Process reproject_lidar_points_from_cam_paras arguments.')
    parser.add_argument('--input_lidar_with_path', type=str,
                        default='/projects/ncdot/NC_2018_Secondary_2/'
                                'route_40001001012_voxel_raster_1ft_with_edges_normalized_sr_sides.csv',
                        help='input file that contains road x, y, z vertices from lidar')
    parser.add_argument('--input_cam_para_path', type=str,
                        default='/projects/ncdot/NC_2018_Secondary_2/route_40001001012_geotagging_output',
                        help='input path that includes camera parameter files for all input images')
    parser.add_argument('--input_sensor_mapping_file_with_path', type=str,
                        default='/projects/ncdot/secondary_road/output/d13/mapped_2lane_sr_images_d13_updated.csv',
                        help='input csv file that includes mapped image lat/lon info')
    parser.add_argument('--input_images_with_cam_loc', type=str,
                        default='/projects/ncdot/NC_2018_Secondary_2/route_40001001012_input.csv',
                        help='input csv file that includes mapped image lat/lon info')
    parser.add_argument('--image_width', type=int, default=2356,
                        help='image width in the screen coordinate system for projecting LIDAR points to')
    parser.add_argument('--image_height', type=int, default=1200,
                        help='image height in the screen coordinate system for projecting LIDAR points to')
    parser.add_argument('--output_path', type=str,
                        default='/projects/ncdot/NC_2018_Secondary_2/route_40001001012_geotagging_output_2',
                        help='output path for reprojecting LIDAR points for each input image')

    args = parser.parse_args()
    input_lidar_with_path = args.input_lidar_with_path
    input_cam_para_path = args.input_cam_para_path
    input_sensor_mapping_file_with_path = args.input_sensor_mapping_file_with_path
    input_images_with_cam_loc = args.input_images_with_cam_loc
    image_width = args.image_width
    image_height = args.image_height
    output_path = args.output_path

    input_df = get_input_file_with_images(input_images_with_cam_loc)

    lidar_df = get_aerial_lidar_road_geo_df(input_lidar_with_path)

    cam_para_files = [filename for filename in os.listdir(input_cam_para_path) if filename.endswith('cam_paras.csv')]
    cam_para_dfs = [pd.read_csv(os.path.join(input_cam_para_path, cam_para_f)) for cam_para_f in cam_para_files]
    cam_para_df = pd.concat(cam_para_dfs)
    cam_para_df['imageBaseName'] = [cam_para_f[len('lidar_project_info_'):-len('_cam_paras.csv')] for cam_para_f
                                    in cam_para_files]
    cam_para_df['CAM_PARA_LIST'] = [[0.1, 20, x, y, z, rx, ry, rz] for x, y, z, rx, ry, rz in
                                    zip(cam_para_df['translation_x'], cam_para_df['translation_y'],
                                        cam_para_df['translation_z'], cam_para_df['rotation_z'],
                                        cam_para_df['rotation_y'], cam_para_df['rotation_x'])]
    cam_para_df.drop(columns=['translation_x', 'translation_y', 'translation_z', 'rotation_z',
                              'rotation_y', 'rotation_x'], inplace=True)
    cam_para_df = cam_para_df.merge(input_df, left_on='imageBaseName', right_on='imageBaseName', how='left')
    map_df = get_mapping_dataframe(input_sensor_mapping_file_with_path)
    cam_para_df.apply(lambda row: reproject_points_from_cam_paras(row, map_df, lidar_df, image_width, image_height,
                                                                  output_path), axis=1)

