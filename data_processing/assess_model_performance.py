import pandas as pd
import argparse


parser = argparse.ArgumentParser(description='Process arguments.')
parser.add_argument('--input_file', type=str,
                    default='../server/metadata/d4_subset_with_manual_inspection.csv',
                    help='input file with path with model predictions and ground truth')

args = parser.parse_args()
input_file = args.input_file

df = pd.read_csv(input_file, header=0, index_col=False)
df_2_correct = df[((df.ROUND_PREDICT_2 >= 0.5) & (df.manual_guardrail_YN == 'Y')) | ((df.ROUND_PREDICT_2 < 0.5) & (df.manual_guardrail_YN == 'N'))]
df_4_correct = df[((df.ROUND_PREDICT_4 >= 0.5) & (df.manual_guardrail_YN == 'Y')) | ((df.ROUND_PREDICT_4 < 0.5) & (df.manual_guardrail_YN == 'N'))]
df_2_wrong = df[((df.ROUND_PREDICT_2 >= 0.5) & (df.manual_guardrail_YN == 'N')) | ((df.ROUND_PREDICT_2 < 0.5) & (df.manual_guardrail_YN == 'Y'))]
df_4_wrong = df[((df.ROUND_PREDICT_4 >= 0.5) & (df.manual_guardrail_YN == 'N')) | ((df.ROUND_PREDICT_4 < 0.5) & (df.manual_guardrail_YN == 'Y'))]
print("2 lane model prediction:", df_2_correct.shape, df_2_wrong.shape)
print("4 lane model prediction:", df_4_correct.shape, df_4_wrong.shape)
