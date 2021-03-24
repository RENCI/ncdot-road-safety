import pandas as pd
import argparse


parser = argparse.ArgumentParser(description='Process arguments.')
parser.add_argument('--label_file', type=str,
                    default='../server/metadata/holdout_test/user_annotated_balanced_image_info_d4.csv',
                    help='labelled guardrail data obtained from guardrail survey data')
parser.add_argument('--predict_label_file', type=str,
                    default='../server/metadata/model_predict_test_base.csv',
                    help='predicted guardrail lable data from first model')
parser.add_argument('--predict_label_file2', type=str,
                    default='../server/metadata/model_predict_test_round1.csv',
                    help='predicted guardrail model lable data from second model')
parser.add_argument('--predict_label_file3', type=str,
                    default='../server/metadata/model_predict_test_round2.csv',
                    help='predicted guardrail model lable data from second model')
parser.add_argument('--output_file', type=str,
                    default='../server/metadata/model_2lane_predict_d4_with_manual_labels_3_models.csv',
                    help='output file with combined annotations and two model predictions')

args = parser.parse_args()
label_file = args.label_file
predict_label_file = args.predict_label_file
predict_label_file2 = args.predict_label_file2
predict_label_file3 = args.predict_label_file3
output_file = args.output_file

df_in = pd.read_csv(label_file, header=0, index_col=False, dtype={'Image': str, 'Presence': str},
                    usecols=['Image', 'Presence'])
df_in['Image'] = df_in['Image'].str.split('/').str[-1]

df_model1 = pd.read_csv(predict_label_file, header=0, index_col=False,
                    dtype={'MAPPED_IMAGE': str, 'ROUND_PREDICT': float},
                    usecols=['MAPPED_IMAGE', 'ROUND_PREDICT'])
df_model1['MAPPED_IMAGE'] = df_model1['MAPPED_IMAGE'].str.split('/').str[-1]
df_model1 = df_model1[df_model1.MAPPED_IMAGE.isin(df_in.Image)]

df_model2 = pd.read_csv(predict_label_file2, header=0, index_col=False,
                    dtype={'MAPPED_IMAGE': str, 'ROUND_PREDICT': float},
                    usecols=['MAPPED_IMAGE', 'ROUND_PREDICT'])
df_model2['MAPPED_IMAGE'] = df_model2['MAPPED_IMAGE'].str.split('/').str[-1]
df_model2 = df_model2[df_model2.MAPPED_IMAGE.isin(df_in.Image)]
df_model2 = df_model2.rename(columns={"ROUND_PREDICT": "ROUND_PREDICT2"})

df_model3 = pd.read_csv(predict_label_file3, header=0, index_col=False,
                    dtype={'MAPPED_IMAGE': str, 'ROUND_PREDICT': float},
                    usecols=['MAPPED_IMAGE', 'ROUND_PREDICT'])
df_model3['MAPPED_IMAGE'] = df_model3['MAPPED_IMAGE'].str.split('/').str[-1]
df_model3 = df_model3[df_model3.MAPPED_IMAGE.isin(df_in.Image)]
df_model3 = df_model3.rename(columns={"ROUND_PREDICT": "ROUND_PREDICT3"})

df_in = df_in.set_index('Image')
df_model1 = df_model1.set_index('MAPPED_IMAGE')
df_model2 = df_model2.set_index('MAPPED_IMAGE')
df_model3 = df_model3.set_index('MAPPED_IMAGE')
df = pd.concat([df_in, df_model1, df_model2, df_model3], axis=1)
df = df.reset_index()
print(df.shape)
print(df)
df['WRONG'] = df.apply(lambda row: 1 if ((row['ROUND_PREDICT'] < 0.5 and row['Presence']=='True') or
                                        (row['ROUND_PREDICT'] >= 0.5 and row['Presence']=='False')) else 0, axis=1)
df['WRONG2'] = df.apply(lambda row: 1 if ((row['ROUND_PREDICT2'] < 0.5 and row['Presence']=='True') or
                                        (row['ROUND_PREDICT2'] >= 0.5 and row['Presence']=='False')) else 0, axis=1)
df['WRONG3'] = df.apply(lambda row: 1 if ((row['ROUND_PREDICT3'] < 0.5 and row['Presence']=='True') or
                                        (row['ROUND_PREDICT3'] >= 0.5 and row['Presence']=='False')) else 0, axis=1)
print(df.shape)
df.to_csv(output_file, index=False)
