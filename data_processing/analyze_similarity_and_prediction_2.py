import pandas as pd
import argparse
from analyze_similarity_and_prediction import get_concat_similarity_pred_dataframe_from_csv, filter_out_trash_images


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Process arguments.')
    parser.add_argument('--similarity_input_file', type=str,
                        default='../server/metadata/model-related/secondary_road/round4/image_similarity_scores.csv',
                        help='input file to get image similarity scores')
    parser.add_argument('--input_file_d4', type=str,
                        default='../server/metadata/model-related/secondary_road/round4/predict_d4.csv',
                        help='input prediction file for mapped images')
    parser.add_argument('--input_file_d8', type=str,
                        default='../server/metadata/model-related/secondary_road/round4/predict_d8.csv',
                        help='input prediction file for mapped images')
    parser.add_argument('--input_file_d13', type=str,
                        default='../server/metadata/model-related/secondary_road/round4/predict_d13.csv',
                        help='input prediction file for mapped images')
    parser.add_argument('--input_file_d14', type=str,
                        default='../server/metadata/model-related/secondary_road/round4/predict_d14.csv',
                        help='input prediction file for mapped images')
    parser.add_argument('--total_image_count', type=int,
                        default=30000,
                        help='total number of images to sample from unlabeled pool')
    parser.add_argument('--uncertainty_group_size', type=int,
                        default=500,
                        help='number of images in one uncertainty group for efficient query in annotation tool')
    parser.add_argument('--output_file', type=str,
                        default='../server/metadata/model-related/secondary_road/round4/image_uncertainty_scores.csv',
                        help='output file that contains uncertainty scores')

    args = parser.parse_args()
    similarity_input_file = args.similarity_input_file
    input_file_d4 = args.input_file_d4
    input_file_d8 = args.input_file_d8
    input_file_d13 = args.input_file_d13
    input_file_d14 = args.input_file_d14
    total_image_count = args.total_image_count
    uncertainty_group_size = args.uncertainty_group_size
    output_file = args.output_file

    # whole_df is sorted by SIMILARITY_YES
    whole_df = get_concat_similarity_pred_dataframe_from_csv(similarity_input_file, input_file_d4, input_file_d8,
                                                             input_file_d13, input_file_d14)
    print(whole_df.shape)

    # sample_df1 tries to capture positive images with more entropy and likely to capture FPs
    sample_df1 = whole_df[(whole_df.SIMILARITY_YES < whole_df.SIMILARITY_NO) & (whole_df.ROUND_PREDICT >= 0.5)]
    print('sample_df1:', sample_df1.shape)

    # sample_df2 tries to capture FNs with more entropy
    sample_df2 = whole_df[(whole_df.SIMILARITY_YES < 0.3) &
                          (whole_df.SIMILARITY_YES > whole_df.SIMILARITY_NO) &
                          (whole_df.ROUND_PREDICT >= 0.1)]
    print('sample_df2:', sample_df2.shape)

    # sample_df3 tries to capture FPs and FNs along decision boundary
    sample_df3 = whole_df[(whole_df.ROUND_PREDICT < 0.6) & (whole_df.ROUND_PREDICT > 0.4)]
    print('sample_df3:', sample_df3.shape)

    # sample_df4 tries to capture FPs and FNs along decision boundary by taking into account similarities
    sample_df4 = whole_df[(whole_df.SIMILARITY_YES < 0.5) & (whole_df.SIMILARITY_NO < 0.5) &
                          (whole_df.ROUND_PREDICT >= 0.5)]
    print('sample_df4:', sample_df4.shape)

    sample_df = pd.concat([sample_df1, sample_df2, sample_df3, sample_df4])
    print('connected sample_df before dropping duplicates:', sample_df.shape)
    sample_df.drop_duplicates(inplace=True)
    print('connected sample_df after dropping duplicates:', sample_df.shape)
    # sort in ascending order with most dissimilar image (smallest similarity score) on top
    dissimilar_df = whole_df[(whole_df['SIMILARITY_YES'] < 0.5) & (whole_df['SIMILARITY_NO'] < 0.5) &
                             (whole_df.SIMILARITY_YES > 0.3)]
    dissimilar_df = dissimilar_df.sort_values(by=['MIN_SIMILARITY']).head(30000-len(sample_df))
    total_sample_df = pd.concat([sample_df, dissimilar_df])
    print('total_sample_df before removing duplicates:', len(total_sample_df))
    total_sample_df.drop_duplicates(inplace=True)
    sub_size = len(total_sample_df)
    print('total_sample_df after removing duplicates:', sub_size)
    print('d4:', len(total_sample_df[total_sample_df.DIVISION == 'd4']),
          ', d8:', len(total_sample_df[total_sample_df.DIVISION == 'd8']),
          ', d13:', len(total_sample_df[total_sample_df.DIVISION == 'd13']),
          ', d14:', len(total_sample_df[total_sample_df.DIVISION == 'd14']))
    # uncertainty reflects sorting by SCORE
    total_sample_df["UNCERTAINTY"] = total_sample_df.apply(
        lambda row: sub_size - total_sample_df.index.get_loc(row.name),
        axis=1)
    total_sample_df["UNCERTAINTY_GROUP"] = total_sample_df.apply(
        lambda row: (int)(total_sample_df.index.get_loc(row.name)/uncertainty_group_size),
        axis=1)
    total_sample_df = total_sample_df.reset_index()
    total_sample_df.to_csv(output_file, index=False)
    print('Done')
