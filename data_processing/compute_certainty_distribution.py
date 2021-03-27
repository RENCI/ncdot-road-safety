import sys
import pandas as pd
import argparse
import matplotlib.pyplot as plt


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Process arguments.')
    parser.add_argument('--input_file', type=str,
                        default='../server/metadata/model_predict_test_round3.csv',
                        help='input file with path with model predictions')

    args = parser.parse_args()
    input_file = args.input_file

    df = pd.read_csv(input_file, header=0, index_col='MAPPED_IMAGE', dtype={'MAPPED_IMAGE': 'str',
                                                                            'ROUND_PREDICT': 'float'})
    df.dropna(inplace=True)
    prob_series = df['ROUND_PREDICT']
    # prob_series = df[df.index.str.startswith('d13') | df.index.str.startswith('d14')]['ROUND_PREDICT']
    plt.hist(prob_series, bins=10, log=True)
    plt.show()
    print("mean:", prob_series.mean())
    print("std:", prob_series.std())
    prob_series_yes = df['ROUND_PREDICT'][df['ROUND_PREDICT'] >= 0.5]
    prob_series_no = df['ROUND_PREDICT'][df['ROUND_PREDICT'] < 0.5]
    prob_series_1 = df['ROUND_PREDICT'][df['ROUND_PREDICT'] == 1.0]
    print(f'{len(prob_series_yes)}, {len(prob_series_no)}, {len(prob_series)}')
    print(len(prob_series_1), len(prob_series_1)/len(prob_series))


