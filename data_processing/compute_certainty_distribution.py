import sys
import pandas as pd
import matplotlib.pyplot as plt


if __name__ == '__main__':
    if len(sys.argv) <= 1:
        print('One input parameter, input file to draw certainty scores, is needed to run the script')
        exit(1)

    input_file = sys.argv[1]
    df = pd.read_csv(input_file, header=0, index_col='MAPPED_IMAGE', dtype={'MAPPED_IMAGE': 'str',
                                                                            'ROUND_PREDICT': 'float'})
    df.dropna(inplace=True)
    prob_series = df['ROUND_PREDICT']
    plt.hist(prob_series, bins=10, log=True)
    plt.show()
    print("mean:", prob_series.mean())
    print("std:", prob_series.std())
    prob_series_yes = df['ROUND_PREDICT'][df['ROUND_PREDICT'] >= 0.5]
    prob_series_no = df['ROUND_PREDICT'][df['ROUND_PREDICT'] < 0.5]
    prob_series_1 = df['ROUND_PREDICT'][df['ROUND_PREDICT'] == 1.0]
    print(f'{len(prob_series_yes)}, {len(prob_series_no)}, {len(prob_series)}')
    print(len(prob_series_1), len(prob_series_1)/len(prob_series))


