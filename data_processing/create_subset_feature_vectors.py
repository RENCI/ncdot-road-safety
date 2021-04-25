import ast
import pandas as pd
import argparse
import numpy as np
from compute_centroid_of_features import div_feature_vector_files, get_feature_dataframe


parser = argparse.ArgumentParser(description='Process arguments.')
parser.add_argument('--sim_yes_file', type=str,
                    default='/projects/ncdot/NC_2018_Secondary/active_learning/guardrail/round3/similarity/'
                            'image_sim_yes_20k.csv',
                    help='file with similarities of images closest to positive centroid')
parser.add_argument('--dissim_file', type=str,
                    default='/projects/ncdot/NC_2018_Secondary/active_learning/guardrail/round3/similarity/'
                            'image_dissim_20k.csv',
                    help='file with similarities of images most dissimilar to both positive and negative centroids')
parser.add_argument('--output_file', type=str,
                    default='/projects/ncdot/NC_2018_Secondary/active_learning/guardrail/round3/similarity/'
                            'image_similarity_feature_vectors.csv',
                    help='output file that contain feature vectors for the images from sim_yes_file and dissim_file')


args = parser.parse_args()
sim_yes_file = args.sim_yes_file
dissim_file = args.dissim_file
output_file = args.output_file

np.random.seed(1)
sim_yes_df = pd.read_csv(sim_yes_file, header=0, index_col='MAPPED_IMAGE', dtype=str,
                         usecols=['MAPPED_IMAGE', 'DIVISION'])
sim_yes_df.TYPE = 'YES'
dissim_df = pd.read_csv(dissim_file, header=0, index_col='MAPPED_IMAGE', dtype=str,
                        usecols=['MAPPED_IMAGE', 'DIVISION'])
dissim_df.TYPE = 'DIS'
sub_df = pd.concat([sim_yes_df, dissim_df])
sub_df = sub_df.reset_index()
sub_df['MAPPED_IMAGE'] = sub_df.MAPPED_IMAGE.astype(str)
sub_df.MAPPED_IMAGE=sub_df.MAPPED_IMAGE.str.strip()

df_list = []
for div_file in div_feature_vector_files:
    df = get_feature_dataframe(div_file)
    df = df[df.index.isin(sub_df.MAPPED_IMAGE)]
    df_list.append(df)
whole_df = pd.concat(df_list)
whole_df['FEATURES'] = whole_df.FEATURES.tolist()
print('after filtering: ', whole_df.shape)
whole_df.to_csv(output_file)
print('Done')
