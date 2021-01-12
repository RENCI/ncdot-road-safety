import pandas as pd
import argparse


parser = argparse.ArgumentParser(description='Process arguments.')
parser.add_argument('--input_file', type=str,
                    default='../server/metadata/d4_subset_with_manual_inspection_common.csv',
                    help='input file with path with model predictions and ground truth')

args = parser.parse_args()
input_file = args.input_file

df = pd.read_csv(input_file, header=0, index_col=False)
df_correct_yes = df[((df.ROUND_PREDICT_2 >= 0.5) & (df.manual_guardrail_YN == 'Y'))]
df_correct_no = df[((df.ROUND_PREDICT_2 < 0.5) & (df.manual_guardrail_YN == 'N'))]
df_wrong_yes = df[((df.ROUND_PREDICT_2 >= 0.5) & (df.manual_guardrail_YN == 'N'))]
df_wrong_no = df[((df.ROUND_PREDICT_2 < 0.5) & (df.manual_guardrail_YN == 'Y'))]
print("model prediction with guardrail:", df_correct_yes.shape, df_wrong_yes.shape)
print("model prediction with no guardrail:", df_correct_no.shape, df_wrong_no.shape)