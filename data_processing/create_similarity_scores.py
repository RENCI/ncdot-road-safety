import ast
import pandas as pd
import argparse
import numpy as np
from compute_centroid_of_features import div_feature_vector_files, get_feature_dataframe_from_csv


# Get cosine similarity between feature vectors A and B using cosine similarity
def get_cosine_similarity(A, B):
    cos_similarity = np.dot(A,B.T) / (np.linalg.norm(A)*np.linalg.norm(B))
    return cos_similarity


parser = argparse.ArgumentParser(description='Process arguments.')
parser.add_argument('--centroid_yes_input_file', type=str,
                    default='/projects/ncdot/NC_2018_Secondary/active_learning/guardrail/round3/annot_data/'
                            'train_data_centroid_yes.csv',
                    help='existing positive training feature vector centroid input file')
parser.add_argument('--centroid_no_input_file', type=str,
                    default='/projects/ncdot/NC_2018_Secondary/active_learning/guardrail/round3/annot_data/'
                            'train_data_centroid_no.csv',
                    help='existing negative training feature vector centroid input file')
parser.add_argument('--remain_image_name_file', type=str,
                    default='/projects/ncdot/NC_2018_Secondary/active_learning/guardrail/round3/annot_data/'
                            'remain_image_base_names.csv',
                    help='input image base names remaining to create uncertainty scores for')
parser.add_argument('--output_file', type=str,
                    default='/projects/ncdot/NC_2018_Secondary/active_learning/guardrail/round3/'
                            'image_similarity_scores.csv',
                    help='output file for similarity scores of the mapped images to training data centroids '
                         'to compute uncertainty scores')


args = parser.parse_args()
centroid_yes_input_file = args.centroid_yes_input_file
centroid_no_input_file = args.centroid_no_input_file
remain_image_name_file = args.remain_image_name_file
output_file = args.output_file

np.random.seed(1)
centroid_yes_df = pd.read_csv(centroid_yes_input_file, header=None, index_col=False, converters={0: ast.literal_eval})
centroid_no_df = pd.read_csv(centroid_no_input_file, header=None, index_col=False, converters={0: ast.literal_eval})
remain_image_df = pd.read_csv(remain_image_name_file, header=0, dtype=str, index_col=['MAPPED_IMAGE'])

df_list = []

for div_file in div_feature_vector_files:
    df = get_feature_dataframe_from_csv(div_file)
    df_list.append(df)
whole_df = pd.concat(df_list)
print('before filtering: ', whole_df.shape)
whole_df = remain_image_df.join(whole_df)
print('after filtering: ', whole_df.shape)
centroid_yes_vec = np.asarray(centroid_yes_df[0][0])
centroid_no_vec = np.asarray(centroid_no_df[0][0])
whole_df['SIMILARITY_YES'] = whole_df.apply(lambda row: get_cosine_similarity(np.asarray(row['FEATURES']),
                                                                              centroid_yes_vec),
                                            axis=1)
whole_df['SIMILARITY_NO'] = whole_df.apply(lambda row: get_cosine_similarity(np.asarray(row['FEATURES']),
                                                                             centroid_no_vec),
                                           axis=1)
whole_df.drop(columns=['FEATURES'], inplace=True)
whole_df = whole_df.sort_values(by=['SIMILARITY_YES', 'SIMILARITY_NO'])
whole_df.to_csv(output_file, index=False)
whole_size = len(whole_df)
# uncertainty reflects sorting by SCORE
whole_df["UNCERTAINTY"] = whole_df.apply(lambda row: whole_size - whole_df.index.get_loc(row.name), axis=1)
whole_df.to_csv(output_file, index=False)
print('Done')
