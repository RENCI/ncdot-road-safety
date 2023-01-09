# This script maps images to PathRunner image viewer sensor output to associate images with
# mileposts and lat/longs, use the shape file line segment road characteristics file to
# filter out 4 lane images using mileposts, join left, center, right views of remaining images to
# prepare images for use by annotation tool and active learning
# Command to run the script: python prepare_images_and_metadata.py
import argparse
import os
import pandas as pd
from utils import image_covered, map_image


parser = argparse.ArgumentParser(description='Process arguments.')
parser.add_argument('--input_sensor_file', type=str,
                    default='/projects/ncdot/secondary_road/d1_sensor_output.TXT',
                    help='input sensor output file with path for mapping images to metadata')
parser.add_argument('--skip_initial_2lane_mapping', action='store_true', default=False,
                    help='whether to skip initial mapping for picking out 2 lanes from sensor output')
parser.add_argument('--division', type=int, default=1, help='division for the data')
parser.add_argument('--input_2lane_shape_file', type=str,
                    default='/projects/ncdot/secondary_road/NCRural2LaneSecondaryRoadsInfo.csv',
                    help='input 2 lane road characteristic csv file to pick out 2 lane images')
parser.add_argument('--root_dir', type=str,
                    default='/projects/ncdot/NC_2018_Secondary/d01',
                    help='root directory to look for images to process')
parser.add_argument('--output_file', type=str,
                    default='/projects/ncdot/secondary_road/output/d01/mapped_2lane_sr_images_d1.csv',
                    help='output file for mapped secondary road images')
parser.add_argument('--sensor_output_file_2lane', type=str,
                    default='/projects/ncdot/secondary_road/output/d01/d1_sensor_output_2lane.csv',
                    help='output file for mapped secondary road images')
parser.add_argument('--join_image', action='store_true', default=False,
                    help='if set, prepare joined images; otherwise, prepare symlink to single images')
parser.add_argument('--output_dir', type=str, default='/projects/ncdot/NC_2018_Secondary/single_images/d01',
                    help='output directory for joined images or symlinked single images')

args = parser.parse_args()
input_sensor_file = args.input_sensor_file
input_2lane_shape_file = args.input_2lane_shape_file
output_file = args.output_file
division = args.division
root_dir = args.root_dir
join_image = args.join_image
output_dir = args.output_dir
sensor_output_file_2lane = args.sensor_output_file_2lane
skip_initial_2lane_mapping = args.skip_initial_2lane_mapping


sensor_df = pd.read_csv(input_sensor_file, header=0, dtype=str,
                            usecols=["RouteID", "Set", "Start-MP","Start-Image", "StaLatitude","StaLongitude"])
sensor_df.columns = sensor_df.columns.str.strip()
sensor_df['Start-MP'] = sensor_df['Start-MP'].str.strip()
sensor_df['Start-MP'] = pd.to_numeric(sensor_df['Start-MP'], downcast="float")
sensor_df['RouteID'] = sensor_df['RouteID'].str.strip()
sensor_df['Start-Image'] = sensor_df['Start-Image'].str.strip()
sensor_df['Start-Image'] = sensor_df['Start-Image'].str.replace(':', '')
sensor_df['StaLatitude'] = sensor_df['StaLatitude'].str.strip()
sensor_df['StaLongitude'] = sensor_df['StaLongitude'].str.strip()
sensor_df['Set'] = sensor_df['Set'].str.strip()
print("Before removing duplicate", sensor_df.shape)
sensor_df.drop_duplicates(inplace=True)
print("After removing duplicate", sensor_df.shape)

if not skip_initial_2lane_mapping:
    shape_df = pd.read_csv(input_2lane_shape_file, header=0, dtype={'Division': int,
                                                                    'RouteID': str,
                                                                    'BeginMp1': float,
                                                                    'EndMp1': float},
                           usecols=['Division', 'RouteID', 'BeginMp1', 'EndMp1'])

    print("Before filtering by division: ", shape_df.shape)
    shape_df = shape_df[shape_df['Division'] == division]
    print("After filtering by division: ", shape_df.shape)
    route_list = list(shape_df['RouteID'].unique())
    sensor_df = sensor_df[sensor_df["RouteID"].isin(route_list)]
    print("sensor data after filtering route ids", sensor_df.shape)
    shape_df.set_index('RouteID', inplace=True)
    shape_df.sort_index()
    print("Shape df size after setting and sorting index:", shape_df.shape)

sensor_df['Start-Image'] = sensor_df['Set'] + sensor_df['Start-Image']
sensor_df.drop_duplicates(subset=['RouteID', 'Start-Image'], inplace=True)
print("sensor data after dropping duplicates on RouteID and Start-Image", sensor_df.shape)
sensor_df.drop(columns=['Set'], inplace=True)

if not skip_initial_2lane_mapping:
    sensor_df["Keep"] = sensor_df.apply(lambda row: image_covered(
        shape_df.loc[row['RouteID']], row['Start-MP']), axis=1)

    sensor_df = sensor_df[sensor_df['Keep'] == True]
    sensor_df.drop(columns=['Keep'], inplace=True)
    print("Sensor df size after filtering out non-2 lane images", sensor_df.shape)
    sensor_df.to_csv(sensor_output_file_2lane, index=False)

row_list = []
# walk the root directory tree and select images to process and map
for dir_name, subdir_list, file_list in os.walk(root_dir):
    for file_name in file_list:
        if file_name.lower().endswith(('1.jpg')):
            base_name = file_name[:-5]
            mapped_info = map_image(sensor_df, base_name, file_list, root_dir, dir_name, output_dir,
                                    is_join_image=join_image)
            if not mapped_info:
                print(base_name, 'cannot be mapped', flush=True)
                continue
            row_list.append(mapped_info)
            if len(row_list) % 100000 == 0:
                output_df = pd.DataFrame(row_list)
                output_df.to_csv(f'{output_file}.{len(row_list)}', index=False)
output_df = pd.DataFrame(row_list)
output_df.to_csv(output_file, index=False)
print('DONE')
