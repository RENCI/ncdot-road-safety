import os
import argparse
import pandas as pd


parser = argparse.ArgumentParser(description='Process arguments.')
parser.add_argument('--input_dir', type=str,
                    default='/projects/ncdot/secondary_road/single_image_features/d04',
                    help='the input directory to read dataframes from for combination')
parser.add_argument('--output_file', type=str,
                    default='/projects/ncdot/secondary_road/single_image_features/d04_single_image_features.parquet',
                    help='the output file with path to store combined dataframe')


args = parser.parse_args()
input_dir = args.input_dir
output_file = args.output_file

combined_results = pd.concat([])

res_df_list = [pd.read_parquet(os.path.join(input_dir, f)) for f in os.listdir(input_dir)]
print('total number of files read: ', len(res_df_list))
combined_df = pd.concat(res_df_list)
combined_df.to_parquet(output_file, index=False)
print('done')
