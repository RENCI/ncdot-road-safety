# This script maps images to PathRunner image viewer sensor output to associate images with
# mileposts and lat/longs, use the shape file line segment road characteristics file to
# filter out 4 lane images using mileposts, join left, center, right views of remaining images to
# prepare images for use by annotation tool and active learning
# Command to run the script: python prepare_images_and_metadata.py
# Command run example: python output_image_path.py /projects/ncdot/2018/machine_learning/data
# /projects/ncdot/2018/machine_learning/output/guardrail_image_path.txt
import argparse
import os
import pandas as pd
from PIL import Image


def image_covered(ref_data, mile_post):
    if isinstance(ref_data, pd.Series):
        mp1 = min(ref_data['BeginMp1'], ref_data['EndMp1'])
        mp2 = max(ref_data['BeginMp1'], ref_data['EndMp1'])
        if mp1 <= mile_post <= mp2:
            return True
        else:
            return False
    else: # DataFrame
        intervals = list(zip(ref_data['BeginMp1'], ref_data['EndMp1']))
        for start, stop in intervals:
            if start <= mile_post <= stop or stop <= mile_post <= start:
                return True
        return False


def join_images(left_image_path, front_image_path, right_image_path):
    img_names = [left_image_path, front_image_path, right_image_path]
    imgs = []
    try:
        for idx in range(3):
            imgs.append(Image.open(img_names[idx]))

        dest_img = Image.new('RGB', (imgs[0].width+imgs[1].width+imgs[2].width, imgs[0].height))

        dest_img.paste(imgs[0], (0, 0))
        dest_img.paste(imgs[1], (imgs[0].width, 0))
        dest_img.paste(imgs[2], (imgs[0].width+imgs[1].width, 0))
        return dest_img
    except OSError as ex:
        print(left_image_path, str(ex))
        return None


parser = argparse.ArgumentParser(description='Process arguments.')
parser.add_argument('--input_sensor_file', type=str,
                    default='/projects/ncdot/secondary_road/d4_sensor_output.txt',
                    help='input sensor output file with path for mapping images to metadata')
parser.add_argument('--division', type=int, default=4, help='division for the data')
parser.add_argument('--input_2lane_shape_file', type=str,
                    default='/projects/ncdot/secondary_road/NCRural2LaneSecondaryRoadsInfo.csv',
                    help='input 2 lane road characteristic csv file to pick out 2 lane images')
parser.add_argument('--root_dir', type=str,
                    default='/projects/ncdot/NC_2018_Secondary/d04',
                    help='root directory to look for images to process')
parser.add_argument('--output_file', type=str, default='../server/metadata/mapped_2lane_sr_images.csv',
                    help='output file for mapped secondary road images')
parser.add_argument('--output_dir', type=str, default='/projects/ncdot/NC_2018_Secondary/images/d4',
                    help='output directory for copying joined 2 lane images')

args = parser.parse_args()
input_sensor_file = args.input_sensor_file
input_2lane_shape_file = args.input_2lane_shape_file
output_file = args.output_file
division = args.division
root_dir = args.root_dir
output_dir = args.output_dir

sensor_df = pd.read_csv(input_sensor_file, header=0, dtype=str, usecols=["RouteID", "SET", "Start-MP",
                                                                         "Start-Image", "StaLatitude",
                                                                         "StaLongitude"])
sensor_df.columns = sensor_df.columns.str.strip()
sensor_df['Start-MP'] = sensor_df['Start-MP'].str.strip()
sensor_df['RouteID'] = sensor_df['RouteID'].str.strip()
sensor_df['Start-Image'] = sensor_df['Start-Image'].str.strip().replace(':', '')
sensor_df['StaLatitude'] = sensor_df['StaLatitude'].str.strip()
sensor_df['StaLongitude'] = sensor_df['StaLongitude'].str.strip()
sensor_df['SET'] = sensor_df['SET'].str.strip()
sensor_df['Start-MP'].astype(float)
print("Before removing duplicate", sensor_df.shape)
sensor_df.drop_duplicates(inplace=True)
print("After removing duplicate", sensor_df.shape)

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
sensor_df['Start-Image'] = sensor_df['SET'] + sensor_df['Start-Image']
sensor_df.drop_duplicates(subset=['RouteID', 'Start-Image'], inplace=True)
print("sensor data after dropping duplicates on index rows", sensor_df.shape)
sensor_df = sensor_df.set_index(['RouteID', 'Start-Image']).sort_index()
print("sensor data after setting index: ", sensor_df.shape)
sensor_df.drop_duplicates(ignore_index=False)
print("sensor data after removing duplicates on index: ", sensor_df.shape)

shape_df.set_index('RouteID', inplace=True)
shape_df.sort_index()
print("Shape df size after setting and sorting index:", shape_df.shape)

sensor_df["Keep"] = sensor_df.apply(lambda row: image_covered(
    shape_df.loc[row['ROUTEID']],
    sensor_df.loc[row['ROUTEID'], row['Start-Image']].at['Start-MP']), axis=1)

sensor_df = sensor_df[sensor_df['Keep'] == True]
sensor_df.drop(columns=['Keep'])
print("Sensor df size after filtering out non-2 lane images", sensor_df.shape)

row_list = []
# walk the root directory tree and select images to process and map
for dir_name, subdir_list, file_list in os.walk(root_dir):
    for file_name in file_list:
        if file_name.lower().endswith(('1.jpg')):
            base_name = file_name[:-5]
            file_name2 = f'{base_name}2.jpg'
            file_name5 = f'{base_name}5.jpg'
            if file_name2 not in file_list or file_name5 not in file_list:
                continue
            base_df = sensor_df[sensor_df['Start-Image'] == base_name]
            if base_df.empty:
                base_name_int = int(base_name)
                if base_name.endswith('01'):
                    base_name_next = str(base_name_int + 1)
                else:
                    base_name_next = str(base_name_int - 1)
                base_df = sensor_df[sensor_df['Start-Image'] == base_name_next]
                if base_df.empty:
                    # cannot be mapped
                    continue

            front = os.path.join(dir_name, file_name)
            left = os.path.join(dir_name, file_name5)
            right = os.path.join(dir_name, file_name2)
            dst_img = join_images(left, front, right)
            if dst_img:
                idx = dir_name.index(root_dir) + len(root_dir)
                rel_input_dir = dir_name[idx:]
                if rel_input_dir.startswith('/') or rel_input_dir.startswith('\\'):
                    rel_input_dir = rel_input_dir[1:]
                target_dir = os.path.join(output_dir, rel_input_dir)
                os.makedirs(target_dir, exist_ok=True)
                target = os.path.join(target_dir, f'{base_name}.jpg')
                dst_img.save(target)
                row_list.append({'ROUTEID': base_df['RouteID'].values[0],
                                 'MAPPED_IMAGE': base_name,
                                 'LATITUDE': base_df['StaLatitude'].values[0],
                                 'LONGITUDE': base_df['StaLongitude'].values[0],
                                 'MILE_POST': base_df['Start-MP'].values[0],
                                 'PATH': target_dir})
output_df = pd.DataFrame(row_list)
output_df.to_csv(output_file, index=False)
print('DONE')
