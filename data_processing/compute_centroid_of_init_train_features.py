import ast
import pandas as pd
import argparse
import numpy as np


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Process arguments.')
    parser.add_argument('--input_file', type=str,
                        default='/projects/ncdot/2018/machine_learning/train_image_features.csv',
                        help='existing training feature vector input file')
    parser.add_argument('--output_file_yes', type=str,
                        default='/projects/ncdot/2018/machine_learning/train_image_features_centroid_yes.csv',
                        help='output file that has centroid vector of positive existing training feature vectors')
    parser.add_argument('--output_file_no', type=str,
                        default='/projects/ncdot/2018/machine_learning/train_image_features_centroid_no.csv',
                        help='output file that has centroid vector of negative existing training feature vectors')

    args = parser.parse_args()
    input_file = args.input_file
    output_file_yes = args.output_file_yes
    output_file_no = args.output_file_no

    df = pd.read_csv(input_file, header=0, index_col=False, usecols=['MAPPED_IMAGE', 'FEATURES'],
                     converters={'FEATURES': ast.literal_eval})
    df.MAPPED_IMAGE = df.MAPPED_IMAGE.str.replace('/projects/ncdot/2018/machine_learning/data_2lanes/train_features/',
                                                  '')
    df.CLASS = df.MAPPED_IMAGE.str.split('/').str[0]
    df.MAPPED_IMAGE = df.MAPPED_IMAGE.str.slice(start=-15)
    df.MAPPED_IMAGE = df.MAPPED_IMAGE.str.replace('.jpg', '')
    df_yes = df[df.CLASS == 'yes']
    df_no = df[df.CLASS == 'no']
    print(df_yes.shape, df_no.shape)
    cent_vector_yes = np.mean(df_yes.FEATURES.tolist(), axis=0)
    cent_vector_no = np.mean(df_no.FEATURES.tolist(), axis=0)

    with open(output_file_yes, 'w') as f:
        f.write('"' + str(cent_vector_yes.tolist()) + '"')
    with open(output_file_no, 'w') as f:
        f.write('"' + str(cent_vector_no.tolist()) + '"')
    print('Done')
