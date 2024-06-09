import argparse
import sys
import os
import pandas as pd
from utils import find_closest_mapped_metadata


parser = argparse.ArgumentParser(description='Process arguments.')
parser.add_argument('--input_sensor_metadata_file', type=str,
                    default='/projects/ncdot/secondary_road/output/d04/d4_sensor_output_2lane.csv',
                    help='input sensor metadata file')
parser.add_argument('--input_image_root_dir', type=str,
                    default='/projects/ncdot/NC_2018_Secondary/d04',
                    help='input image root directory to walk over and find all images for the division')
parser.add_argument('--input_map_file', type=str,
                    default='/projects/ncdot/secondary_road/output/d04/mapped_2lane_sr_images_d4.csv',
                    help='input sensor metadata file')
parser.add_argument('--output_map_file', type=str,
                    default='/projects/ncdot/secondary_road/output/d04/mapped_2lane_sr_images_d4_updated.csv',
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

img_paths_and_basenames = []
for dir_name, subdir_list, file_list in os.walk(input_image_root_dir):
    for file_name in file_list:
        if file_name.lower().endswith(('1.jpg')):
            img_paths_and_basenames.append([dir_name, file_name[:-5]])
img_df = pd.DataFrame(img_paths_and_basenames, columns=['IMAGE_PATH', 'IMAGE_BASE_NAME'])
print(f'img_df shape: {img_df.shape}')
img_df[['MAPPED_INDEX', 'MAPPED_VALUE']] = \
    img_df.apply(lambda row: pd.Series(find_closest_mapped_metadata(
        row['IMAGE_BASE_NAME'], sensor_df[['Start-Image']])), axis=1)
print(f'after metadata mapping: img_df shape: {img_df.shape}')

img_df['MAPPED_VAL_DIFF'] = abs(img_df['IMAGE_BASE_NAME'] - img_df['MAPPED_VALUE'])
# did not use img_df[img_df['MAPPED_VAL_DIFF'] < 3] since drop_duplicates() may drop
# the row with smaller MAPPED_VAL_DIFF. Doing it the following way will make sure
# MAPPED_VAL_DIFF of 2 of duplicates will be dropped
map_img_df_01 = img_df[img_df['MAPPED_VAL_DIFF'] < 2]
map_img_df_2 = img_df[img_df['MAPPED_VAL_DIFF'] == 2]
map_img_df = pd.concat([map_img_df_01, map_img_df_2])
print(f'before dropping duplicates, map_img_df shape: {map_img_df.shape}')
map_img_df.drop_duplicates(subset=['MAPPED_VALUE'], keep='first', inplace=True)
print(f'after dropping duplicates, map_img_df shape: {map_img_df.shape}')
output_list = []
map_img_df.apply(lambda row: output_list.append([sensor_df.iloc[row.MAPPED_INDEX]['RouteID'],
                                                 row.IMAGE_BASE_NAME,
                                                sensor_df.iloc[row.MAPPED_INDEX]['StaLatitude'],
                                                sensor_df.iloc[row.MAPPED_INDEX]['StaLongitude'],
                                                sensor_df.iloc[row.MAPPED_INDEX]['Start-MP'],
                                                row.IMAGE_PATH
                                                ]), axis=1)
print(f'output_list length: {len(output_list)}')
output_cols = ['ROUTEID', 'MAPPED_IMAGE', 'LATITUDE', 'LONGITUDE', 'MILE_POST', 'PATH']
map_df = pd.DataFrame(output_list, columns=output_cols)

input_map_df = pd.read_csv(input_map_file, dtype={
    'ROUTEID': str,
    'MAPPED_IMAGE': int,
    'LATITUDE': str,
    'LONGITUDE': str,
    'MILE_POST': float,
    'PATH': str
})

output_map_df = pd.concat([input_map_df, map_df])
print(f'before dropping duplicates, output_map_df shape: {output_map_df.shape}')
output_map_df.drop_duplicates(inplace=True)
print(f'after dropping duplicates, output_map_df shape: {output_map_df.shape}')
output_map_df.sort_values(by=['ROUTEID', 'MAPPED_IMAGE'], inplace=True)
output_map_df.to_csv(output_map_file, index=False)
print(f'DONE, output_map_df shape: {output_map_df.shape}, map_df shape: {map_df.shape}, '
      f'input_map_df shape: {input_map_df.shape}')
sys.exit(0)
