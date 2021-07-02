import pandas as pd
import argparse


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Process arguments.')
    parser.add_argument('--input_map_file', type=str,
                        default='/projects/ncdot/secondary_road/output/d13/mapped_2lane_sr_images_d13.csv',
                        help='input mapping file with route id and mile post')
    parser.add_argument('--input_predict_file', type=str,
                        default='/projects/ncdot/secondary_road/predict/guardrail/predict_d13_single.csv',
                        help='input model prediction file')
    parser.add_argument('--threshold', type=float, default=0.8,
                        help='threshold for model binary classification')
    parser.add_argument('--output_file', type=str,
                        default='/projects/ncdot/secondary_road/predict/guardrail/guardrail_model_predict_d13.csv',
                        help='output file for final deliverable')

    args = parser.parse_args()
    input_map_file = args.input_map_file
    input_predict_file = args.input_predict_file
    threshold = args.threshold
    output_file = args.output_file

    map_df = pd.read_csv(input_map_file, header=0, index_col='MAPPED_IMAGE', dtype=str,
                         usecols=['ROUTEID', 'MAPPED_IMAGE', 'MILE_POST'])
    predict_df = pd.read_csv(input_predict_file, header=0, index_col=None,
                             dtype={'MAPPED_IMAGE': str,
                                    'ROUND_PREDICT': float})
    predict_df.MAPPED_IMAGE = predict_df.MAPPED_IMAGE.str.split('/').str[-1]
    predict_df.MAPPED_IMAGE = predict_df.MAPPED_IMAGE.str.replace('.jpg', '')
    predict_df['MAPPED_IMAGE'] = predict_df.MAPPED_IMAGE.str[:-1]
    predict_df = predict_df.groupby(by=['MAPPED_IMAGE']).max()
    map_size = len(map_df)
    predict_size = len(predict_df)
    if map_size != predict_size:
        print(f'mapping file and prediction file have different size, exiting. {map_size} != {predict_size}')
        exit(1)
    predict_df['PRESENCE'] = predict_df.apply(lambda row: True if row.ROUND_PREDICT >= threshold else False, axis=1)
    df = pd.concat([map_df, predict_df], axis=1)
    df.sort_values(by=['ROUTEID', 'MILE_POST'], inplace=True)
    df.reset_index(inplace=True)
    df.rename(columns={'index':'MAPPED_IMAGE'}, inplace=True)
    df.to_csv(output_file, index=False)
