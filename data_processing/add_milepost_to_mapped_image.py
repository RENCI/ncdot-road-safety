import argparse
import pandas as pd


parser = argparse.ArgumentParser(description='Process arguments.')
parser.add_argument('--input_mapped_image_file', type=str,
                    default='../server/metadata/sensor_data_mapped_unique_3584576.csv',
                    help='input mapped image file with path for getting mapped images')
parser.add_argument('--input_sensor_output_file', type=str, default='../server/metadata/SensorFieldExportNew.csv',
                    help='input sensor output file with path for mapping images to mileposts')
parser.add_argument('--output_file', type=str, default='../server/metadata/mapped_images_with_milepost.csv',
                    help='output file for mapped images with milepost')

args = parser.parse_args()

input_mapped_image_file = args.input_mapped_image_file
input_sensor_output_file = args.input_sensor_output_file
output_file = args.output_file

route_id_file = '../server/metadata/route_ids_with_2_lanes.csv'
route_df = pd.read_csv(route_id_file, header=0, dtype=str)
print(route_df.shape)
route_list = list(route_df['RouteID'])

image_df = pd.read_csv(input_mapped_image_file, header=0, dtype=str, usecols=["ROUTEID", "SET", "IMAGE",
                                                                              "MAPPED_IMAGE"])
image_df = image_df[image_df["ROUTEID"].isin(route_list)]
print("image data after filtering route ids", image_df.shape)

sensor_df = pd.read_csv(input_sensor_output_file, header=0, dtype=str, usecols=['RouteID', 'Set', 'Start-Mi',
                                                                                'Start-Image'])
sensor_df.columns = sensor_df.columns.str.strip()
sensor_df['Start-Mi'] = sensor_df['Start-Mi'].str.strip()
sensor_df['RouteID'] = sensor_df['RouteID'].str.strip()
sensor_df['Start-Image'] = sensor_df['Start-Image'].str.strip()
sensor_df.drop_duplicates(inplace=True)
print("After removing duplicate", sensor_df.shape)
sensor_df = sensor_df[sensor_df["RouteID"].isin(route_list)]
print("sensor data after filtering route ids", sensor_df.shape)
sensor_df.drop_duplicates(subset=['RouteID', 'Set', 'Start-Image'], inplace=True)
print("sensor data after dropping duplicates on index rows", sensor_df.shape)
sensor_df = sensor_df.set_index(['RouteID', 'Set', 'Start-Image']).sort_index()
print("sensor data after setting index: ", sensor_df.shape)
sensor_df.drop_duplicates(ignore_index=False)
print("sensor data after removing duplicates on index: ", sensor_df.shape)

image_df["MILEPOST"] = image_df.apply(lambda row: sensor_df.loc[row['ROUTEID'], row['SET'], row['IMAGE']].at['Start-Mi'], axis=1)
image_df.to_csv(output_file, index=False)
print('DONE')
