import ast
import pandas as pd
import argparse
import numpy as np


div_feature_vector_files = ['/projects/ncdot/NC_2018_Secondary/image_features/d4_image_features.parquet',
                            '/projects/ncdot/NC_2018_Secondary/image_features/d8_image_features.parquet',
                            '/projects/ncdot/NC_2018_Secondary/image_features/d13_image_features.parquet',
                            '/projects/ncdot/NC_2018_Secondary/image_features/d14_image_features.parquet']


def get_feature_dataframe(input_file, compute_centroid=False, image_subset_yes_df=None, image_subset_no_df=None):
    if input_file.endswith('.csv'):
        df = pd.read_csv(input_file, header=0, index_col='MAPPED_IMAGE', dtype={'MAPPED_IMAGE': str},
                         engine='c', low_memory=False, memory_map=True,
                         usecols=['MAPPED_IMAGE', 'FEATURES'],
                         converters={'FEATURES': ast.literal_eval})
    elif input_file.endswith('.parquet'):
        df = pd.read_parquet(input_file, columns=['MAPPED_IMAGE', 'FEATURES'])
        df = df.set_index('MAPPED_IMAGE')
    else:
        raise NotImplementedError(f'{input_file} is not csv or parquet file, exiting')
    df.index = df.index.str.slice(start=-15)
    df.index = df.index.str.replace('.jpg', '')
    print('total size of division:', df.shape, flush=True)
    if image_subset_yes_df is not None:
        df_yes = image_subset_yes_df.join(df)
        print('positive size of division:', df_yes.shape, flush=True)
    if image_subset_no_df is not None:
        df_no = image_subset_no_df.join(df)
        print('negative size of division:', df_no.shape, flush=True)
    if image_subset_yes_df is None and image_subset_no_df is None:
        if compute_centroid:
            cent_vec = np.mean(df.FEATURES.tolist(), axis=0)
            return df, cent_vec
        else:
            return df
    elif image_subset_yes_df is None: # image_subset_no_col is not None
        if compute_centroid:
            cent_vec = np.mean(df_no.FEATURES.tolist(), axis=0)
            return df_no, cent_vec
        else:
            return df_no
    elif image_subset_no_df is None: # image_subset_yes_col is not None
        cent_vec = np.mean(df_yes.FEATURES.tolist(), axis=0)
        if compute_centroid:
            return df_yes, cent_vec
        else:
            return df_yes
    else: # both image_subset_yes_col and image_subset_no_col are not None
        if compute_centroid:
            cent_no_vector = np.mean(df_no.FEATURES.tolist(), axis=0)
            cent_yes_vector = np.mean(df_yes.FEATURES.tolist(), axis=0)
            return df_yes, df_no, cent_yes_vector, cent_no_vector
        else:
            return df_yes, df_no


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Process arguments.')
    parser.add_argument('--centroid_yes_input_file', type=str,
                        default='/projects/ncdot/2018/machine_learning/train_image_features_centroid_yes.csv',
                        help='existing training feature vector centroid positive input file')
    parser.add_argument('--centroid_no_input_file', type=str,
                        default='/projects/ncdot/2018/machine_learning/train_image_features_centroid_no.csv',
                        help='existing training feature vector centroid negative input file')
    parser.add_argument('--input_count_for_centroid_yes', type=int,
                        default=127103, help='number of positive instances used to compute centroid in '
                                             'centroid_yes_input_file')
    parser.add_argument('--input_count_for_centroid_no', type=int,
                        default=127103, help='number of negative instances used to compute centroid in '
                                             'centroid_no_input_file')
    parser.add_argument('--annot_input_file', type=str,
                        default='/projects/ncdot/NC_2018_Secondary/active_learning/guardrail/round4/annot_data/'
                                'all_user_annots_train.csv',
                        help='user annotation input file with user annotations to add to existing training data')
    parser.add_argument('--output_yes_file', type=str,
                        default='/projects/ncdot/NC_2018_Secondary/active_learning/guardrail/round4/annot_data/'
                                'train_data_centroid_yes.csv',
                        help='output file that has centroid vector of positive existing training feature vectors '
                             'and user annotated data')
    parser.add_argument('--output_no_file', type=str,
                        default='/projects/ncdot/NC_2018_Secondary/active_learning/guardrail/round4/annot_data/'
                                'train_data_centroid_no.csv',
                        help='output file that has centroid vector of negative existing training feature vectors '
                             'and user annotated data')
    args = parser.parse_args()
    centroid_yes_input_file = args.centroid_yes_input_file
    centroid_no_input_file = args.centroid_no_input_file
    input_count_for_centroid_yes = args.input_count_for_centroid_yes
    input_count_for_centroid_no = args.input_count_for_centroid_no
    annot_input_file = args.annot_input_file
    output_yes_file = args.output_yes_file
    output_no_file = args.output_no_file
    centroid_yes_df = pd.read_csv(centroid_yes_input_file, header=None, index_col=False,
                                  converters={0: ast.literal_eval})
    centroid_no_df = pd.read_csv(centroid_no_input_file, header=None, index_col=False,
                                  converters={0: ast.literal_eval})
    annot_df = pd.read_csv(annot_input_file, header=0, index_col='Image', dtype=str, usecols=['Image', 'Presence'])
    annot_df['DIVISION'] = annot_df.index.str.split('/').str[0]
    annot_df.index = annot_df.index.str.slice(start=-15)
    annot_df.index = annot_df.index.str.replace('.jpg', '')
    annot_df_divs = [
        annot_df[annot_df.DIVISION == 'd04'],
        annot_df[annot_df.DIVISION == 'd08'],
        annot_df[annot_df.DIVISION == 'd13'],
        annot_df[annot_df.DIVISION == 'd14']
    ]
    count_yes = input_count_for_centroid_yes
    count_no = input_count_for_centroid_no
    input_centroid_yes = np.asarray(centroid_yes_df[0][0])
    input_centroid_no = np.asarray(centroid_no_df[0][0])
    div_feature_vector_yes_centroids = []
    div_feature_vector_no_centroids = []
    div_feature_vector_yes_counts = []
    div_feature_vector_no_counts = []
    for i, div_file in enumerate(div_feature_vector_files):
        div_df_yes, div_df_no, centroid_vector_yes, centroid_vector_no = get_feature_dataframe(
            div_file, compute_centroid=True,
            image_subset_yes_df=annot_df_divs[i][annot_df_divs[i].Presence == 'True'],
            image_subset_no_df=annot_df_divs[i][annot_df_divs[i].Presence == 'False']
        )
        div_feature_vector_yes_centroids.append(np.asarray(centroid_vector_yes))
        div_feature_vector_no_centroids.append(np.asarray(centroid_vector_no))
        div_yes_cnt = len(div_df_yes)
        div_no_cnt = len(div_df_no)
        count_yes += div_yes_cnt
        count_no += div_no_cnt
        div_feature_vector_yes_counts.append(div_yes_cnt)
        div_feature_vector_no_counts.append(div_no_cnt)

    # compute weighted centroid of input centroid and annotated name centroids for all divisions
    cent_vector_yes = input_count_for_centroid_yes/count_yes * input_centroid_yes
    cent_vector_no = input_count_for_centroid_no / count_no * input_centroid_no
    for i, cent in enumerate(div_feature_vector_yes_centroids):
        cent_vector_yes += div_feature_vector_yes_counts[i]/count_yes * cent
    for i, cent in enumerate(div_feature_vector_no_centroids):
        cent_vector_no += div_feature_vector_no_counts[i]/count_no * cent

    with open(output_yes_file, 'w') as f:
        f.write('"' + str(cent_vector_yes.tolist()) + '"')
    with open(output_no_file, 'w') as f:
        f.write('"' + str(cent_vector_no.tolist()) + '"')
    print(f'count_yes:{count_yes}, count_no:{count_no}')
    print('Done')
