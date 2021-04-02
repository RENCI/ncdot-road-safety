import ast
import pandas as pd
import argparse
import numpy as np


div_feature_vector_files = ['/projects/ncdot/NC_2018_Secondary/image_features/d4_image_features.csv',
                            '/projects/ncdot/NC_2018_Secondary/image_features/d8_image_features.csv',
                            '/projects/ncdot/NC_2018_Secondary/image_features/d13_image_features.csv',
                            '/projects/ncdot/NC_2018_Secondary/image_features/d14_image_features.csv']


def get_feature_dataframe_from_csv(input_csv_file, compute_centroid=False, image_subset_col=None):
    df = pd.read_csv(input_csv_file, header=0, index_col=False, usecols=['MAPPED_IMAGE', 'FEATURES'],
                     converters={'FEATURES': ast.literal_eval})
    df.MAPPED_IMAGE = df.MAPPED_IMAGE.str.slice(start=-15)
    df.MAPPED_IMAGE = df.MAPPED_IMAGE.str.replace('.jpg', '')
    if image_subset_col is not None:
        df = df[df.MAPPED_IMAGE.isin(image_subset_col)]
    if compute_centroid:
        cent_vector = np.mean(df.FEATURES.tolist(), axis=0)
        print(df.shape)
        return df, cent_vector
    return df, None


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Process arguments.')
    parser.add_argument('--centroid_input_file', type=str,
                        default='/projects/ncdot/2018/machine_learning/train_image_features_centroid.txt',
                        help='existing training feature vector centroid input file')
    parser.add_argument('--input_count_for_centroid', type=int,
                        default=254206, help='number of instances used to compute centroid in centroid_input_file')
    parser.add_argument('--annot_input_file', type=str,
                        default='/projects/ncdot/NC_2018_Secondary/active_learning/guardrail/round3/annot_data/'
                                'all_user_annots.txt',
                        help='user annotation input file with user annotations to add to existing training data')
    parser.add_argument('--output_file', type=str,
                        default='/projects/ncdot/NC_2018_Secondary/active_learning/guardrail/round3/annot_data/'
                                'train_data_centroid.csv',
                        help='output file that has centroid vector of existing training feature vectors and user '
                             'annotated data')

    args = parser.parse_args()
    centroid_input_file = args.centroid_input_file
    input_count_for_centroid = args.input_count_for_centroid
    annot_input_file = args.annot_input_file
    output_file = args.output_file


    centroid_df = pd.read_csv(centroid_input_file, header=None, index_col=False, converters={0: ast.literal_eval})

    annot_df = pd.read_csv(annot_input_file, header=0, index_col=False, dtype=str, usecols=['Image'])
    annot_df.Image = annot_df.Image.str.slice(start=-15)
    annot_df.Image = annot_df.Image.str.replace('.jpg', '')

    count = input_count_for_centroid
    input_centroid = np.asarray(centroid_df[0][0])
    div_feature_vector_centroids = []
    div_feature_vector_counts = []
    for div_file in div_feature_vector_files:
        div_df, centroid_vector = get_feature_dataframe_from_csv(div_file, compute_centroid=True,
                                                            image_subset_col=annot_df.Image)
        div_feature_vector_centroids.append(np.asarray(centroid_vector))
        div_cnt = len(div_df)
        count += div_cnt
        div_feature_vector_counts.append(div_cnt)

    # compute weighted centroid of input centroid and annotated name centroids for all divisions
    cent_vector = input_count_for_centroid/count * input_centroid
    for i, cent in enumerate(div_feature_vector_centroids):
        cent_vector += div_feature_vector_counts[i]/count * cent

    with open(output_file, 'w') as f:
        f.write('"' + str(cent_vector.tolist()) + '"')
    print('Done')
