import pandas as pd
import argparse
import matplotlib.pyplot as plt
from sklearn.metrics import roc_curve, roc_auc_score


parser = argparse.ArgumentParser(description='Process arguments.')
parser.add_argument('--input_file', type=str,
                    default='../server/metadata/model-related/secondary_road/d4_subset_with_manual_inspection_300.csv',
                    help='input file with path to create roc curve from')
parser.add_argument('--model_predict_file', type=str,
                    default='../server/metadata/model-related/secondary_road/predict_d4_subset_300.csv',
                    help='the active learning model prediction file')

args = parser.parse_args()
input_file = args.input_file
model_predict_file = args.model_predict_file

df_in = pd.read_csv(input_file, header=0, index_col=False, dtype={'MAPPED_IMAGE': str,
                                                                  'MANUAL_YN': str,
                                                                  'ROUND_PREDICT_2': float},
                    usecols=['MAPPED_IMAGE', 'MANUAL_YN', 'ROUND_PREDICT_2'])
df_in['MANUAL_YN'] = df_in.MANUAL_YN.apply(lambda row: 0 if row == 'N' else 1)
df_al = pd.read_csv(model_predict_file, header=0, index_col=False, dtype={'MAPPED_IMAGE': str, 'ROUND_PREDICT': float})
df_al['MAPPED_IMAGE'] = df_al['MAPPED_IMAGE'].str.replace('/projects/ncdot/NC_2018_Secondary/subset_data/data/data', '')
df_al['MAPPED_IMAGE'] = df_al['MAPPED_IMAGE'].str.replace('.jpg', '')
df = pd.concat([df_in, df_al], axis=1)

fpr, tpr, thresholds = roc_curve(df['MANUAL_YN'], df['ROUND_PREDICT_2'], pos_label=1)
fpr_al, tpr_al, thresholds_al = roc_curve(df['MANUAL_YN'], df['ROUND_PREDICT'], pos_label=1)
plt.plot(fpr, tpr, linewidth=2)
plt.plot(fpr_al, tpr_al, linewidth=2)
plt.title('ROC Curve')
plt.ylabel('True Positive Rate (Recall)')
plt.xlabel('False Positive Rate')
plt.legend(['Initial model', 'AL model'], loc='lower right')
plt.plot([0, 1], [0, 1], 'k--')
plt.show()
score_2 = roc_auc_score(df['MANUAL_YN'], df['ROUND_PREDICT_2'])
score_al = roc_auc_score(df['MANUAL_YN'], df['ROUND_PREDICT'])
print(score_2, score_al)
