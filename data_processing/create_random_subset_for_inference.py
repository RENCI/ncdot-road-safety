import pandas as pd
import argparse
import os


parser = argparse.ArgumentParser(description='Process arguments.')
parser.add_argument('--input_file', type=str,
                    default='/projects/ncdot/secondary_road/mapped_2lane_sr_images_d4.csv',
                    help='input file with path for mapped images to create random subset from')
parser.add_argument('--root_dir', type=str,
                    default='/projects/ncdot/NC_2018_Secondary/images/d4_symlink_subset',
                    help='root directory to create symlinked random subset in')
parser.add_argument('--subset_size', type=int, default=100, help='number of images in the subset')
parser.add_argument('--output_file', type=str,
                    default='/projects/ncdot/secondary_road/mapped_2lane_sr_images_d4_subset.csv',
                    help='output file for the subset mapped secondary road images')

args = parser.parse_args()
input_file = args.input_file
subset_size = args.subset_size
output_file = args.output_file
root_dir = args.root_dir

df = pd.read_csv(input_file, header=0, index_col=False, dtype=str)
print(df.shape)
sub_df = df.sample(n=subset_size, random_state=1)
print(sub_df.shape)
sub_df.apply(lambda row: os.symlink('{}/{}.jpg'.format(row['PATH'], row['MAPPED_IMAGE']),
                                    '{}/{}.jpg'.format(root_dir, row['MAPPED_IMAGE'])))
sub_df.drop(['ROUTEID', 'LATITUDE', 'LONGITUDE', 'MILE_POST'], axis = 1)
sub_df.to_csv(output_file, index=False)
print('Done')
