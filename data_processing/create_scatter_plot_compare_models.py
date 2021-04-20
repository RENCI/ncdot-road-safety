import pandas as pd
import argparse
import matplotlib.pyplot as plt
import seaborn as sns


parser = argparse.ArgumentParser(description='Process arguments.')
parser.add_argument('--input_file', type=str,
                    # default='../server/metadata/holdout_test/user_annoted_balanced_image_info.txt',
                    default='../server/metadata/holdout_test/user_annoted_image_info_for_holdout.csv',
                    help='input file with path to create scatter plot from')
parser.add_argument('--model_predict_file', type=str,
                    default='../server/metadata/model_predict_test_base.csv',
                    help='the active learning model prediction file')
parser.add_argument('--plot_title', type=str,
                    default='Baseline & round1 model prediction comparisons on holdout test',
                    help='plot title')
parser.add_argument('--x_axis_label', type=str,
                    default='Baseline model predict probability',
                    help='x axis label')
parser.add_argument('--model_predict_file2', type=str,
                    default='../server/metadata/model_predict_test_round1.csv',
                    help='the active learning model prediction file')
parser.add_argument('--y_axis_label', type=str,
                    default='Round1 model predict probability',
                    help='y axis label')
parser.add_argument('--probability_plot', type=bool, default=True,
                    help='If true, draw probability vs probability plot between two models for comparison; otherwise, '
                         'draw probability vs images plot for model comparison')
parser.add_argument('--probability_plot_all', type=bool, default=False,
                    help='If true, draw probability vs probability plot between two models for comparison with '
                         'predictions for all images; otherwise, only draw different predictions between two models.')

args = parser.parse_args()
input_file = args.input_file
model_predict_file = args.model_predict_file
model_predict_file2 = args.model_predict_file2
probability_plot = args.probability_plot
probability_plot_all = args.probability_plot_all
plot_title = args.plot_title

x_axis_label = args.x_axis_label
y_axis_label = args.y_axis_label

df_in = pd.read_csv(input_file, header=0, index_col=False, dtype={'Image': str, 'Presence': str},
                    usecols=['Image', 'Presence'])
df_in['Image'] = df_in['Image'].str.split('/').str[-1]

df_al = pd.read_csv(model_predict_file, header=0, index_col=False,
                    dtype={'MAPPED_IMAGE': str, 'ROUND_PREDICT': float},
                    usecols=['MAPPED_IMAGE', 'ROUND_PREDICT'])
df_al['MAPPED_IMAGE'] = df_al['MAPPED_IMAGE'].str.split('/').str[-1]
df_al = df_al[df_al.MAPPED_IMAGE.isin(df_in.Image)]
df_al = df_al.rename(columns={'ROUND_PREDICT': x_axis_label})

df_al2 = pd.read_csv(model_predict_file2, header=0, index_col=False,
                    dtype={'MAPPED_IMAGE': str, 'ROUND_PREDICT': float},
                    usecols=['MAPPED_IMAGE', 'ROUND_PREDICT'])
df_al2['MAPPED_IMAGE'] = df_al2['MAPPED_IMAGE'].str.split('/').str[-1]
df_al2 = df_al2[df_al2.MAPPED_IMAGE.isin(df_in.Image)]
df_al2 = df_al2.rename(columns={'ROUND_PREDICT': y_axis_label})

df_in = df_in.set_index('Image')
df_al = df_al.set_index('MAPPED_IMAGE')
df_al2 = df_al2.set_index('MAPPED_IMAGE')
df = pd.concat([df_in, df_al, df_al2], axis=1)
df = df.reset_index()
print(df.shape)

X = df.index

Y1 = df[x_axis_label]
Y2 = df[y_axis_label]

if probability_plot:
    if probability_plot_all:
        ax = sns.stripplot(x=x_axis_label, y=y_axis_label, data=df,
                           jitter=0.3, linewidth=1, hue='Presence', palette={"True": "blue",
                                                                             "False": "red"})
    else:
        df['Different_Predictions'] = df.apply(lambda row: 'FPs to TNs'
        if (row[x_axis_label] >= 0.5 and row[y_axis_label] < 0.5 and row['Presence'] == 'False')
        else 'FNs to TPs' if (row[x_axis_label] < 0.5 and row[y_axis_label] >= 0.5 and row['Presence'] == 'True')
        else 'TNs to FPs' if (row[x_axis_label] < 0.5 and row[y_axis_label] >= 0.5 and row['Presence'] == 'False')
        else 'TPs to FNs' if (row[x_axis_label] >= 0.5 and row[y_axis_label] < 0.5 and row['Presence'] == 'True')
        else 'none', axis=1)
        print('Number of wrong predictions of previous model: ',
              len(df[(df['Different_Predictions'] == 'FPs to TNs') | (df['Different_Predictions'] == 'FNs to TPs')]))
        print('Number of wrong predictions of updated model: ',
              len(df[(df['Different_Predictions'] =='TNs to FPs') | (df['Different_Predictions'] == 'TPs to FNs')]))
        print(df[df['Different_Predictions'] != 'none'][y_axis_label])
        ax = sns.stripplot(x=x_axis_label, y=y_axis_label, data=df[df['Different_Predictions'] != 'none'],
                           jitter=0.3, linewidth=1, hue='Different_Predictions',
                           palette={"FPs to TNs": "blue",
                                    "FNs to TPs": 'blue',
                                    "TNs to FPs": "red",
                                    "TPs to FNs": "red"})
        ax.set_title(plot_title)
else:
    # df['WRONG'] indicates those rows where the baseline model1 predicts wrongly but updated model2 predicts correctly
    df['WRONG'] = df.apply(lambda row: 'Blue' if ((row[x_axis_label] >= 0.5 and row[y_axis_label] < 0.5
                                                  and row['Presence'] == 'False') or
                                                 (row[x_axis_label] < 0.5 and row[y_axis_label] >= 0.5 and
                                                  row['Presence'] == 'True')) else 'none',
                           axis=1)
    # df['WRONG2'] indicates those rows where the baseline model1 predicts correctly but updated model2 predicts wrongly
    df['WRONG2'] = df.apply(lambda row: 'Red' if ((row[y_axis_label] >= 0.5 and row[x_axis_label] < 0.5 and
                                                    row['Presence'] == 'False') or
                                                   (row[y_axis_label] < 0.5 and row[x_axis_label] >= 0.5 and
                                                    row['Presence'] == 'True')) else 'none',
                            axis=1)
    print('Number of wrong predictions of base model: ', len(df[df['WRONG'] == 'Blue']))
    print('Number of wrong predictions of updated model: ', len(df[df['WRONG2'] == 'Red']))
    plt.scatter(X, Y1, s=20, marker='o', facecolors=df['WRONG'], edgecolors=df['WRONG'],
                label=["predict_correct: ", "predict_wrong: "] + df['WRONG'].unique())
    plt.scatter(X, Y2, s=20, marker='o', facecolors=df['WRONG2'], edgecolors=df['WRONG2'],
                label=["predict_wrong: ", "predict_correct: "] + df['WRONG2'].unique())
    plt.title(plot_title)
    plt.ylabel('Prediction Probability')
    plt.xlabel('Image')

# plt.legend(loc='lower left')
plt.show()
