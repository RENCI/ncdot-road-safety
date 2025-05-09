import argparse
import os
import sys
import pandas as pd
import numpy as np
from utils import (bearing_between_two_latlon_points, get_aerial_lidar_road_geo_df, add_lidar_x_y_from_lat_lon)
from get_road_boundary_points import get_image_lane_points
from align_segmented_road_with_lidar import init_transform_from_lidar_to_world_coordinate_system, \
    get_input_file_with_images, extract_lidar_3d_points_for_camera, LIDAR_DIST_THRESHOLD
from common.utils import haversine


def create_data(row, img_width, img_height, seg_lane_dir, input_lidar_file, out_file_base,
                input_loc=None, input_road_intersect=None):
    # get input image base name
    input_2d_mapped_image = row["imageBaseName"]
    lane_image_name = os.path.join(seg_lane_dir, f'{input_2d_mapped_image}1_lanes.png')
    img_width, img_height, _, input_list, _ = get_image_lane_points(lane_image_name, resized_width=img_width,
                                                                    resized_height=img_height)

    input_2d_points = input_list[0]
    out_file = f'{out_file_base}_{input_2d_mapped_image}.csv'
    np.savetxt(os.path.join(os.path.dirname(out_file_base), f'input_2d_{input_2d_mapped_image}1.csv'),
               input_2d_points, delimiter=',', header='X,Y', comments='', fmt='%d')

    ldf = get_aerial_lidar_road_geo_df(input_lidar_file)

    cam_lat = float(row['LATITUDE'])
    cam_lon = float(row['LONGITUDE'])

    cam_lat2 = float(row['LATITUDE_next'])
    cam_lon2 = float(row['LONGITUDE_next'])

    cam_br = bearing_between_two_latlon_points(cam_lat, cam_lon, cam_lat2, cam_lon2, is_degree=False)
    cam_geom_df = add_lidar_x_y_from_lat_lon(pd.DataFrame(data={'LONGITUDE': [cam_lon], 'LATITUDE': [cam_lat]}))
    proj_cam_x = cam_geom_df.iloc[0].x
    proj_cam_y = cam_geom_df.iloc[0].y

    cam_lidar_z = row['CAM_Z']

    # filter out LIDAR points approximately by distance for performance improvement
    ldf = ldf[((ldf.X - proj_cam_x).abs() < LIDAR_DIST_THRESHOLD[1]) &
              ((ldf.Y - proj_cam_y).abs() < LIDAR_DIST_THRESHOLD[1])]

    input_3d_gdf, cam_br, _ = extract_lidar_3d_points_for_camera(ldf, [cam_lat, cam_lon],
                                                                 [cam_lat2, cam_lon2],
                                                                 dist_th=LIDAR_DIST_THRESHOLD,
                                                                 include_all_cols=True, fov=90,
                                                                 proj_cam_x=proj_cam_x,
                                                                 proj_cam_y=proj_cam_y
                                                                 )
    input_3d_gdf['BEARING'] = input_3d_gdf['geometry_y'].apply(lambda geom: bearing_between_two_latlon_points(
        cam_lat, cam_lon, geom.y, geom.x, is_degree=False) - cam_br)
    print(input_3d_gdf.shape)
    print(input_3d_gdf.columns)
    cam_df = pd.DataFrame(data={'LATITUDE': [cam_lat2], 'LONGITUDE': [cam_lon2]})
    cam_gdf = add_lidar_x_y_from_lat_lon(cam_df)
    proj_cam_x2 = cam_gdf.iloc[0].x
    proj_cam_y2 = cam_gdf.iloc[0].y
    proj_cam_z2 = row['CAM_Z_next'] if pd.notna(row['CAM_Z_next']) else row['CAM_Z']
    print(f'proj_cam_z2: {proj_cam_z2}')
    input_3d_gdf = init_transform_from_lidar_to_world_coordinate_system(input_3d_gdf, proj_cam_x, proj_cam_y,
                                                                        cam_lidar_z, proj_cam_x2, proj_cam_y2,
                                                                        proj_cam_z2)
    print(input_3d_gdf.shape)
    print(input_3d_gdf.columns)

    if input_loc:
        input_3d_gdf['DISTANCE_TO_POLE'] = input_3d_gdf.apply(lambda row: haversine(input_loc[1], input_loc[0],
                                                                                    row['geometry_y'].x,
                                                                                    row['geometry_y'].y), axis=1)
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
                        default='data/d13_route_40001001012/'
                                'route_40001001012_voxel_raster_1ft_with_edges_normalized_sr_sides.csv',
                        help='input file that contains x, y, z vertices from lidar')
    parser.add_argument('--lane_seg_dir', type=str,
                        default='data/d13_route_40001001012/segmentation',
                        help='directory to retrieve segmented road lane images')
    parser.add_argument('--obj_image_input', type=str,
                        default='data/d13_route_40001001012/manual_registration/input.csv',
                        help='input csv file that contains image base names for creating manual registration data')
    parser.add_argument('--image_width', type=int, default=2356)
    parser.add_argument('--image_height', type=int, default=1200)
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
                        default='data/d13_route_40001001012/manual_registration/lidar_info',
                        help='output lidar file base with path which will be appended with image name '
                             'to have lidar INITIAL WORLD coordinate info for each input image')

    args = parser.parse_args()
    input_lidar = args.input_lidar_with_path
    lane_seg_dir = args.lane_seg_dir
    obj_image_input = args.obj_image_input
    input_landmark_loc = args.input_landmark_loc
    output_lidar_file_base = args.output_lidar_file_base
    input_road_lidar_with_intersection = args.input_road_lidar_with_intersection
    image_width = args.image_width
    image_height = args.image_height

    # load input file to get the image names for alignment
    input_df = get_input_file_with_images(obj_image_input)
    print(input_df.columns)
    input_df['CAM_Z_next'] = input_df['CAM_Z'].shift(-1)
    input_df['LATITUDE_next'] = input_df['LATITUDE'].shift(-1)
    input_df['LONGITUDE_next'] = input_df['LONGITUDE'].shift(-1)

    # Apply create_data() to all rows except the last row
    input_df.iloc[:-1, :].apply(lambda row: create_data(row, image_width, image_height, lane_seg_dir, input_lidar,
                                                        output_lidar_file_base,
                                                        input_loc=input_landmark_loc,
                                                        input_road_intersect=input_road_lidar_with_intersection),
                                axis=1)
    sys.exit()
