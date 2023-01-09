# This script updates the mapped sensor output image list to add the images missing from the initial mapping done
# by running prepare_images_and_metadata.py back to the mapped list.
# Command to run the script: python update_sensor_mapped_image_list.py
import argparse
import os
import pandas as pd
from utils import map_image


parser = argparse.ArgumentParser(description='Process arguments.')
parser.add_argument('--root_dir', type=str,
                    default='/projects/ncdot/NC_2018_Secondary/d13',
                    help='root directory to look for images to process')
parser.add_argument('--input_map_file_to_update', type=str,
                    default='/projects/ncdot/secondary_road/output/d13/mapped_2lane_sr_images_d13.csv',
                    help='previously mapped file to be updated')
parser.add_argument('--input_sensor_output_file_2lane', type=str,
                    default='/projects/ncdot/secondary_road/output/d13/d13_sensor_output_2lane.csv',
                    help='input 2-lane only sensor output file for mapping images to lat/lon and mileposts')
parser.add_argument('--output_dir', type=str, default='/projects/ncdot/NC_2018_Secondary/single_images/d13',
                    help='output directory for creating symlinked images')
parser.add_argument('--output_file', type=str,
                    default='/projects/ncdot/secondary_road/output/d13/mapped_2lane_sr_images_d13_updated.csv',
                    help='output file for updating the file as set in input_map_file_to_update argument')

args = parser.parse_args()
root_dir = args.root_dir
input_map_file_to_update = args.input_map_file_to_update
input_sensor_output_file_2lane = args.input_sensor_output_file_2lane
output_dir = args.output_dir
output_file = args.output_file


sensor_df = pd.read_csv(input_sensor_output_file_2lane, header=0, dtype={
    'RouteID': str,
    'Start-MP': float,
    'Start-Image': str,
    'StaLatitude': str,
    'StaLongitude':str
})

mapped_images_df = pd.read_csv(input_map_file_to_update, header=0, dtype=str, usecols=['MAPPED_IMAGE'])


row_list = []
# walk the root directory tree and select images to process and map
for dir_name, subdir_list, file_list in os.walk(root_dir):
    for file_name in file_list:
        if file_name.lower().endswith(('1.jpg')):
            base_name = file_name[:-5]
            if mapped_images_df['MAPPED_IMAGE'].str.contains(base_name).any():
                # the image has already been mapped, no need to map again
                continue
            mapped_info = map_image(sensor_df, base_name, file_list, root_dir, dir_name, output_dir)
            if not mapped_info:
                print(base_name, 'cannot be mapped', flush=True)
                continue
            row_list.append(mapped_info)

output_df = pd.DataFrame(row_list)
output_df.to_csv(output_file, index=False)
print('DONE')
