import pandas as pd
import argparse
import matplotlib.pyplot as plt


parser = argparse.ArgumentParser(description='Process arguments.')
parser.add_argument('--input_file', type=str,
                    default='../server/metadata/d4_subset_with_manual_inspection_300.csv',
                    help='input file with path to create scatter plot from')
args = parser.parse_args()
input_file = args.input_file

df = pd.read_csv(input_file, header=0, index_col=False,
                 dtype={'MAPPED_IMAGE': str,
                        'MANUAL_YN': str,
                        'ROUND_PREDICT_2': float,
                        'ROUND_PREDICT_4': float})
df['X'] = df.index
df['WRONG'] = df.apply(lambda row:
                    'Red' if ((row['ROUND_PREDICT_4']>=0.5 and row['MANUAL_YN']=='N')
                    or (row['ROUND_PREDICT_4']<0.5 and row['MANUAL_YN']=='Y')) else 'none', axis=1)
df.MANUAL_YN = df.MANUAL_YN.apply(lambda row: 'Grey' if row == 'N' else 'Blue')
print('Number of wrong predictions: ', len(df[df['WRONG'] == 'Red']))
plt.scatter(df['X'], df['ROUND_PREDICT_4'], s=20, marker='o', facecolors='none',
            edgecolors=df['MANUAL_YN'], label=["guardrail_no: ", "guardrail_yes: "] + df['MANUAL_YN'].unique())
plt.scatter(df['X'], df['ROUND_PREDICT_4'], s=10, marker='o', facecolors=df['WRONG'],
            edgecolors='none', label=['predict_correct:', 'predict_wrong: '] + df['WRONG'].unique() + [' fill', ' fill'])
plt.title('Scatter plot for 4 lane model')
plt.ylabel('Prediction Probability')
plt.xlabel('Image')
#plt.legend(loc='lower left')
plt.grid(True)
plt.show()
