import pandas as pd
import argparse
import matplotlib.pyplot as plt
import math


parser = argparse.ArgumentParser(description='Process arguments.')
parser.add_argument('--input_file', type=str,
                    default='../server/metadata/holdout_test/user_annoted_balanced_image_info.txt',
                    help='input file with path to create scatter plot from')
parser.add_argument('--subplot', type=bool,
                    default=False,
                    help='whether to show subplot with limited X range or not')
parser.add_argument('--model_predict_file', type=str,
                    default='../server/metadata/model_predict_test_round3.csv',
                    help='the active learning model prediction file')
parser.add_argument('--plt_title', type=str,
                    default='Scatter plot for round3 model prediction on balanced holdout test',
                    help='the plot title')
parser.add_argument('--logplot', type=bool, default=False,
                    help='whether to show scatterplot of prediction probability vs log(1-prob+1e-5')
parser.add_argument('--output_file', type=str,
                    default='../server/metadata/scatterplot_test.pdf',
                    help='output pdf file for the generated scatter plot')

args = parser.parse_args()
input_file = args.input_file
subplot = args.subplot
model_predict_file = args.model_predict_file
logplot = args.logplot
output_file = args.output_file
plt_title = args.plt_title

df_in = pd.read_csv(input_file, header=0, index_col=False, dtype={'Image': str, 'Presence': str},
                    usecols=['Image', 'Presence'])
df_in['Image'] = df_in['Image'].str.split('/').str[-1]
df_al = pd.read_csv(model_predict_file, header=0, index_col=False,
                    dtype={'MAPPED_IMAGE': str, 'ROUND_PREDICT': float},
                    usecols=['MAPPED_IMAGE', 'ROUND_PREDICT'])
df_al['MAPPED_IMAGE'] = df_al['MAPPED_IMAGE'].str.split('/').str[-1]
df_al = df_al[df_al.MAPPED_IMAGE.isin(df_in.Image)]
df_in = df_in.set_index('Image')
df_al = df_al.set_index('MAPPED_IMAGE')
df = pd.concat([df_in, df_al], axis=1)
df = df.reset_index()
print(df.shape)

df['WRONG'] = df.apply(lambda row: 'Red' if ((row['ROUND_PREDICT']>=0.5 and row['Presence'] == 'False') or
                                             (row['ROUND_PREDICT']<0.5 and row['Presence'] == 'True')) else 'none',
                       axis=1)

pred_series = df['ROUND_PREDICT']

df.Presence = df.Presence.apply(lambda row: 'Grey' if row == 'False' else 'Blue')
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
    ax.scatter(X, Y, s=20, marker='o', facecolors='none', edgecolors=df['Presence'],
               label=["guardrail_no: ", "guardrail_yes: "] + df['Presence'].unique())
    ax.scatter(X, Y, s=10, marker='o', facecolors=df['WRONG'], edgecolors='none',
               label=['predict_correct:', 'predict_wrong: '] + df['WRONG'].unique() + [' fill', ' fill'])
    ax.set_xlim(100, 250)
else:
    plt.scatter(X, Y, s=20, marker='o', facecolors='none', edgecolors=df['Presence'],
                label=["guardrail_no: ", "guardrail_yes: "] + df['Presence'].unique())
    plt.scatter(X, Y, s=10, marker='o', facecolors=df['WRONG'], edgecolors='none',
                label=['predict_correct:', 'predict_wrong: '] + df['WRONG'].unique() + [' fill', ' fill'])
plt.title(plt_title)
plt.ylabel('Prediction Probability')
plt.xlabel('Image')

# plt.legend(loc='lower left')
plt.show()
#plt.savefig(output_file)
