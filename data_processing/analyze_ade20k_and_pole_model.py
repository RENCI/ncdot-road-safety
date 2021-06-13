import pandas as pd
import argparse


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Process arguments.')
    parser.add_argument('--predict_input_file1', type=str,
                        default='../server/metadata/pole/ncdot_pole_annotations.csv',
                        help='input file to get ade20k model prediction from')
    parser.add_argument('--predict_input_file2', type=str,
                        default='../server/metadata/pole/round2/model_predict_al_sample.csv',
                        help='input file to get ade20k model prediction from')
    parser.add_argument('--uncertainty_group_size', type=int,
                        default=500,
                        help='number of images in one uncertainty group for efficient query in annotation tool')
    parser.add_argument('--output_file', type=str,
                        default='../server/metadata/pole/round2/image_uncertainty_scores.csv',
                        help='output file that contains uncertainty scores')

    args = parser.parse_args()
    predict_input_file1 = args.predict_input_file1
    predict_input_file2 = args.predict_input_file2
    uncertainty_group_size = args.uncertainty_group_size
    output_file = args.output_file

    ade_df = pd.read_csv(predict_input_file1, index_col=None, usecols=['MAPPED_IMAGE', 'POLES_ALL'],
                         dtype={'MAPPED_IMAGE': str, 'POLES_ALL': bool})
    model_df = pd.read_csv(predict_input_file2, index_col=None)
    model_df.MAPPED_IMAGE = model_df.MAPPED_IMAGE.str.split('/').str[-1].str.split('.').str[0]
    model_df['GROUP'] = model_df.MAPPED_IMAGE.str[:-1]
    model_df['PREDICT_GROUP'] = model_df.apply(lambda row: 1 if row.ROUND_PREDICT>=0.5 else 0, axis=1)
    model_df.drop(columns=['ROUND_PREDICT'], inplace=True)
    model_df = model_df.groupby(by=['GROUP']).sum()
    model_df.reset_index(inplace=True)
    model_df.GROUP = model_df.GROUP.astype('string')
    ade_df = ade_df[ade_df.MAPPED_IMAGE.isin(model_df.GROUP)]
    print('ade_df:', ade_df.shape, 'model_df:', model_df.shape)
    ade_df.set_index('MAPPED_IMAGE', inplace=True)
    model_df.set_index('GROUP', inplace=True)
    concat_df = pd.concat([ade_df, model_df], axis=1)
    disagree_df = concat_df[((concat_df.POLES_ALL == True) & (concat_df.PREDICT_GROUP == 0)) |
                            ((concat_df.POLES_ALL == False) & (concat_df.PREDICT_GROUP > 0))]
    agree_df = concat_df[((concat_df.POLES_ALL == True) & (concat_df.PREDICT_GROUP > 0)) |
                         ((concat_df.POLES_ALL == False) & (concat_df.PREDICT_GROUP == 0))]

    print('disagree_df:', disagree_df.shape, 'agree_df:', agree_df.shape)

    # sort with the 893 images with positive ade model prediction and negative model prediction, followed by
    # 7608 images with negative ade model prediction and positive model prediction
    disagree_df = disagree_df.sort_values(by=['POLES_ALL', 'PREDICT_GROUP'], ascending=False)
    agree_df = agree_df.sort_values(by=['POLES_ALL', 'PREDICT_GROUP'], ascending=False)
    sample_df = pd.concat([disagree_df, agree_df])
    size = len(sample_df)
    indices = sample_df.index
    # uncertainty reflects sorting by SCORE
    sample_df["UNCERTAINTY"] = sample_df.apply(lambda row: size - indices.get_loc(row.name),
                                                   axis=1)
    sample_df["UNCERTAINTY_GROUP"] = sample_df.apply(
        lambda row: (int)(indices.get_loc(row.name)/uncertainty_group_size),
        axis=1)
    sample_df = sample_df.reset_index()
    sample_df.to_csv(output_file, index=False)
    print('Done')
