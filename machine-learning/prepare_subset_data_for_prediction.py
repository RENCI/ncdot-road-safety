import os
import pandas as pd
import argparse
from utils import sym_link_single_image


parser = argparse.ArgumentParser(description='Process arguments.')
parser.add_argument('--input_file', type=str,
                    default='/projects/ncdot/NC_2018_Secondary/active_learning/pole/round0/data_info/'
                            'ncdot_pole_annotations.csv',
                    help='subset input file with path')
parser.add_argument('--filter_file', type=str,
                    default='/projects/ncdot/NC_2018_Secondary/active_learning/pole/round2/annot_data/'
                            'remain_image_base_names_pole.csv',
                    help='filter image base names to filter input file')
parser.add_argument('--target_dir', type=str,
                    default='/projects/ncdot/NC_2018_Secondary/active_learning/pole/round2/sample_data/',
                    help='target directory to create subset data in')


args = parser.parse_args()
input_file = args.input_file
filter_file = args.filter_file
target_dir = args.target_dir

df = pd.read_csv(input_file, header=0, index_col=False, dtype=str, usecols=['MAPPED_IMAGE', 'PATH'])
# remove the last 5 character before .jpg from path
df.PATH = df.PATH.str[:-5] + '.jpg'
print('original input df:', df.shape)
df_filter = pd.read_csv(filter_file, header=0, index_col=False, dtype=str, usecols=['MAPPED_IMAGE'])
print('filter df:', df.shape)
df = df[df.MAPPED_IMAGE.isin(df_filter.MAPPED_IMAGE)]
print('original file after filtering', df.shape)

df.apply(lambda row: sym_link_single_image(row['PATH'], os.path.join(target_dir, row['MAPPED_IMAGE'])), axis=1)
print('Done')
