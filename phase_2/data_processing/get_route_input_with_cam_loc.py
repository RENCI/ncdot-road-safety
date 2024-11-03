import argparse
import pandas as pd
from utils import get_aerial_lidar_road_geo_df, compute_match, get_mapping_dataframe
from align_segmented_road_with_lidar import get_mapping_data

PREV_CAM_Z = None

def compute_camera_locs(row, ldf, mapping_df):
    """
    :param row: the image metadata dataframe row to be processed
    :param ldf: lidar 3D point geodataframe
    :param mapping_df: mapping dataframe to extract camera location and its next camera location
    for determining bearing direction
    :return: the computed camera locations for each image frame row
    """
    global PREV_CAM_Z
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
    if PREV_CAM_Z is not None:
        if abs(cam_lidar_z - PREV_CAM_Z) > 10:
            print(f'{input_2d_mapped_image} cam_lidar_z: {cam_lidar_z}, too far from its previous cam z: {PREV_CAM_Z}')
            cam_lidar_z = PREV_CAM_Z

    PREV_CAM_Z = cam_lidar_z
    return cam_lidar_z


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='input and output parameters')
    parser.add_argument('--input_mapping', type=str,
                        default='data/d13_route_40001001011/other/mapped_2lane_sr_images_d13.csv',
                        help='input image mapping csv file')
    parser.add_argument('--input_lidar_with_path', type=str,
                            default='data/d13_route_40001001012/'
                                    'route_40001001012_voxel_raster_1ft_with_edges_normalized_sr_sides.csv',
                            help='input file that contains road x, y, z vertices from lidar')
    parser.add_argument('--input_images', type=str,
                        default='data/d13_route_40001001012/route_40001001012_input.csv',
                        help='input csv file that contains all images to get camera lat/lon for')
    parser.add_argument('--output_file', type=str,
                        default='data/d13_route_40001001012/route_40001001012_with_cam_loc.csv',
                        help='output file with image name and corresponding camera lat/lon')


    args = parser.parse_args()
    input_mapping = args.input_mapping
    input_lidar = args.input_lidar_with_path
    input_images = args.input_images
    output_file = args.output_file

    lidar_df = get_aerial_lidar_road_geo_df(input_lidar)
    mapping_df = get_mapping_dataframe(input_mapping)
    image_df = pd.read_csv(input_images, usecols=['imageBaseName'], dtype=str)
    image_df.drop_duplicates(subset=['imageBaseName'], inplace=True)
    merge_df = pd.merge(mapping_df, image_df, how='inner', left_on=['MAPPED_IMAGE'], right_on=['imageBaseName'])
    merge_df.drop(columns='MAPPED_IMAGE', inplace=True)
    merge_df['CAM_Z'] = merge_df.apply(
            lambda row: compute_camera_locs(row, lidar_df, mapping_df), axis=1)
    merge_df['LATITUDE'] = merge_df['LATITUDE'].str.replace('+', '', regex=False)
    merge_df.to_csv(output_file, index=False)
