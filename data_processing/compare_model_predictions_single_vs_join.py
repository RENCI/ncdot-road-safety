import argparse
import pandas as pd
from create_balanced_random_subset_html_for_inspection import create_html_file_for_inspection
from sklearn.metrics import classification_report, confusion_matrix


parser = argparse.ArgumentParser(description='Process arguments.')
parser.add_argument('--predict_join_file', type=str,
                    default='../server/metadata/round5/model_predict_test_balanced.csv',
                    help='model prediction on the joined images')
parser.add_argument('--predict_single_file', type=str,
                    default='../server/metadata/round5/model_predict_test_single.csv',
                    help='Same model prediction on the single images')
parser.add_argument('--label_file', type=str,
                    default='../server/metadata/holdout_test/user_annoted_balanced_image_info.txt',
                    help='Same model prediction on the single images')
parser.add_argument('--output_concat_file', type=str,
                    default='../server/metadata/round5/predict_annot.csv',
                    help='Same model prediction on the single images')
parser.add_argument('--output_html_file', type=str,
                    default='../server/templates/single_vs_join_5.html',
                    help='Same model prediction on the single images')

args = parser.parse_args()
predict_join_file = args.predict_join_file
predict_single_file = args.predict_single_file
label_file = args.label_file
output_html_file = args.output_html_file
output_concat_file = args.output_concat_file

join_df = pd.read_csv(predict_join_file, header=0, index_col=None, usecols=['MAPPED_IMAGE', 'ROUND_PREDICT'],
                      dtype={'MAPPED_IMAGE': 'str', 'ROUND_PREDICT': 'float'})
single_df = pd.read_csv(predict_single_file, header=0, index_col='MAPPED_IMAGE', dtype={'MAPPED_IMAGE': 'str',
                                                                                        'ROUND_PREDICT': 'float'})
label_df = pd.read_csv(label_file, header=0, index_col='Image')
label_df.index = label_df.index.str.split('/').str[-1]
label_df.index = label_df.index.str.replace('.jpg', '')

join_df.MAPPED_IMAGE = join_df.MAPPED_IMAGE.str.split('/').str[-1]
join_df.MAPPED_IMAGE = join_df.MAPPED_IMAGE.str.replace('.jpg', '')
single_df.index = single_df.index.str.split('/').str[-1]
single_df.index = single_df.index.str.replace('.jpg', '')
single_df['GROUP'] = single_df.index.str[:-1]
single_df['ROUND_PREDICT_GROUP'] = single_df.apply(lambda row: 1 if row.ROUND_PREDICT>=0.5 else 0, axis=1)
single_df.drop(columns=['ROUND_PREDICT'], inplace=True)
single_df = single_df.groupby(by=['GROUP']).sum()
join_df = join_df[join_df['MAPPED_IMAGE'].isin(single_df.index)]
join_df.set_index('MAPPED_IMAGE', inplace=True)
concat_df = pd.concat([single_df, join_df, label_df], axis=1)
concat_df.rename(columns={'index': 'MAPPED_IMAGE'}, inplace=True)
concat_df.to_csv(output_concat_file)
print('Confusion Matrix for joined images')
concat_df['ROUND_PREDICT'] = concat_df.ROUND_PREDICT.apply(lambda row: 0 if row < 0.5 else 1)
concat_df['ROUND_PREDICT_SINGLE'] = concat_df.apply(lambda row: 1 if (row.ROUND_PREDICT_GROUP > 0 or
                                                                      row.ROUND_PREDICT > 0) else 0, axis=1)
print(confusion_matrix(concat_df['Presence'], concat_df['ROUND_PREDICT']))
print('Classification Report for joined images')
print(classification_report(concat_df['Presence'], concat_df['ROUND_PREDICT']))
print('Confusion Matrix for single images')
print(confusion_matrix(concat_df['Presence'], concat_df['ROUND_PREDICT_SINGLE']))
print('Classification Report for single images')
print(classification_report(concat_df['Presence'], concat_df['ROUND_PREDICT_SINGLE']))
same_df = concat_df[((concat_df.ROUND_PREDICT >= 0.5) & (concat_df.ROUND_PREDICT_GROUP > 0)) |
                     ((concat_df.ROUND_PREDICT < 0.5) & (concat_df.ROUND_PREDICT_GROUP == 0))]
same = len(same_df)
diff_df = concat_df[((concat_df.ROUND_PREDICT >= 0.5) & (concat_df.ROUND_PREDICT_GROUP == 0)) |
                     ((concat_df.ROUND_PREDICT < 0.5) & (concat_df.ROUND_PREDICT_GROUP > 0))]
diff = len(diff_df)
print(same, diff)
diff_df.reset_index(inplace=True)
diff_df.rename(columns={'index': 'MAPPED_IMAGE', 'ROUND_PREDICT_GROUP': 'ROUND_PREDICT_2'}, inplace=True)
print(diff_df)
create_html_file_for_inspection(diff_df, output_html_file, predict_only=True)
