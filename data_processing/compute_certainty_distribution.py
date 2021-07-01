import pandas as pd
import argparse
import matplotlib.pyplot as plt


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Process arguments.')
    parser.add_argument('--input_file', type=str,
                        default='../server/metadata/predict/guardrail/predict_d13_single.csv',
                        help='input file with path with model predictions')
    parser.add_argument('--threshold', type=float, default=0.8,
                        help='threshold for model binary classification')
    parser.add_argument('--title', type=str, default='D13 guardrail model single image prediction distribution',
                        help='title to put on the plot')
    parser.add_argument('--joined', type=bool, default=False, help='compute certainty distribution for joined images')

    args = parser.parse_args()
    input_file = args.input_file
    title = args.title
    threshold = args.threshold
    joined = args.joined

    df = pd.read_csv(input_file, header=0, index_col=None, dtype={'MAPPED_IMAGE': 'str',
                                                                  'ROUND_PREDICT': 'float'})
    df.dropna(inplace=True)
    df['MAPPED_IMAGE'] = df['MAPPED_IMAGE'].str.replace('.jpg', '')
    df['MAPPED_IMAGE'] = df['MAPPED_IMAGE'].str.split('/').str[-1]
    if joined and len(df.MAPPED_IMAGE[0]) == 12:
        # single image prediction, need to create joined image prediction
        df.MAPPED_IMAGE = df.MAPPED_IMAGE.str[:-1]
        df = df.groupby(by=['MAPPED_IMAGE']).max()
    prob_series = df['ROUND_PREDICT']
    # prob_series = df[df.index.str.startswith('d13') | df.index.str.startswith('d14')]['ROUND_PREDICT']
    plt.title(title)
    plt.hist(prob_series, bins=10, log=True)
    plt.show()
    print("mean:", prob_series.mean())
    print("std:", prob_series.std())
    prob_series_yes = df['ROUND_PREDICT'][df['ROUND_PREDICT'] >= threshold]
    prob_series_no = df['ROUND_PREDICT'][df['ROUND_PREDICT'] < threshold]
    prob_series_1 = df['ROUND_PREDICT'][df['ROUND_PREDICT'] == 1.0]
    print(f'{len(prob_series_yes)}, {len(prob_series_no)}, {len(prob_series)}')
    print(len(prob_series_1), len(prob_series_1)/len(prob_series))
