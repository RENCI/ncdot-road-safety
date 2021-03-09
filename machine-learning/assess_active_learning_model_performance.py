import pandas as pd
import numpy as np
import argparse
from sklearn.metrics import classification_report, confusion_matrix
from sklearn.metrics import average_precision_score


parser = argparse.ArgumentParser(description='Process arguments.')
parser.add_argument('--input_file', type=str,
                    default='../server/metadata/model-related/secondary_road/d4_subset_with_manual_inspection_300.csv',
                    help='input file with path with original 2 lane model predictions and ground truth')
parser.add_argument('--input_al_pred_file', type=str,
                    default='../server/metadata/model-related/secondary_road/predict_d4_subset_300.csv',
                    help='input file with active learning model prediction on the subset data')

args = parser.parse_args()
input_file = args.input_file
input_al_pred_file = args.input_al_pred_file

df_in = pd.read_csv(input_file, header=0, index_col=False,
                    dtype={'MAPPED_IMAGE': str, "ROUND_PREDICT_2": float, 'MANUAL_YN': str},
                    usecols=['MAPPED_IMAGE', 'ROUND_PREDICT_2', 'MANUAL_YN'])
df_al = pd.read_csv(input_al_pred_file, header=0, index_col=False, dtype={'MAPPED_IMAGE': str,
                                                      'ROUND_PREDICT': float})
df_al['MAPPED_IMAGE'] = df_al['MAPPED_IMAGE'].str.replace('/projects/ncdot/NC_2018_Secondary/subset_data/data/data', '')
df_al['MAPPED_IMAGE'] = df_al['MAPPED_IMAGE'].str.replace('.jpg', '')
df = pd.concat([df_in, df_al], axis=1)
print(df.shape)
df_in_correct = df[((df.ROUND_PREDICT_2 >= 0.5) & (df.MANUAL_YN == 'Y')) | ((df.ROUND_PREDICT_2 < 0.5) & (df.MANUAL_YN == 'N'))]
df_in_yes_correct = df[((df.ROUND_PREDICT_2 >= 0.5) & (df.MANUAL_YN == 'Y'))]
df_in_no_correct = df[((df.ROUND_PREDICT_2 < 0.5) & (df.MANUAL_YN == 'N'))]
df_al_correct = df[((df.ROUND_PREDICT >= 0.5) & (df.MANUAL_YN == 'Y')) | ((df.ROUND_PREDICT < 0.5) & (df.MANUAL_YN == 'N'))]
df_al_yes_correct = df[((df.ROUND_PREDICT >= 0.5) & (df.MANUAL_YN == 'Y'))]
df_al_no_correct = df[((df.ROUND_PREDICT < 0.5) & (df.MANUAL_YN == 'N'))]
df_in_wrong = df[((df.ROUND_PREDICT_2 >= 0.5) & (df.MANUAL_YN == 'N')) | ((df.ROUND_PREDICT_2 < 0.5) & (df.MANUAL_YN == 'Y'))]
df_in_yes_wrong = df[((df.ROUND_PREDICT_2 >= 0.5) & (df.MANUAL_YN == 'N'))]
df_in_no_wrong = df[((df.ROUND_PREDICT_2 < 0.5) & (df.MANUAL_YN == 'Y'))]
df_al_wrong = df[((df.ROUND_PREDICT >= 0.5) & (df.MANUAL_YN == 'N')) | ((df.ROUND_PREDICT < 0.5) & (df.MANUAL_YN == 'Y'))]
df_al_yes_wrong = df[((df.ROUND_PREDICT >= 0.5) & (df.MANUAL_YN == 'N'))]
df_al_no_wrong = df[((df.ROUND_PREDICT < 0.5) & (df.MANUAL_YN == 'Y'))]
print("2 lane original model yes prediction:", df_in_correct.shape, df_in_yes_correct.shape, df_in_yes_wrong.shape)
print("2 lane original model no prediction:", df_in_correct.shape, df_in_no_correct.shape, df_in_no_wrong.shape)
print("AL model yes prediction:", df_al_correct.shape, df_al_yes_correct.shape, df_al_yes_wrong.shape)
print("AL model no prediction:", df_al_correct.shape, df_al_no_correct.shape, df_al_no_wrong.shape)

df.MANUAL_YN = np.where(df.MANUAL_YN.eq('Y'), 1, 0)
df.ROUND_PREDICT_2 = np.where(df.ROUND_PREDICT_2>=0.5, 1, 0)
df.ROUND_PREDICT = np.where(df.ROUND_PREDICT>=0.5, 1, 0)
print('Confusion Matrix for original model')
print(confusion_matrix(df.MANUAL_YN, df.ROUND_PREDICT_2))
print('Classification Report for original model')
print(classification_report(df.MANUAL_YN, df.ROUND_PREDICT_2))
print('average precision score for original model', average_precision_score(df.MANUAL_YN, df.ROUND_PREDICT_2))
print('Confusion Matrix for AL model')
print(confusion_matrix(df.MANUAL_YN, df.ROUND_PREDICT))
print('Classification Report for AL model')
print(classification_report(df.MANUAL_YN, df.ROUND_PREDICT))
print('average precision score for AL model', average_precision_score(df.MANUAL_YN, df.ROUND_PREDICT))
