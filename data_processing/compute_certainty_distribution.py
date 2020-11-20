import sys
import pandas as pd
import matplotlib.pyplot as plt


if __name__ == '__main__':
    if len(sys.argv) <= 1:
        print('One input parameter, input file to draw certainty scores, is needed to run the script')
        exit(1)

    input_file = sys.argv[1]
    df = pd.read_csv(input_file, header=0, index_col='MAPPED_IMAGE', dtype={'MAPPED_IMAGE': 'str',
                                                                            'Probability': 'float'})
    df.dropna(inplace=True)
    prob_series = df['Probability']
    plt.hist(prob_series, bins=10, log=True)
    plt.show()
    print("mean:", prob_series.mean())
    print("std:", prob_series.std())

