import argparse
from utils import get_aerial_lidar_road_geo_df, compute_match, get_mapping_dataframe
from align_segmented_road_with_lidar import get_mapping_data, get_input_file_with_images


def compute_camera_locs(row, ldf, mapping_df):
    """
    :param row: the image metadata dataframe row to be processed
    :param ldf: lidar 3D point geodataframe
    :param mapping_df: mapping dataframe to extract camera location and its next camera location
    for determining bearing direction
    :return: the computed camera locations for each image frame row
    """

    if len(row["imageBaseName"]) == 11:
        # get input image base name
        input_2d_mapped_image = row["imageBaseName"]
    else:
        # get input image base name
        input_2d_mapped_image = row["imageBaseName"][:-1]

    # compute base camera parameters
    _, _, proj_cam_x, proj_cam_y, _, _, _, _ = get_mapping_data(mapping_df, input_2d_mapped_image)

    # get the lidar road vertex with the closest distance to the camera location
    cam_nearest_lidar_idx, _ = compute_match(proj_cam_x, proj_cam_y, ldf['X'], ldf['Y'])
    cam_lidar_z = ldf.iloc[cam_nearest_lidar_idx].Z

    return cam_lidar_z


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Process arguments.')
    parser.add_argument('--input_lidar_with_path', type=str,
                        default='data/d13_route_40001001012/'
                                'route_40001001012_voxel_raster_1ft_with_edges_normalized_sr_sides.csv',
                        help='input file that contains road x, y, z vertices from lidar')
    parser.add_argument('--obj_image_input', type=str,
                        default='data/d13_route_40001001012/route_40001001012_input.csv',
                        help='input csv file that contains image base names with objects detected along with other '
                             'inputs for mapping')
    parser.add_argument('--input_sensor_mapping_file_with_path', type=str,
                        default='data/d13_route_40001001011/other/mapped_2lane_sr_images_d13.csv',
                        help='input csv file that includes mapped image lat/lon info')
    parser.add_argument('--lidar_proj_output_file', type=str,
                        default='data/d13_route_40001001012/route_40001001012_input_with_camera_z.csv',
                        help='output file with path for each input image with camera location included')

    args = parser.parse_args()
    input_lidar = args.input_lidar_with_path
    obj_image_input = args.obj_image_input
    input_sensor_mapping_file_with_path = args.input_sensor_mapping_file_with_path
    lidar_proj_output_file = args.lidar_proj_output_file

    lidar_df = get_aerial_lidar_road_geo_df(input_lidar)

    input_df = get_input_file_with_images(obj_image_input)

    map_df = get_mapping_dataframe(input_sensor_mapping_file_with_path)

    input_df['CAM_Z'] = input_df.apply(
        lambda row: compute_camera_locs(row, lidar_df, map_df), axis=1)

    input_df.to_csv(lidar_proj_output_file, index=False)
    exit(0)
