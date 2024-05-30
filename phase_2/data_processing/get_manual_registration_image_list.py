import argparse
import sys
import os
import pandas as pd
from utils import get_data_from_image


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Process arguments.')
    parser.add_argument('--input_file', type=str,
                        default='/projects/ncdot/NC_2018_Secondary_2/segmentations/d13_segmentation_path_mapping.csv',
                        help='input file name with path')
    parser.add_argument('--input_sensor_mapping_file_with_path', type=str,
                        default='data/d13_route_40001001011/other/mapped_2lane_sr_images_d13.csv',
                        help='input csv file that includes mapped image lat/lon info')
    parser.add_argument('--output_file', type=str,
                        default='/projects/ncdot/NC_2018_Secondary_2/manual_registration/d13_initial_camera_params.csv',
                        help='output file name with path')

    args = parser.parse_args()
    input_file = args.input_file
    input_sensor_mapping_file_with_path = args.input_sensor_mapping_file_with_path
    output_file = args.output_file

    map_df = pd.read_csv(input_sensor_mapping_file_with_path, usecols=['ROUTEID', 'MAPPED_IMAGE'], dtype=str)
    map_df.sort_values(by=['ROUTEID', 'MAPPED_IMAGE'], inplace=True, ignore_index=True)

    input_df = pd.read_csv(input_file, usecols=['IMAGE_PATH'])
    input_list = input_df['IMAGE_PATH'].tolist()
    out_columns = ['ROUTE_ID', 'IMAGE_BASE_NAME', 'VFOV', 'POS_X', 'POS_Y', 'POS_Z', 'ROT_X', 'ROT_Y', 'ROT_Z']
    out_list = []

    prev_image_width = prev_image_height = -1
    for img_path in input_list:
        image_width, image_height, _ = get_data_from_image(img_path)
        if image_width != prev_image_width or image_height != prev_image_height:
            img_base_name = os.path.basename(img_path)[:-5]
            mapped_image_df = map_df[map_df['MAPPED_IMAGE'] == img_base_name]
            route_id = mapped_image_df.iloc[0].ROUTEID
            out_list.append([route_id, img_base_name, '', '', '', '', '', '', ''])
            prev_image_height = image_height
            prev_image_width = image_width

    out_df = pd.DataFrame(out_list, columns=out_columns)
    sys.exit(0)
