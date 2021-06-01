import os
import pandas as pd
import argparse
from utils import sym_link_single_image


parser = argparse.ArgumentParser(description='Process arguments.')
parser.add_argument('--input_file', type=str,
                    default='/projects/ncdot/NC_2018_Secondary/active_learning/guardrail/round0/predict/'
                            'model_2lane_predict_d13.csv',
                    help='input file that contains joined image path')
parser.add_argument('--source_dir', type=str,
                    default='/projects/ncdot/NC_2018_Secondary',
                    help='target directory to create single image data in')
parser.add_argument('--target_dir', type=str,
                    default='/projects/ncdot/NC_2018_Secondary/single_images',
                    help='target directory to create single image data in')


args = parser.parse_args()
input_file = args.input_file
source_dir = args.source_dir
target_dir = args.target_dir

df = pd.read_csv(input_file, header=0, index_col=False, dtype=str, usecols=['MAPPED_IMAGE'])
print(df.shape)

df.apply(lambda row: sym_link_single_image(os.path.join(source_dir, row['MAPPED_IMAGE']),
                                           os.path.join(target_dir, row['MAPPED_IMAGE'])), axis=1)
print('Done')
