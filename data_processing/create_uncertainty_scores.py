import pandas as pd
import argparse
import numpy as np
import matplotlib.pyplot as plt


def get_dataframe_from_csv(input_csv_file):
    return pd.read_csv(input_csv_file, header=0, index_col=['MAPPED_IMAGE'], usecols=['MAPPED_IMAGE', 'ROUND_PREDICT'],
                       dtype={'MAPPED_IMAGE': str, 'ROUND_PREDICT': float})


def get_uniform_random_samples(df, initial_score, sample_n=5):
    """
    random sampling across divisions with uncertainty reflecting sorting order starting from initial_score and
    descreasing by one for the next sorted item
    :param df: data frame to be sampled
    :param initial_score: initial uncertainty sorting socre
    :param sample_n: sampling size for each division before sampling the next division
    :return: data frame that contains uniformly sampled data
    """
    size = len(df)
    idx = 0
    sample_df = None
    while idx < size:
        if sample_df is None:
            sample_df = df.groupby('DIVISION').sample(n=sample_n, random_state=42)
            sample_df["UNCERTAINTY"] = sample_df.apply(lambda row: initial_score - sample_df.index.get_loc(row.name),
                                                       axis=1)
        else:
            score = initial_score - len(sample_df)
            min_size = df.groupby('DIVISION').size().min()
            if min_size < sample_n:
                new_sample_df = df.groupby('DIVISION').sample(n=min_size, random_state=42)
            else:
                new_sample_df = df.groupby('DIVISION').sample(n=sample_n, random_state=42)
            new_sample_df["UNCERTAINTY"] = new_sample_df.apply(lambda row: score-new_sample_df.index.get_loc(row.name),
                                                               axis=1)
            sample_df = pd.concat([sample_df, new_sample_df])

        df = df[~df.index.isin(sample_df.index)]
        idx += sample_n * 4
        if idx % 100000 == 0:
            sample_df.to_csv(output_file + '.' + str(idx))
    return sample_df


def get_shuffled_set(df, positive=True):
    if positive is True:
        sub_df = df[df.ROUND_PREDICT >= 0.5]
    else:
        sub_df = df[df.ROUND_PREDICT < 0.5]
    return sub_df.sample(frac=1, random_state=42)


def get_sub_samples_by_distribution(df):
    # currently unused
    # drop negative predictions
    df_yes = df[df.ROUND_PREDICT >= 0.5]
    print(f'positive predictions: {df_yes.shape}')
    print(f'1.0 predictions: {df[df.ROUND_PREDICT == 1.0].shape}')
    plt.hist(df_yes['ROUND_PREDICT'], bins=5, log=True)
    plt.show()
    hist, bin_edges = np.histogram(df_yes['ROUND_PREDICT'], bins=5, density=True)
    bin_edges[5] = 1.1
    print(f'bins: {bin_edges}, hists: {hist}')

    df_yes['BIN_INDEX'] = np.digitize(df_yes['ROUND_PREDICT'], bin_edges)
    # create random sampling with the same distribution as positive prediction data while giving west regions
    # such as division 13 more weight
    df_yes['WEIGHT'] = hist[df_yes['BIN_INDEX'] - 1] * df_yes['DIVISION_WEIGHT']
    sub_df = df_yes.sample(n=sample_size, weights='WEIGHT', replace=False, random_state=1)
    plt.hist(sub_df['ROUND_PREDICT'], bins=[0.5, 0.6, 0.7, 0.8, 0.9, 1], log=True)
    plt.show()
    print(sub_df[sub_df['DIVISION_WEIGHT'] == 1.5])
    print(sub_df[sub_df['DIVISION_WEIGHT'] == 1])
    # uncertainty would be in the range of [0.1, 0.6]
    # where predict probability of 0.5 has higher uncertainty than
    # predict probability of 1.0
    sub_df['UNCERTAINTY'] = (1.1 - sub_df['ROUND_PREDICT']) * sub_df['DIVISION_WEIGHT']
    sub_df['UNCERTAINTY'] = np.round(sub_df['UNCERTAINTY'], decimals=2)
    print(sub_df[sub_df['UNCERTAINTY'] > 0.2])
    sub_df = sub_df.drop(columns=['BIN_INDEX', 'WEIGHT'])
    sub_df.index = sub_df.index.str.slice(start=-15)
    sub_df.index = sub_df.index.str.replace('.jpg', '')
    sub_df = sub_df.sort_values(by=['UNCERTAINTY'], ascending=False)
    return sub_df


parser = argparse.ArgumentParser(description='Process arguments.')
parser.add_argument('--input_file_d4', type=str,
                    default='../server/metadata/model-related/secondary_road/model_2lane_predict_d4.csv',
                    help='input prediction file for mapped images to create uncertainty scores for')
parser.add_argument('--input_file_d8', type=str,
                    default='../server/metadata/model-related/secondary_road/model_2lane_predict_d8.csv',
                    help='input prediction file for mapped images to create uncertainty scores for')
parser.add_argument('--input_file_d13', type=str,
                    default='../server/metadata/model-related/secondary_road/model_2lane_predict_d13.csv',
                    help='input prediction file for mapped images to create uncertainty scores for')
parser.add_argument('--input_file_d14', type=str,
                    default='../server/metadata/model-related/secondary_road/model_2lane_predict_d14.csv',
                    help='input prediction file for mapped images to create uncertainty scores for')
parser.add_argument('--sample_size', type=int,
                    default=20000,
                    help='sample size for manual annotation with uncertainty scores computed to be ingested into db')
parser.add_argument('--output_file', type=str,
                    default='../server/metadata/image_uncertainty_scores.csv',
                    help='output file for uncertainty scores of the mapped images to ingest into annotation tool db')


args = parser.parse_args()
input_file_d4 = args.input_file_d4
input_file_d8 = args.input_file_d8
input_file_d13 = args.input_file_d13
input_file_d14 = args.input_file_d14
sample_size = args.sample_size
output_file = args.output_file

df_d4 = get_dataframe_from_csv(input_file_d4)
df_d8 = get_dataframe_from_csv(input_file_d8)
df_d13 = get_dataframe_from_csv(input_file_d13)
df_d14 = get_dataframe_from_csv(input_file_d14)
print(df_d4.shape, df_d8.shape, df_d13.shape, df_d14.shape)

df_d4['DIVISION'] = 'd4'
df_d8['DIVISION'] = 'd8'
df_d13['DIVISION'] = 'd13'
df_d14['DIVISION'] = 'd14'

# df_d4['DIVISION_WEIGHT'] = 1
# df_d8['DIVISION_WEIGHT'] = 1
# df_d13['DIVISION_WEIGHT'] = 1.5
# df_d14['DIVISION_WEIGHT'] = 1.5

whole_df = pd.concat([df_d4, df_d8, df_d13, df_d14])
whole_size = len(whole_df)
# uncertainty currently only reflects sorting
whole_df['UNCERTAINTY'] = whole_size
print(len(whole_df[whole_df.ROUND_PREDICT >= 0.5]))
whole_df_pos = get_uniform_random_samples(whole_df[whole_df.ROUND_PREDICT >= 0.5], whole_size)
pos_size = len(whole_df_pos)
print(pos_size)
whole_df_neg = get_uniform_random_samples(whole_df[whole_df.ROUND_PREDICT < 0.5], whole_size - pos_size)
whole_df_sorted = pd.concat([whole_df_pos, whole_df_neg])

# sub_df = get_sub_samples_by_distribution(whole_df)
whole_df_sorted.to_csv(output_file)
print('Done')
