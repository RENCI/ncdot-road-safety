import pandas as pd
import numpy as np
import argparse
from sklearn.metrics import classification_report, confusion_matrix
from sklearn.metrics import average_precision_score
from sklearn.metrics import precision_recall_curve
from sklearn.metrics import roc_curve
import matplotlib.pyplot as plt


parser = argparse.ArgumentParser(description='Process arguments.')
parser.add_argument('--label_file', type=str,
                    default='../server/metadata/training_Image_guardrail_yn.csv',
                    help='labelled guardrail data obtained from guardrail survey data')
parser.add_argument('--predict_label_file', type=str,
                    default='../server/metadata/guardrail_classification.csv',
                    help='predicted guardrail lable data')

args = parser.parse_args()
label_file = args.label_file
predict_label_file = args.predict_label_file

df_labels = pd.read_csv(label_file, header=0, index_col='MAPPED_IMAGE', usecols=['MAPPED_IMAGE', 'GUARDRAIL_YN'])
df_labels.GUARDRAIL_YN = np.where(df_labels.GUARDRAIL_YN.eq('Y'), 1, 0)
df_labels.sort_index(inplace=True)
df_predict_labels = pd.read_csv(predict_label_file, header=0, index_col='MAPPED_IMAGE')
df_predict_labels.dropna(inplace=True)
df_predict_labels.sort_index(inplace=True)
df_predict_labels['PREDICTION_YN'] = np.where(df_predict_labels['Probability']>=0.5, 1, 0)
df_result = pd.concat([df_labels, df_predict_labels], axis=1, join='inner')
print('Confusion Matrix')
print(confusion_matrix(df_result['GUARDRAIL_YN'], df_result['PREDICTION_YN']))
print('Classification Report')
print(classification_report(df_result['GUARDRAIL_YN'], df_result['PREDICTION_YN']))
print('average precision score', average_precision_score(df_result['GUARDRAIL_YN'], df_result['PREDICTION_YN']))
precision, recall, threshold = precision_recall_curve(df_result['GUARDRAIL_YN'], df_result['PREDICTION_YN'])
plt.plot(threshold, precision[:-1], "b--", label='Precision')
plt.plot(threshold, recall[:-1], "g--", label='Recall')
plt.grid(True)
plt.show()

fpr, tpr, threshold = roc_curve(df_result['GUARDRAIL_YN'], df_result['PREDICTION_YN'])
plt.plot(fpr, tpr, linewidth=2)
plt.plot([0, 1], [0, 1], 'k--')
plt.grid(True)
plt.show()
