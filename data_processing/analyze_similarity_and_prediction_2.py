import pandas as pd
import argparse
import matplotlib.pyplot as plt
from analyze_similarity_and_prediction import get_concat_similarity_pred_dataframe_from_csv, filter_out_trash_images


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Process arguments.')
    parser.add_argument('--similarity_input_file', type=str,
                        default='../server/metadata/model-related/secondary_road/round3/image_similarity_scores.csv',
                        help='input file to get image similarity scores')
    parser.add_argument('--input_file_d4', type=str,
                        default='../server/metadata/model-related/secondary_road/round3/predict_d4.csv',
                        help='input prediction file for mapped images')
    parser.add_argument('--input_file_d8', type=str,
                        default='../server/metadata/model-related/secondary_road/round3/predict_d8.csv',
                        help='input prediction file for mapped images')
    parser.add_argument('--input_file_d13', type=str,
                        default='../server/metadata/model-related/secondary_road/round3/predict_d13.csv',
                        help='input prediction file for mapped images')
    parser.add_argument('--input_file_d14', type=str,
                        default='../server/metadata/model-related/secondary_road/round3/predict_d14.csv',
                        help='input prediction file for mapped images')
    parser.add_argument('--positive_image_count', type=int,
                        default=20000,
                        help='number of images most similar to the positive class centroid to select')
    parser.add_argument('--dissimilar_image_count', type=int,
                        default=20000,
                        help='number of images most dissimilar to both positive and negative class centroids to select')
    parser.add_argument('--partition', type=int,
                        default=8,
                        help='partitions to use for splitting positive_image_count and dissimilar_image_count to '
                             'create mixed samples between the two. For example, with default values, 2500 samples '
                             'are selected from each in alternation between 2 sets')
    parser.add_argument('--uncertainty_group_size', type=int,
                        default=500,
                        help='number of images in one uncertainty group for efficient query in annotation tool')
    parser.add_argument('--sim_yes_output_file', type=str,
                        default='../server/metadata/model-related/secondary_road/round3/image_sim_yes_20k.csv',
                        help='output file that contains 20k most similar images to positive class centroid')
    parser.add_argument('--dissim_output_file', type=str,
                        default='../server/metadata/model-related/secondary_road/round3/image_dissim_20k_2.csv',
                        help='output file that contains 20k most dissimilar images to both centroid with similarity '
                             'less than the threshold set by dissim_similarity_threshold argument')
    parser.add_argument('--output_file', type=str,
                        default='../server/metadata/model-related/secondary_road/round3/image_uncertainty_scores_2.csv',
                        help='output file that contains uncertainty scores')

    args = parser.parse_args()
    similarity_input_file = args.similarity_input_file
    input_file_d4 = args.input_file_d4
    input_file_d8 = args.input_file_d8
    input_file_d13 = args.input_file_d13
    input_file_d14 = args.input_file_d14
    positive_image_count = args.positive_image_count
    dissimilar_image_count = args.dissimilar_image_count
    partition = args.partition
    uncertainty_group_size = args.uncertainty_group_size
    output_file = args.output_file
    sim_yes_output_file = args.sim_yes_output_file
    dissim_output_file = args.dissim_output_file

    # whole_df is sorted by SIMILARITY_YES
    whole_df = get_concat_similarity_pred_dataframe_from_csv(similarity_input_file, input_file_d4, input_file_d8,
                                                             input_file_d13, input_file_d14)
    print(whole_df.shape)

    # analyze the first 10K images, sorted in descending order with most similar image (largest SIMILARITY_YES score
    # on top, that are most similar to the positive class centroid and the top 10K images that are most dissimilar
    # to both centroids
    sim_yes_sub_df = whole_df.head(positive_image_count)
    #plt.hist(sim_yes_sub_df['ROUND_PREDICT'], bins=10)
    #plt.show()
    # sim_yes_sub_df.to_csv(sim_yes_output_file)
    # sort in ascending order with most dissimilar image (smallest similarity score) on top
    dissimilar_sub_df = whole_df.sort_values(by=['MAX_SIMILARITY']).head(dissimilar_image_count)
    dissimilar_sub_df = filter_out_trash_images(dissimilar_sub_df)
    # plt.hist(dissimilar_sub_df['ROUND_PREDICT'], bins=10)
    # plt.show()
    dissimilar_sub_df.to_csv(dissim_output_file)
    sub_df_list = []
    sim_len = (int)(positive_image_count / partition)
    dissimilar_len = (int)(dissimilar_image_count / partition)
    for idx in range(partition):
        sub_df_list.append(sim_yes_sub_df[idx*sim_len:idx*sim_len+sim_len])
        sub_df_list.append(dissimilar_sub_df[idx * dissimilar_len:idx*dissimilar_len+dissimilar_len])
    sub_df = pd.concat(sub_df_list)
    print('sub_df before removing duplicates', len(sub_df))
    sub_df.drop_duplicates(inplace=True)
    print('sub_df after removing duplicates', len(sub_df))
    sub_size = len(sub_df)
    print(sub_size, ', d4:', len(sub_df[sub_df.DIVISION == 'd4']), ', d8:', len(sub_df[sub_df.DIVISION == 'd8']),
          ', d13:', len(sub_df[sub_df.DIVISION == 'd13']), ', d14:', len(sub_df[sub_df.DIVISION == 'd14']))
    # uncertainty reflects sorting by SCORE
    sub_df["UNCERTAINTY"] = sub_df.apply(lambda row: sub_size - sub_df.index.get_loc(row.name), axis=1)
    sub_df["UNCERTAINTY_GROUP"] = sub_df.apply(lambda row: (int)(sub_df.index.get_loc(row.name)/uncertainty_group_size),
                                               axis=1)
    sub_df = sub_df.reset_index()
    sub_df.to_csv(output_file, index=False)
    print('Done')
