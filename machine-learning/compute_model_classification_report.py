import pandas as pd
import numpy as np
import argparse
from sklearn.metrics import classification_report, confusion_matrix
from sklearn.metrics import average_precision_score
# from utils import draw_plots


parser = argparse.ArgumentParser(description='Process arguments.')
parser.add_argument('--label_file', type=str,
                    default='../server/metadata/user_annotated_balanced_image_info_d4.txt',
                    help='labelled guardrail data obtained from guardrail survey data')
parser.add_argument('--predict_label_file', type=str,
                    default='../server/metadata/model-related/secondary_road/model_2lane_predict_d4.csv',
                    help='predicted guardrail lable data')

args = parser.parse_args()
label_file = args.label_file
predict_label_file = args.predict_label_file

df_in = pd.read_csv(label_file, header=0, index_col=False, dtype={'Image': str, 'Presence': str},
                    usecols=['Image', 'Presence'])
df_in['Image'] = df_in['Image'].str.split('/').str[-1]
df_al = pd.read_csv(predict_label_file, header=0, index_col=False,
                    dtype={'MAPPED_IMAGE': str, 'ROUND_PREDICT': float},
                    usecols=['MAPPED_IMAGE', 'ROUND_PREDICT'])
df_al['MAPPED_IMAGE'] = df_al['MAPPED_IMAGE'].str.split('/').str[-1]
df_al = df_al[df_al.MAPPED_IMAGE.isin(df_in.Image)]
df_in = df_in.set_index('Image')
df_al = df_al.set_index('MAPPED_IMAGE')
df = pd.concat([df_in, df_al], axis=1)
df = df.reset_index()
df['Presence'] = df.Presence.apply(lambda row: 0 if row == 'False' else 1)
df['ROUND_PREDICT'] = df.ROUND_PREDICT.apply(lambda row: 0 if row < 0.5 else 1)
print(df.shape)
df.to_csv('model_2lane_predict_d4_with_manual_labels.csv', index=False)
print('Confusion Matrix')
print(confusion_matrix(df['Presence'], df['ROUND_PREDICT']))
print('Classification Report')
print(classification_report(df['Presence'], df['ROUND_PREDICT']))
print('average precision score', average_precision_score(df['Presence'], df['ROUND_PREDICT']))
#draw_plots(df_result['GUARDRAIL_YN'], df_result['PREDICTION_YN'])
