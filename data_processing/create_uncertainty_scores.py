import pandas as pd
import argparse
import numpy as np
import matplotlib.pyplot as plt


parser = argparse.ArgumentParser(description='Process arguments.')
parser.add_argument('--input_file_d4', type=str,
                    default='../server/metadata/model-related/secondary_road/model_2lane_predict_d4.csv',
                    help='input prediction file for mapped images to create uncertainty scores for')
parser.add_argument('--input_file_d8', type=str,
                    default='../server/metadata/model-related/secondary_road/model_2lane_predict_d8.csv',
                    help='input prediction file for mapped images to create uncertainty scores for')
parser.add_argument('--input_file_d13', type=str,
                    default='../server/metadata/model-related/secondary_road/model_2lane_predict_d13.csv',
                    help='input prediction file for mapped images to create uncertainty scores for')
parser.add_argument('--input_file_d14', type=str,
                    default='../server/metadata/model-related/secondary_road/model_2lane_predict_d14.csv',
                    help='input prediction file for mapped images to create uncertainty scores for')
parser.add_argument('--sample_size', type=int,
                    default=20000,
                    help='sample size for manual annotation with uncertainty scores computed to be ingested into db')
parser.add_argument('--output_file', type=str,
                    default='../server/metadata/image_uncertainty_scores.csv',
                    help='output file for uncertainty scores of the mapped images to ingest into annotation tool db')


args = parser.parse_args()
input_file_d4 = args.input_file_d4
input_file_d8 = args.input_file_d8
input_file_d13 = args.input_file_d13
input_file_d14 = args.input_file_d14
sample_size = args.sample_size
output_file = args.output_file

df_d4 = pd.read_csv(input_file_d4, header=0, index_col=['MAPPED_IMAGE'], usecols=['MAPPED_IMAGE', 'ROUND_PREDICT'],
                    dtype={'MAPPED_IMAGE': str, 'ROUND_PREDICT': float})
df_d8 = pd.read_csv(input_file_d8, header=0, index_col=['MAPPED_IMAGE'], usecols=['MAPPED_IMAGE', 'ROUND_PREDICT'],
                    dtype={'MAPPED_IMAGE': str, 'ROUND_PREDICT': float})
df_d13 = pd.read_csv(input_file_d13, header=0, index_col=['MAPPED_IMAGE'], usecols=['MAPPED_IMAGE', 'ROUND_PREDICT'],
                     dtype={'MAPPED_IMAGE': str, 'ROUND_PREDICT': float})
# df_d14 = pd.read_csv(input_file_d14, header=0, index_col=['MAPPED_IMAGE'], usecols=['MAPPED_IMAGE', 'ROUND_PREDICT'],
#                    dtype={'MAPPED_IMAGE': str, 'ROUND_PREDICT': float})
# print(df_d4.shape, df_d8.shape, df_d13.shape, df_d14.shape)
df_d4['DIVISION_WEIGHT'] = 1
df_d8['DIVISION_WEIGHT'] = 1
df_d13['DIVISION_WEIGHT'] = 1.5
df = pd.concat([df_d4, df_d8, df_d13])
print(df.shape)
# plt.hist(df['ROUND_PREDICT'], bins=10)
# plt.show()

# drop negative predictions
df_yes = df[df.ROUND_PREDICT >= 0.5]
print(f'positive predictions: {df_yes.shape}')
plt.hist(df_yes['ROUND_PREDICT'], bins=5, log=True)
plt.show()
hist, bin_edges = np.histogram(df_yes['ROUND_PREDICT'], bins=5, density=True)
bin_edges[5] = 1.1
print(f'bins: {bin_edges}, hists: {hist}')

df_yes['BIN_INDEX'] = np.digitize(df_yes['ROUND_PREDICT'], bin_edges)
# create random sampling with the same distribution as positive prediction data while giving west regions
# such as division 13 more weight
df_yes['WEIGHT'] = hist[df_yes['BIN_INDEX'] - 1] * df_yes['DIVISION_WEIGHT']
sub_df = df_yes.sample(n=sample_size, weights='WEIGHT', replace=False, random_state=1)
plt.hist(sub_df['ROUND_PREDICT'], bins=[0.5, 0.6, 0.7, 0.8, 0.9, 1], log=True)
plt.show()
# print(sub_df[sub_df['DIVISION_WEIGHT'] == 1.5])
# print(sub_df[sub_df['DIVISION_WEIGHT'] == 1])
sub_df = sub_df.drop(columns=['BIN_INDEX', 'WEIGHT'])
# uncertainty would be in the range of [0.1, 0.6]
# where predict probability of 0.5 has higher uncertainty than
# predict probability of 1.0
sub_df['UNCERTAINTY'] = 1.1 - sub_df['ROUND_PREDICT']
sub_df['UNCERTAINTY'] = np.round(sub_df['UNCERTAINTY'], decimals=2)
print(len(sub_df[sub_df['UNCERTAINTY'] > 0.2 ]))
sub_df.index = sub_df.index.str.slice(start=-15)
sub_df.index = sub_df.index.str.replace('.jpg', '')
sub_df = sub_df.sort_values(by=['UNCERTAINTY'])
sub_df.to_csv(output_file)
print('Done')
