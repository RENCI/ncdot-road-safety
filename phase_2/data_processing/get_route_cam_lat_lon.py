import argparse
import pandas as pd


parser = argparse.ArgumentParser(description='input and output parameters')
parser.add_argument('--input_mapping', type=str,
                    default='data/d13_route_40001001011/other/mapped_2lane_sr_images_d13.csv',
                    help='input image mapping csv file')
parser.add_argument('--input_images', type=str,
                    default='data/d13_route_40001001012/route_40001001012_input.csv',
                    help='input csv file that contains all images to get camera lat/lon for')
parser.add_argument('--output_file', type=str,
                    default='data/d13_route_40001001012/route_40001001012_cam_lat_lon.csv',
                    help='output file with image name and corresponding camera lat/lon')


args = parser.parse_args()
input_mapping = args.input_mapping
input_images = args.input_images
output_file = args.output_file

mapping_df = pd.read_csv(input_mapping, usecols=['MAPPED_IMAGE', 'LATITUDE', 'LONGITUDE'])
image_df = pd.read_csv(input_images, usecols=['imageBaseName'])
merge_df = pd.merge(mapping_df, image_df, how='inner', left_on=['MAPPED_IMAGE'], right_on=['imageBaseName'])
merge_df.drop(columns='imageBaseName', inplace=True)
merge_df.to_csv(output_file, index=False)
