import pandas as pd
import argparse
import matplotlib.pyplot as plt


parser = argparse.ArgumentParser(description='Process arguments.')
parser.add_argument('--input_file', type=str,
                    default='../server/metadata/user_annotated_balanced_image_info_d4.csv',
                    help='input file with path to create scatter plot from')
parser.add_argument('--model_predict_file', type=str,
                    default='../server/metadata/model_predict_test_base.csv',
                    help='the active learning model prediction file')
parser.add_argument('--model_predict_file2', type=str,
                    default='../server/metadata/model_predict_test.csv',
                    help='the active learning model prediction file')
parser.add_argument('--probability_plot', type=bool, default=True,
                    help='If true, draw probability vs probability plot between two models for comparison; otherwise, '
                         'draw probability vs images plot for model comparison')

args = parser.parse_args()
input_file = args.input_file
model_predict_file = args.model_predict_file
model_predict_file2 = args.model_predict_file2
probability_plot = args.probability_plot

df_in = pd.read_csv(input_file, header=0, index_col=False, dtype={'Image': str, 'Presence': str},
                    usecols=['Image', 'Presence'])
df_in['Image'] = df_in['Image'].str.split('/').str[-1]

df_al = pd.read_csv(model_predict_file, header=0, index_col=False,
                    dtype={'MAPPED_IMAGE': str, 'ROUND_PREDICT': float},
                    usecols=['MAPPED_IMAGE', 'ROUND_PREDICT'])
df_al['MAPPED_IMAGE'] = df_al['MAPPED_IMAGE'].str.split('/').str[-1]
df_al = df_al[df_al.MAPPED_IMAGE.isin(df_in.Image)]

df_al2 = pd.read_csv(model_predict_file2, header=0, index_col=False,
                    dtype={'MAPPED_IMAGE': str, 'ROUND_PREDICT': float},
                    usecols=['MAPPED_IMAGE', 'ROUND_PREDICT'])
df_al2['MAPPED_IMAGE'] = df_al2['MAPPED_IMAGE'].str.split('/').str[-1]
df_al2 = df_al2[df_al2.MAPPED_IMAGE.isin(df_in.Image)]
df_al2 = df_al2.rename(columns={'ROUND_PREDICT': 'ROUND_PREDICT2'})

df_in = df_in.set_index('Image')
df_al = df_al.set_index('MAPPED_IMAGE')
df_al2 = df_al2.set_index('MAPPED_IMAGE')
df = pd.concat([df_in, df_al, df_al2], axis=1)
df = df.reset_index()
print(df.shape)

X = df.index
Y1 = df['ROUND_PREDICT']
Y2 = df['ROUND_PREDICT2']

if probability_plot:
    # df['WRONG'] indicates those rows where the baseline model1 predicts wrongly but updated model2 predicts correctly
    df['WRONG'] = df.apply(lambda row: 'Blue' if ((row['ROUND_PREDICT'] >= 0.5 and row['ROUND_PREDICT2'] < 0.5
    and row['Presence'] == 'False') or (row['ROUND_PREDICT'] < 0.5 and row['ROUND_PREDICT2'] >= 0.5 and
                                        row['Presence'] == 'True'))
    else 'Red' if ((row['ROUND_PREDICT2'] >= 0.5 and row['ROUND_PREDICT'] < 0.5 and row['Presence'] == 'False') or
    (row['ROUND_PREDICT2'] < 0.5 and row['ROUND_PREDICT'] >= 0.5 and row['Presence'] == 'True')) else 'none',
                           axis=1)
    print('Number of wrong predictions of base model: ', len(df[df['WRONG'] == 'Blue']))
    print('Number of wrong predictions of updated model: ', len(df[df['WRONG'] == 'Red']))
    plt.scatter(Y1, Y2, s=20, marker='o', facecolors=df['WRONG'], edgecolors=df['WRONG'])
    plt.title('Scatter plot for model comparison on holdout test (d4)')
    plt.ylabel('Updated model prediction probability')
    plt.xlabel('Base model prediction probability')
else:
    # df['WRONG'] indicates those rows where the baseline model1 predicts wrongly but updated model2 predicts correctly
    df['WRONG'] = df.apply(lambda row: 'Blue' if ((row['ROUND_PREDICT'] >= 0.5 and row['ROUND_PREDICT2'] < 0.5
                                                  and row['Presence'] == 'False') or
                                                 (row['ROUND_PREDICT'] < 0.5 and row['ROUND_PREDICT2'] >= 0.5 and
                                                  row['Presence'] == 'True')) else 'none',
                           axis=1)
    # df['WRONG2'] indicates those rows where the baseline model1 predicts correctly but updated model2 predicts wrongly
    df['WRONG2'] = df.apply(lambda row: 'Red' if ((row['ROUND_PREDICT2'] >= 0.5 and row['ROUND_PREDICT'] < 0.5 and
                                                    row['Presence'] == 'False') or
                                                   (row['ROUND_PREDICT2'] < 0.5 and row['ROUND_PREDICT'] >= 0.5 and
                                                    row['Presence'] == 'True')) else 'none',
                            axis=1)
    print('Number of wrong predictions of base model: ', len(df[df['WRONG'] == 'Red']))
    print('Number of wrong predictions of updated model: ', len(df[df['WRONG2'] == 'Blue']))
    plt.scatter(X, Y1, s=20, marker='o', facecolors=df['WRONG'], edgecolors=df['WRONG'],
                label=["predict_correct: ", "predict_wrong: "] + df['WRONG'].unique())
    plt.scatter(X, Y2, s=20, marker='o', facecolors=df['WRONG2'], edgecolors=df['WRONG2'],
                label=["predict_wrong: ", "predict_correct: "] + df['WRONG2'].unique())
    plt.title('Scatter plot for model comparison on holdout test (d13/14)')
    plt.ylabel('Prediction Probability')
    plt.xlabel('Image')

# plt.legend(loc='lower left')
plt.show()
