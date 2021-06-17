import os
import argparse
import dask.dataframe as dd
from utils import round_feature


parser = argparse.ArgumentParser(description='Process arguments.')
parser.add_argument('--input_dir', type=str,
                    default='/projects/ncdot/secondary_road/single_image_features/d04',
                    help='the input directory to read dataframes from for combination')
parser.add_argument('--output_file', type=str,
                    default='/projects/ncdot/secondary_road/single_image_features/d04_single_image_features.parquet',
                    help='the output file with path to store combined dataframe')


if __name__ == '__main__':
    args = parser.parse_args()
    input_dir = args.input_dir
    output_file = args.output_file
    res_df_list = [dd.read_parquet(os.path.join(input_dir, f)) for f in os.listdir(input_dir)]
    combined_df = dd.concat(res_df_list)
    combined_df = round_feature(combined_df)
    combined_df.to_parquet(output_file, index=False)

    print('done')
