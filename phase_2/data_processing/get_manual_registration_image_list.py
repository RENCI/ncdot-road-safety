import argparse
import sys
import os
import pandas as pd
from utils import get_image_resolution


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Process arguments.')
    parser.add_argument('--input_file', type=str,
                        default='/projects/ncdot/NC_2018_Secondary_2/segmentations/d13_segmentation_path_mapping.csv',
                        help='input file name with path')
    parser.add_argument('--input_sensor_mapping_file_with_path', type=str,
                        default='/projects/ncdot/secondary_road/output/d13/mapped_2lane_sr_images_d13.csv',
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

    input_columns = ['IMAGE_PATH', 'SEGMENTATION_PATH']
    input_df = pd.read_csv(input_file, usecols=input_columns)
    input_img_paths = input_df['IMAGE_PATH'].tolist()
    input_img_seg_paths = input_df['SEGMENTATION_PATH'].tolist()
    out_columns = ['ROUTE_ID', 'IMAGE_BASE_NAME', 'VFOV', 'POS_X', 'POS_Y', 'POS_Z', 'ROT_X', 'ROT_Y', 'ROT_Z']
    out_list = []
    updated_input_list = []
    prev_image_width = prev_image_height = -1
    for idx, img_paths in enumerate(zip(input_img_paths, input_img_seg_paths)):
        img_path, img_seg_path = img_paths
        img_base_name = os.path.basename(img_path)[:-5]
        mapped_image_df = map_df[map_df['MAPPED_IMAGE'] == img_base_name]
        if len(mapped_image_df) > 0:
            updated_input_list.append([img_path, img_seg_path])
            image_width, image_height = get_image_resolution(img_path)
            if image_width != prev_image_width or image_height != prev_image_height:
                route_id = mapped_image_df.iloc[0].ROUTEID
                out_list.append([route_id, img_base_name, '', '', '', '', '', '', ''])
                prev_image_height = image_height
                prev_image_width = image_width
                print(f'{img_base_name} is added to list for manual registration, '
                      f'image_width: {image_width}, image_height: {image_height}', flush=True)
        if idx % 100000 == 0:
            print(f'{idx} images have been checked', flush=True)
    out_df = pd.DataFrame(out_list, columns=out_columns)
    out_df.to_csv(output_file, index=False)
    updated_input_df = pd.DataFrame(updated_input_list, columns=input_columns)
    updated_input_df.to_csv(os.path.join(os.path.dirname(output_file), os.path.basename(input_file)), index=False)
    sys.exit(0)
