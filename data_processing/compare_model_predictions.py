import argparse
import pandas as pd


parser = argparse.ArgumentParser(description='Process arguments.')
parser.add_argument('--predict_base_file', type=str,
                    default='../server/metadata/model-related/secondary_road/base/model_2lane_predict_d14.csv',
                    help='baseline model prediction')
parser.add_argument('--predict1_file', type=str,
                    default='../server/metadata/model-related/secondary_road/round1/predict_d14.csv',
                    help='AL round1 prediction')
parser.add_argument('--predict2_file', type=str,
                    default='../server/metadata/model-related/secondary_road/round2/predict_d14.csv',
                    help='AL round2 prediction')
parser.add_argument('--output_file', type=str,
                    default='../server/metadata/predict_d14_committee.csv',
                    help='output file for combined model predictions for the committee')

args = parser.parse_args()
predict_base_file = args.predict_base_file
predict1_file = args.predict1_file
predict2_file = args.predict2_file
output_file = args.output_file

base_df = pd.read_csv(predict_base_file, header=0, index_col='MAPPED_IMAGE', usecols=['MAPPED_IMAGE', 'ROUND_PREDICT'],
                      dtype={'MAPPED_IMAGE': 'str', 'ROUND_PREDICT': 'float'})
round1_df = pd.read_csv(predict1_file, header=0, index_col='MAPPED_IMAGE', dtype={'MAPPED_IMAGE': 'str',
                                                                                      'ROUND_PREDICT': 'float'})
round1_df = round1_df.rename(columns={'ROUND_PREDICT': 'ROUND_PREDICT1'})
round2_df = pd.read_csv(predict2_file, header=0, index_col='MAPPED_IMAGE', dtype={'MAPPED_IMAGE': 'str',
                                                                                      'ROUND_PREDICT': 'float'})
round2_df = round2_df.rename(columns={'ROUND_PREDICT': 'ROUND_PREDICT2'})
concat_df = pd.concat([base_df, round1_df, round2_df], axis=1)
pos_same = len(concat_df[(concat_df.ROUND_PREDICT > 0.5) &
                         (concat_df.ROUND_PREDICT1 > 0.5) & (concat_df.ROUND_PREDICT2 > 0.5)])
neg_same = len(concat_df[(concat_df.ROUND_PREDICT <= 0.5) &
                         (concat_df.ROUND_PREDICT1 <= 0.5) & (concat_df.ROUND_PREDICT2 <= 0.5)])
print(pos_same, neg_same, len(concat_df) - pos_same - neg_same, len(concat_df))
concat_df.to_csv(output_file)
