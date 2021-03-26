import pandas as pd
import argparse
import matplotlib.pyplot as plt
from sklearn.metrics import roc_curve, roc_auc_score


parser = argparse.ArgumentParser(description='Process arguments.')
parser.add_argument('--input_file', type=str,
                    default='../server/metadata/holdout_test/user_annoted_balanced_image_info.txt',
                    help='input file with path to create roc curve from')
parser.add_argument('--curve_title', type=str,
                    default='ROC Curve',
                    help='ROC curve title')
parser.add_argument('--model_predict_file', type=str,
                    default='../server/metadata/model_predict_test_base.csv',
                    help='the active learning model prediction file')
parser.add_argument('--model_predict_file2', type=str,
                    default='../server/metadata/model_predict_test_round1.csv',
                    help='the active learning model prediction file')
parser.add_argument('--model_predict_file3', type=str,
                    default='../server/metadata/model_predict_test_round2.csv',
                    help='the active learning model prediction file')


args = parser.parse_args()
input_file = args.input_file
model_predict_file = args.model_predict_file
model_predict_file2 = args.model_predict_file2
model_predict_file3 = args.model_predict_file3
curve_title = args.curve_title

df_in = pd.read_csv(input_file, header=0, index_col=False, dtype={'Image': str, 'Presence': str},
                    usecols=['Image', 'Presence'])
df_in['Image'] = df_in['Image'].str.split('/').str[-1]
df_al = pd.read_csv(model_predict_file, header=0, index_col=False,
                    dtype={'MAPPED_IMAGE': str, 'ROUND_PREDICT': float},
                    usecols=['MAPPED_IMAGE', 'ROUND_PREDICT'])
df_al2 = pd.read_csv(model_predict_file2, header=0, index_col=False,
                     dtype={'MAPPED_IMAGE': str, 'ROUND_PREDICT': float},
                     usecols=['MAPPED_IMAGE', 'ROUND_PREDICT'])
df_al3 = pd.read_csv(model_predict_file3, header=0, index_col=False,
                     dtype={'MAPPED_IMAGE': str, 'ROUND_PREDICT': float},
                     usecols=['MAPPED_IMAGE', 'ROUND_PREDICT'])
df_al['MAPPED_IMAGE'] = df_al['MAPPED_IMAGE'].str.split('/').str[-1]
df_al2['MAPPED_IMAGE'] = df_al2['MAPPED_IMAGE'].str.split('/').str[-1]
df_al3['MAPPED_IMAGE'] = df_al3['MAPPED_IMAGE'].str.split('/').str[-1]
df_al2 = df_al2.rename(columns={'ROUND_PREDICT': 'ROUND_PREDICT2'})
df_al3 = df_al3.rename(columns={'ROUND_PREDICT': 'ROUND_PREDICT3'})
df_al = df_al[df_al.MAPPED_IMAGE.isin(df_in.Image)]
df_al2 = df_al2[df_al2.MAPPED_IMAGE.isin(df_in.Image)]
df_al3 = df_al3[df_al3.MAPPED_IMAGE.isin(df_in.Image)]
df_in = df_in.set_index('Image')
df_al = df_al.set_index('MAPPED_IMAGE')
df_al2 = df_al2.set_index('MAPPED_IMAGE')
df_al3 = df_al3.set_index('MAPPED_IMAGE')
df = pd.concat([df_in, df_al, df_al2, df_al3], axis=1)
df = df.reset_index()
df['Presence'] = df.Presence.apply(lambda row: 0 if row == 'False' else 1)
print(df.shape)

fpr, tpr, thresholds = roc_curve(df['Presence'], df['ROUND_PREDICT'], pos_label=1)
fpr2, tpr2, thresholds2 = roc_curve(df['Presence'], df['ROUND_PREDICT2'], pos_label=1)
fpr3, tpr3, thresholds3 = roc_curve(df['Presence'], df['ROUND_PREDICT3'], pos_label=1)
plt.plot(fpr, tpr, linewidth=2)
plt.plot(fpr2, tpr2, linewidth=2)
plt.plot(fpr3, tpr3, linewidth=2)
plt.title(curve_title)
plt.ylabel('True Positive Rate (Recall)')
plt.xlabel('False Positive Rate')
score = round(roc_auc_score(df['Presence'], df['ROUND_PREDICT']), 3)
score2 = round(roc_auc_score(df['Presence'], df['ROUND_PREDICT2']), 3)
score3 = round(roc_auc_score(df['Presence'], df['ROUND_PREDICT3']), 3)
plt.legend([f'Baseline model (AUC: {score})', f'Round1 model (AUC: {score2})', f'Round2 model (AUC: {score3})'], loc='lower right')
plt.plot([0, 1], [0, 1], 'k--')
plt.show()
print(score, score2, score3)
