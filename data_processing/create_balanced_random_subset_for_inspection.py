import pandas as pd
import argparse


parser = argparse.ArgumentParser(description='Process arguments.')
parser.add_argument('--input_file_1', type=str,
                    default='../server/metadata/model_2lane_predict_d4.csv',
                    help='input file with path for first model prediction')
parser.add_argument('--input_file_2', type=str,
                    default='../server/metadata/model_4lane_predict_d4.csv',
                    help='input file with path for second model prediction')
parser.add_argument('--input_file_exclude', type=str,
                    default='../server/metadata/mapped_2lane_sr_images_d4_subset.csv',
                    help='input file with path to be excluded for subset selection for model prediction inspection')
parser.add_argument('--subset_size', type=int, default=100, help='number of images in the subset')
parser.add_argument('--output_file', type=str,
                    default='../server/metadata/balanced_d4_subset_for_manual_inspection.csv',
                    help='output file for the subset for manual inspection to compare 2 model predictions')

args = parser.parse_args()
input_file_1 = args.input_file_1
input_file_2 = args.input_file_2
input_file_exclude = args.input_file_exclude
subset_size = args.subset_size
output_file = args.output_file

#df_exclude = pd.read_csv(input_file_exclude, header=0, index_col=False, dtype=str, usecols=['MAPPED_IMAGE'])
df1 = pd.read_csv(input_file_1, header=0, index_col=False, dtype={'MAPPED_IMAGE': 'str', 'ROUND_PREDICT_2': 'float'},
                  usecols=['MAPPED_IMAGE', 'ROUND_PREDICT_2'])
df2 = pd.read_csv(input_file_2, header=0, index_col=False, dtype={'MAPPED_IMAGE': 'str', 'ROUND_PREDICT_4': 'float'},
                  usecols=['MAPPED_IMAGE', 'ROUND_PREDICT_4'])
df = pd.merge(df1, df2, on='MAPPED_IMAGE')
print(df.shape)
df['PATH'] = df['MAPPED_IMAGE'].str.slice(stop=-15)
df['MAPPED_IMAGE'] = df['MAPPED_IMAGE'].str.replace('.jpg', '')
df['MAPPED_IMAGE'] = df['MAPPED_IMAGE'].str.split('/').str[-1]
#df = df[~df.MAPPED_IMAGE.isin(df_exclude.MAPPED_IMAGE)]
df_diff = df[df.ROUND_PREDICT_2 != df.ROUND_PREDICT_4]
print(df_diff.shape)
df_diff = df_diff[((df.ROUND_PREDICT_2>=0.5) & (df.ROUND_PREDICT_4<0.5)) | ((df.ROUND_PREDICT_2<0.5) & (df.ROUND_PREDICT_4>=0.5))]
print(df_diff.shape)
#sub_df = df_diff.sample(n=subset_size, random_state=1)
#sub_df.to_csv(output_file, index=False)
print('Done')
