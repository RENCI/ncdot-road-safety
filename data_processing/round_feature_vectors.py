import argparse
import ast
import numpy as np
import dask.dataframe as dd


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Process arguments.')
    parser.add_argument('--input_file', type=str,
                        default='/projects/ncdot/NC_2018_Secondary/image_features/d4_image_features.csv',
                        help='input file to get image feature vectors from')
    parser.add_argument('--output_file', type=str,
                        default='/projects/ncdot/NC_2018_Secondary/image_features/d4_image_features.parquet',
                        help='output file with rounded image feature vectors in parquet format')
    args = parser.parse_args()
    input_file = args.input_file
    output_file = args.output_file


    df = dd.read_csv(input_file, header=0, dtype={'MAPPED_IMAGE': str}, usecols=['MAPPED_IMAGE', 'FEATURES'],
                     converters={'FEATURES': ast.literal_eval})
    out_df = df.map_partitions(lambda sdf: sdf.apply(lambda row: np.round(np.asarray(row.FEATURES), 4), axis=1),
                               meta=('FEATURES', 'float')).compute(scheduler='processes')
    out_df = out_df.drop(columns=['FEATURES'])
    out_df.to_csv(output_file + '.csv')
    out_df.to_parquet(output_file, engine='pyarrow')
