import pandas as pd
import argparse
import matplotlib.pyplot as plt
from sklearn.metrics import precision_recall_curve


parser = argparse.ArgumentParser(description='Process arguments.')
parser.add_argument('--input_file', type=str,
                    default='../server/metadata/model-related/secondary_road/d4_subset_with_manual_inspection_300.csv',
                    help='input file with path to create roc curve from')
args = parser.parse_args()
input_file = args.input_file

df = pd.read_csv(input_file, header=0, index_col=False,
                 dtype={'MAPPED_IMAGE': str,
                        'MANUAL_YN': str,
                        'ROUND_PREDICT_2': float,
                        'ROUND_PREDICT_4': float})
df['MANUAL_YN'] = df.MANUAL_YN.apply(lambda row: 0 if row == 'N' else 1)
precision, recall, thresholds = precision_recall_curve(df['MANUAL_YN'].to_numpy(), df['ROUND_PREDICT_2'].to_numpy(), pos_label=1)
print(precision)
print(recall)
print(thresholds)
plt.plot(thresholds, precision[:-1], 'b--', linewidth=2, label='Precision')
plt.plot(thresholds, recall[:-1], 'g-', linewidth=2, label='Recall')
plt.xlabel('Threshold')
plt.legend()
plt.grid(True)
plt.show()
