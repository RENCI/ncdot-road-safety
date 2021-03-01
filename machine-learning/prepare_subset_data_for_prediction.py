import pandas as pd
import argparse
import os


parser = argparse.ArgumentParser(description='Process arguments.')
parser.add_argument('--input_file', type=str,
                    default='/projects/ncdot/secondary_road/mapped_2lane_sr_images_d4_subset_300.csv',
                    help='subset input file with path')
parser.add_argument('--target_dir', type=str,
                    default='/projects/ncdot/NC_2018_Secondary/subset_data/',
                    help='target directory to create subset data in')


args = parser.parse_args()
input_file = args.input_file
target_dir = args.target_dir

df = pd.read_csv(input_file, header=0, index_col=False, dtype=str, usecols=['MAPPED_IMAGE', 'PATH'])
df['MAPPED_IMAGE'] = df['MAPPED_IMAGE'] + '.jpg'
df['PATH'] = df['PATH'].str.replace('/projects/ncdot/NC_2018_Secondary/images/d4',
                                    '/projects/ncdot/NC_2018_Secondary/images/d04')
df['PATH'] = df['PATH'] + '/' + df['MAPPED_IMAGE']

print(df.shape)


def prepare_image(src, dst):
    dst_path = os.path.dirname(dst)
    os.makedirs(dst_path, exist_ok=True)
    os.symlink(src, dst)
    return

df.apply(lambda row: prepare_image(row['PATH'], target_dir + row['MAPPED_IMAGE']), axis=1)
print('Done')
