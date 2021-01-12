import pandas as pd
import argparse
import matplotlib.pyplot as plt
from sklearn.metrics import roc_curve, roc_auc_score, precision_recall_curve


parser = argparse.ArgumentParser(description='Process arguments.')
parser.add_argument('--input_file', type=str,
                    default='../server/metadata/d4_subset_with_manual_inspection_300.csv',
                    help='input file with path to create roc curve from')
args = parser.parse_args()
input_file = args.input_file

df = pd.read_csv(input_file, header=0, index_col=False,
                 dtype={'MAPPED_IMAGE': str,
                        'MANUAL_YN': str,
                        'ROUND_PREDICT_2': float,
                        'ROUND_PREDICT_4': float})
df['MANUAL_YN'] = df.MANUAL_YN.apply(lambda row: 0 if row == 'N' else 1)
fpr, tpr, thresholds = roc_curve(df['MANUAL_YN'], df['ROUND_PREDICT_2'], pos_label=1)
fpr4, tpr4, thresholds4 = roc_curve(df['MANUAL_YN'], df['ROUND_PREDICT_4'], pos_label=1)
plt.plot(fpr, tpr, linewidth=2)
plt.plot(fpr4, tpr4, linewidth=2)
plt.title('ROC Curve')
plt.ylabel('True Positive Rate (Recall)')
plt.xlabel('False Positive Rate')
plt.legend(['2 lane model', '4 lane model'], loc='lower right')
plt.plot([0, 1], [0, 1], 'k--')
plt.show()
score_2 = roc_auc_score(df['MANUAL_YN'], df['ROUND_PREDICT_2'])
score_4 = roc_auc_score(df['MANUAL_YN'], df['ROUND_PREDICT_4'])
print(score_2, score_4)
