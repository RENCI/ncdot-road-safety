import argparse
import pandas as pd


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Process arguments.')
    parser.add_argument('--input_file', type=str,
                        default='/projects/ncdot/secondary_road/single_image_features/d04_single_image_features.parquet',
                        help='input file to get image feature vectors from')
    parser.add_argument('--output_file1', type=str,
                        default='/projects/ncdot/secondary_road/single_image_features/d04_single_image_features1.parquet',
                        help='output file with first half of the input data frame in parquet format')
    parser.add_argument('--output_file2', type=str,
                        default='/projects/ncdot/secondary_road/single_image_features/d04_single_image_features2.parquet',
                        help='output file with last half of the input data frame in parquet format')
    parser.add_argument('half_size', type=int, default=1112214, help='middle index number to separate input '
                                                                     'dataframe into two')
    args = parser.parse_args()
    input_file = args.input_file
    output_file1 = args.output_file1
    output_file2 = args.output_file2
    half_size = args.half_size

    df = pd.read_parquet(input_file, engine='fastparquet')
    df1 = df.iloc[:half_size, :]
    df1.to_parquet(output_file1, index=False)
    df = df.iloc[half_size:, :]
    df.to_parquet(output_file2, index=False)
