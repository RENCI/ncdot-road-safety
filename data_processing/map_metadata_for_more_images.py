# This script maps more images to PathRunner image viewer sensor output to associate images with
# mileposts and lat/longs. It reads all images in a division and checks against the existing mapped file
# to find those unmapped images to see whether they can be further mapped to the sensor output. It then
# combines the previously mapped data with the further mapped data to create an updated more complete mapping data
# Command to run the script: python map_metadata_for_more_images.py --input_sensor_metadata_file
# <input_sensor_metadata_file> --input_image_root_dir <input_image_root_dir>
# --input_map_file <previously_mapped_input_file> --output_map_file <updated_mapped_output_file>

import argparse
import sys
import os
import pandas as pd
from utils import find_closest_mapped_metadata, get_unmapped_base_images, get_image_path


parser = argparse.ArgumentParser(description='Process arguments.')
parser.add_argument('--input_sensor_metadata_file', type=str,
                    default='/projects/ncdot/secondary_road/output/d10/d10_sensor_output_2lane.csv',
                    help='input sensor metadata file')
parser.add_argument('--input_image_root_dir', type=str,
                    default='/projects/ncdot/NC_2018_Secondary/d10',
                    help='input image root directory to walk over and find all images for the division')
parser.add_argument('--input_map_file', type=str,
                    default='/projects/ncdot/secondary_road/output/d10/mapped_2lane_sr_images_d10.csv',
                    help='input sensor metadata file')
parser.add_argument('--output_map_file', type=str,
                    default='/projects/ncdot/secondary_road/output/d10/mapped_2lane_sr_images_d10_updated.csv',
                    help='output mapping file')

args = parser.parse_args()
input_sensor_metadata_file = args.input_sensor_metadata_file
input_image_root_dir = args.input_image_root_dir
input_map_file = args.input_map_file
output_map_file = args.output_map_file

sensor_df = pd.read_csv(input_sensor_metadata_file, dtype={
    'RouteID': str,
    'Start-MP': float,
    'Start-Image': int,
    'StaLatitude': str,
    'StaLongitude': str
})
print(f'sensor_df shape: {sensor_df.shape}')

input_map_df = pd.read_csv(input_map_file, header=0, dtype={
    'ROUTEID': str,
    'MAPPED_IMAGE': int,
    'LATITUDE': str,
    'LONGITUDE': str,
    'MILE_POST': float,
    'PATH': str
})

df_input_img_map = input_map_df[['MAPPED_IMAGE']]

img_basenames = []
for dir_name, subdir_list, file_list in os.walk(input_image_root_dir):
    for file_name in file_list:
        if len(file_name) == 16 and file_name.lower().endswith(('1.jpg')):
            img_basenames.append(int(file_name[:-5]))

all_img_df = pd.DataFrame(img_basenames, columns=['IMAGE_BASE_NAME'])
print(f'all_img_df shape: {all_img_df.shape}')
to_be_mapped_df = get_unmapped_base_images(all_img_df, df_input_img_map)
print(f'to_be_mapped_df shape: {to_be_mapped_df.shape}')
to_be_mapped_df[['MAPPED_INDEX', 'MAPPED_VALUE']] = \
    to_be_mapped_df.apply(lambda row: pd.Series(find_closest_mapped_metadata(
        row['IMAGE_BASE_NAME'], sensor_df[['Start-Image']])), axis=1)
print(f'after metadata mapping: to_be_mapped_df shape: {to_be_mapped_df.shape}')

to_be_mapped_df['MAPPED_VAL_DIFF'] = abs(to_be_mapped_df['IMAGE_BASE_NAME'] - to_be_mapped_df['MAPPED_VALUE'])
# did not use to_be_mapped_df[to_be_mapped_df['MAPPED_VAL_DIFF'] < 3] since drop_duplicates() may drop
# the row with smaller MAPPED_VAL_DIFF. Doing it the following way will make sure
# MAPPED_VAL_DIFF of 2 of duplicates will be dropped
map_img_df_01 = to_be_mapped_df[to_be_mapped_df['MAPPED_VAL_DIFF'] < 2]
map_img_df_2 = to_be_mapped_df[to_be_mapped_df['MAPPED_VAL_DIFF'] == 2]
map_img_df = pd.concat([map_img_df_01, map_img_df_2])
print(f'before dropping duplicates, map_img_df shape: {map_img_df.shape}')
map_img_df.drop_duplicates(subset=['MAPPED_VALUE'], keep='first', inplace=True)
print(f'after dropping duplicates, map_img_df shape: {map_img_df.shape}')
map_img_df['IMAGE_PATH'] = map_img_df.apply(lambda row: get_image_path(str(row['MAPPED_IMAGE']),
                                                                       prefix_path=input_image_root_dir,
                                                                       include_image_name=False), axis=1)
output_list = []
map_img_df.apply(lambda row: output_list.append([sensor_df.iloc[row.MAPPED_INDEX]['RouteID'],
                                                 row.IMAGE_BASE_NAME,
                                                 sensor_df.iloc[row.MAPPED_INDEX]['StaLatitude'],
                                                 sensor_df.iloc[row.MAPPED_INDEX]['StaLongitude'],
                                                 sensor_df.iloc[row.MAPPED_INDEX]['Start-MP'],
                                                 row.IMAGE_PATH]), axis=1)
print(f'output_list length: {len(output_list)}')
output_cols = ['ROUTEID', 'MAPPED_IMAGE', 'LATITUDE', 'LONGITUDE', 'MILE_POST', 'PATH']
map_df = pd.DataFrame(output_list, columns=output_cols)

output_map_df = pd.concat([input_map_df, map_df])
print(f'before dropping duplicates, output_map_df shape: {output_map_df.shape}')
output_map_df.drop_duplicates(inplace=True)
print(f'after dropping duplicates, output_map_df shape: {output_map_df.shape}')
output_map_df.sort_values(by=['ROUTEID', 'MAPPED_IMAGE'], inplace=True)
output_map_df.to_csv(output_map_file, index=False)
print(f'DONE, output_map_df shape: {output_map_df.shape}, map_df shape: {map_df.shape}, '
      f'input_map_df shape: {input_map_df.shape}')
sys.exit(0)
