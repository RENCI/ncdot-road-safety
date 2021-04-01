import ast
import pandas as pd
import argparse
import numpy as np


def get_feature_dataframe_from_csv(input_csv_file, compute_centroid=False):
    df = pd.read_csv(input_csv_file, header=0, index_col=False, usecols=['MAPPED_IMAGE', 'FEATURES'],
                     converters={'FEATURES': ast.literal_eval})
    df.MAPPED_IMAGE = df.MAPPED_IMAGE.str.slice(start=-15)
    df.MAPPED_IMAGE = df.MAPPED_IMAGE.str.replace('.jpg', '')
    if compute_centroid:
        cent_vector = np.mean(df.FEATURES.tolist(), axis=0)
        return df, cent_vector
    return df


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Process arguments.')
    parser.add_argument('--train_input_file', type=str,
                        default='../server/metadata/model-related/features/train_image_features.csv',
                        help='input file to get image features in training data')
    parser.add_argument('--output_file', type=str,
                        default='../server/metadata/model-related/features/train_image_features_centroid.csv',
                        help='output file that has centroid vector of the input image features')

    args = parser.parse_args()
    train_input_file = args.train_input_file
    output_file = args.output_file

    train_df, train_df_vector = get_feature_dataframe_from_csv(train_input_file, compute_centroid=True)
    train_df_vector.to_csv(output_file, index=False)
    print('Done')
