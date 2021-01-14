import pandas as pd
import argparse
import matplotlib.pyplot as plt
import math


parser = argparse.ArgumentParser(description='Process arguments.')
parser.add_argument('--input_file', type=str,
                    default='../server/metadata/model-related/secondary_road/d4_subset_with_manual_inspection_300.csv',
                    help='input file with path to create scatter plot from')
parser.add_argument('--subplot', type=bool,
                    default=False,
                    help='whether to show subplot with limited X range or not')
parser.add_argument('--two_lane_only', type=bool,
                    default=True,
                    help='whether to show 2 lane only model prediction plot or 4 lane model prediction plot')
parser.add_argument('--logplot', type=bool, default=False,
                    help='whether to show scatterplot of prediction probability vs log(1-prob+1e-5')
parser.add_argument('--output_file', type=str,
                    default='../server/metadata/model-related/secondary_road/scatterplot_2lane.pdf',
                    help='output pdf file for the generated scatter plot')
args = parser.parse_args()
input_file = args.input_file
subplot = args.subplot
two_lane_only = args.two_lane_only
logplot = args.logplot
output_file = args.output_file

df = pd.read_csv(input_file, header=0, index_col=False,
                 dtype={'MAPPED_IMAGE': str,
                        'MANUAL_YN': str,
                        'ROUND_PREDICT_2': float,
                        'ROUND_PREDICT_4': float})
if two_lane_only:
    df['WRONG'] = df.apply(lambda row: 'Red' if ((row['ROUND_PREDICT_2']>=0.5 and row['MANUAL_YN'] == 'N') or
                                                 (row['ROUND_PREDICT_2']<0.5 and row['MANUAL_YN'] == 'Y')) else 'none',
                           axis=1)
    pred_series = df['ROUND_PREDICT_2']
else:
    df['WRONG'] = df.apply(lambda row: 'Red' if ((row['ROUND_PREDICT_4']>=0.5 and row['MANUAL_YN'] == 'N') or
                                                 (row['ROUND_PREDICT_4']<0.5 and row['MANUAL_YN'] == 'Y')) else 'none',
                           axis=1)
    pred_series = df['ROUND_PREDICT_4']

df.MANUAL_YN = df.MANUAL_YN.apply(lambda row: 'Grey' if row == 'N' else 'Blue')
print('Number of wrong predictions: ', len(df[df['WRONG'] == 'Red']))
# Saving plt with high dpi in order to reveal more cluttered structures
#plt.figure(dpi=1200)
if logplot:
    X = pred_series
    Y = pred_series.apply(lambda row: math.log(1 - row + 1e-5))
else:
    X = df.index
    Y = pred_series

if subplot:
    # the subplot is for limitting the range of the plot aimed at revealing cluttered structures of particular
    # interest even more
    fig, ax = plt.subplots(1,  1)
    ax.scatter(X, Y, s=20, marker='o', facecolors='none', edgecolors=df['MANUAL_YN'],
               label=["guardrail_no: ", "guardrail_yes: "] + df['MANUAL_YN'].unique())
    ax.scatter(X, Y, s=10, marker='o', facecolors=df['WRONG'], edgecolors='none',
               label=['predict_correct:', 'predict_wrong: '] + df['WRONG'].unique() + [' fill', ' fill'])
    ax.set_xlim(100, 250)
else:
    plt.scatter(X, Y, s=20, marker='o', facecolors='none', edgecolors=df['MANUAL_YN'],
                label=["guardrail_no: ", "guardrail_yes: "] + df['MANUAL_YN'].unique())
    plt.scatter(X, Y, s=10, marker='o', facecolors=df['WRONG'], edgecolors='none',
                label=['predict_correct:', 'predict_wrong: '] + df['WRONG'].unique() + [' fill', ' fill'])
plt.title('Scatter plot for 2 lane model')
plt.ylabel('Prediction Probability')
plt.xlabel('Image')
plt.grid(True)
# plt.legend(loc='lower left')
plt.show()
#plt.savefig(output_file)
