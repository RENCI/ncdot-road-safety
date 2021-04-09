import pandas as pd
import argparse
import numpy as np
import matplotlib.pyplot as plt


def get_pred_dataframe_from_csv(input_csv_file, filter_image_df=None):
    df = pd.read_csv(input_csv_file, header=0, index_col=False, usecols=['MAPPED_IMAGE', 'ROUND_PREDICT'],
                     dtype={'MAPPED_IMAGE': str, 'ROUND_PREDICT': float})
    df.MAPPED_IMAGE = df.MAPPED_IMAGE.str.strip()
    df.MAPPED_IMAGE = df.MAPPED_IMAGE.str.slice(start=-15)
    df.MAPPED_IMAGE = df.MAPPED_IMAGE.str.replace('.jpg', '')
    if filter_image_df is not None:
        df = df[df.MAPPED_IMAGE.isin(filter_image_df['MAPPED_IMAGE'])]
    df = df.set_index('MAPPED_IMAGE')
    return df


def compute_score(db, prob, sd=0.2):
    """
    Compute a score for image sampling.
    :param db: decision boundary
    :param prob: model prediction
    :param sd: standard deviation for normal distribution, which will determine how far away from
    the decision boundary to sample
    :return: a score used for uncertainty based image sampling
    """
    return abs(prob-db) + np.random.normal(0, sd)


def get_uniform_random_samples(df, initial_score, sample_n=5):
    """
    random sampling across divisions with uncertainty reflecting sorting order starting from initial_score and
    descreasing by one for the next sorted item
    :param df: data frame to be sampled
    :param initial_score: initial uncertainty sorting score
    :param sample_n: sampling size for each division before sampling the next division
    :return: data frame that contains uniformly sampled data
    """
    size = len(df)
    idx = 0
    sample_df = None
    while idx < size:
        group_size = len(df.groupby('DIVISION'))
        if sample_df is None:
            sample_df = df.groupby('DIVISION').sample(n=sample_n, random_state=42)
            sample_df["UNCERTAINTY"] = sample_df.apply(lambda row: initial_score - sample_df.index.get_loc(row.name),
                                                       axis=1)
            idx += sample_n * group_size
        else:
            score = initial_score - len(sample_df)
            min_size = df.groupby('DIVISION').size().min()
            if min_size < sample_n:
                new_sample_df = df.groupby('DIVISION').sample(n=min_size, random_state=42)
                idx += min_size * group_size
            else:
                new_sample_df = df.groupby('DIVISION').sample(n=sample_n, random_state=42)
                idx += sample_n * group_size
            new_sample_df["UNCERTAINTY"] = new_sample_df.apply(lambda row: score-new_sample_df.index.get_loc(row.name),
                                                               axis=1)
            sample_df = pd.concat([sample_df, new_sample_df])

        df = df[~df.index.isin(sample_df.index)]
        # if idx % 100000 == 0:
        #     sample_df.to_csv(output_file + '.' + str(idx))
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
    sub_df = df_yes.sample(n=20000, weights='WEIGHT', replace=False, random_state=1)
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


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Process arguments.')
    parser.add_argument('--input_file_d4', type=str,
                        default='../server/metadata/model-related/secondary_road/round2/predict_d4.csv',
                        help='input prediction file for mapped images to create uncertainty scores for')
    parser.add_argument('--d4_db', type=float, default=0.01, help='decision boundary for division 4')
    parser.add_argument('--input_file_d8', type=str,
                        default='../server/metadata/model-related/secondary_road/round2/predict_d8.csv',
                        help='input prediction file for mapped images to create uncertainty scores for')
    parser.add_argument('--d8_db', type=float, default=0, help='decision boundary for division 8')
    parser.add_argument('--input_file_d13', type=str,
                        default='../server/metadata/model-related/secondary_road/round2/predict_d13.csv',
                        help='input prediction file for mapped images to create uncertainty scores for')
    parser.add_argument('--input_file_d14', type=str,
                        default='../server/metadata/model-related/secondary_road/round2/predict_d14.csv',
                        help='input prediction file for mapped images to create uncertainty scores for')
    parser.add_argument('--d1314_db', type=float, default=0.08, help='decision boundary for division 13/14')
    parser.add_argument('--remain_image_name_file', type=str,
                        default='../server/metadata/remain_image_base_names.csv',
                        help='input image base names remaining to create uncertainty scores for')
    parser.add_argument('--output_file', type=str,
                        default='../server/metadata/image_uncertainty_scores_round2.csv',
                        help='output file for uncertainty scores of the mapped images to ingest into annotation tool db')


    args = parser.parse_args()
    input_file_d4 = args.input_file_d4
    input_file_d8 = args.input_file_d8
    input_file_d13 = args.input_file_d13
    input_file_d14 = args.input_file_d14
    d4_db = args.d4_db
    d8_db = args.d8_db
    d1314_db = args.d1314_db
    remain_image_name_file = args.remain_image_name_file
    output_file = args.output_file

    np.random.seed(1)

    remain_image_df = pd.read_csv(remain_image_name_file, header=0, dtype=str)
    df_d4 = get_pred_dataframe_from_csv(input_file_d4, filter_image_df=remain_image_df)
    print('d4 shape', df_d4.shape)
    df_d8 = get_pred_dataframe_from_csv(input_file_d8, filter_image_df=remain_image_df)
    print('d8 shape', df_d8.shape)
    df_d13 = get_pred_dataframe_from_csv(input_file_d13, filter_image_df=remain_image_df)
    print('d13 shape', df_d13.shape)
    df_d14 = get_pred_dataframe_from_csv(input_file_d14, filter_image_df=remain_image_df)
    print('d14 shape', df_d14.shape)

    df_d4['DIVISION'] = 'd4'
    df_d8['DIVISION'] = 'd8'
    df_d13['DIVISION'] = 'd13'
    df_d14['DIVISION'] = 'd14'

    df_d4['SCORE'] = df_d4.apply(lambda row: compute_score(d4_db, row['ROUND_PREDICT'], 0.16), axis=1)
    df_d8['SCORE'] = df_d8.apply(lambda row: compute_score(d8_db, row['ROUND_PREDICT'], 0.16), axis=1)
    df_d13['SCORE'] = df_d13.apply(lambda row: compute_score(d1314_db, row['ROUND_PREDICT'], 0.2), axis=1)
    df_d14['SCORE'] = df_d14.apply(lambda row: compute_score(d1314_db, row['ROUND_PREDICT'], 0.2), axis=1)
    whole_df = pd.concat([df_d4, df_d8, df_d13, df_d14])
    whole_df = whole_df.sort_values(by=['SCORE'])
    whole_size = len(whole_df)
    df_10k = whole_df.head(10000)
    print(whole_size, ', d4:', len(df_10k[df_10k.DIVISION=='d4']), ', d8:', len(df_10k[df_10k.DIVISION=='d8']),
          ', d13:', len(df_10k[df_10k.DIVISION=='d13']), ', d14:', len(df_10k[df_10k.DIVISION=='d14']))
    # uncertainty reflects sorting by SCORE
    whole_df["UNCERTAINTY"] = whole_df.apply(lambda row: whole_size - whole_df.index.get_loc(row.name), axis=1)
    whole_df.to_csv(output_file)
    print('Done')
