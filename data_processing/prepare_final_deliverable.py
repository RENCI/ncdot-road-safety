import pandas as pd
import argparse


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Process arguments.')
    parser.add_argument('--input_map_file', type=str,
                        default='/projects/ncdot/secondary_road/output/d01/mapped_2lane_sr_images_d1.csv',
                        help='input mapping file with route id and mile post')
    parser.add_argument('--input_predict_file', type=str,
                        default='/projects/ncdot/secondary_road/predict/pole/predict_d01_single.csv',
                        help='input model prediction file')
    parser.add_argument('--input_predict_file_2', type=str,
                        default='',
                        help='input model prediction file for missing images to be added into input_predict_file')
    parser.add_argument('--threshold', type=float, default=0.67,
                        help='threshold for model binary classification')
    parser.add_argument('--output_file', type=str,
                        default='/projects/ncdot/secondary_road/predict/pole/deliverable/'
                                'pole_model_predict_d1_no_front.csv',
                        help='output file for final deliverable')
    parser.add_argument('--drop_front', action='store_true', default=False,
                        help='whether to drop front view image prediction for the frame prediction')

    args = parser.parse_args()
    input_map_file = args.input_map_file
    input_predict_file = args.input_predict_file
    input_predict_file_2 = args.input_predict_file_2
    threshold = args.threshold
    output_file = args.output_file
    drop_front = args.drop_front

    map_df = pd.read_csv(input_map_file, header=0, index_col=None, dtype=str,
                         usecols=['ROUTEID', 'MAPPED_IMAGE', 'MILE_POST'])
    predict_df = pd.read_csv(input_predict_file, header=0, index_col=None,
                             dtype={'MAPPED_IMAGE': str,
                                    'ROUND_PREDICT': float})
    if input_predict_file_2:
        predict_df_2 = pd.read_csv(input_predict_file_2, header=0, index_col=None,
                                   dtype={'MAPPED_IMAGE': str,
                                          'ROUND_PREDICT': float})
        predict_df = pd.concat([predict_df, predict_df_2])
    predict_df.MAPPED_IMAGE = predict_df.MAPPED_IMAGE.str.split('/').str[-1]
    predict_df.MAPPED_IMAGE = predict_df.MAPPED_IMAGE.str.replace('.jpg', '')
    if drop_front:
        predict_df.loc[predict_df.MAPPED_IMAGE.str.endswith('1'), 'ROUND_PREDICT'] = 0
    predict_df['MAPPED_IMAGE'] = predict_df.MAPPED_IMAGE.str[:-1]
    predict_df = predict_df.groupby(by=['MAPPED_IMAGE']).max()
    map_size = len(map_df)
    predict_size = len(predict_df)
    if map_size != predict_size:
        # use predict_size to filter map data frame to accommodate some malformed mapped images that cannot be predicted
        map_df = map_df[map_df.MAPPED_IMAGE.isin(predict_df.index)]
        print(f'after filtering map_df by predict_df, map_df size is {len(map_df)}, predict_df size is {predict_size}')

    predict_df['PRESENCE'] = predict_df.apply(lambda row: True if row.ROUND_PREDICT >= threshold else False, axis=1)
    map_df.set_index('MAPPED_IMAGE', inplace=True)
    df = pd.concat([map_df, predict_df], axis=1)
    df.reset_index(inplace=True)
    df.rename(columns={'index': 'MAPPED_IMAGE'}, inplace=True)
    df = df.sort_values(by=['ROUTEID', 'MILE_POST'])
    df.to_csv(output_file, index=False)
