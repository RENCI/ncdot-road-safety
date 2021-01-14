import pandas as pd
import argparse


parser = argparse.ArgumentParser(description='Process arguments.')
parser.add_argument('--input_file', type=str,
                    default='../server/metadata/model-related/training_image_guardrail_yn_2lanes.csv',
                    help='input file with path to create roc curve from')
parser.add_argument('--subset_size', type=int,
                    default=30,
                    help='number of images in the subset')
parser.add_argument('--output_file', type=str,
                    default='../server/metadata/model-related/training_image_guardrail_y_subset_30.csv',
                    help='number of images in the subset')
args = parser.parse_args()
input_file = args.input_file
subset_size = args.subset_size
output_file = args.output_file

df = pd.read_csv(input_file, header=0, index_col=False,
                 dtype={'MAPPED_IMAGE': str,
                        'GUARDRAIL_YN': str})
print(len(df))
df.drop(df[df.GUARDRAIL_YN == 'N'].index, inplace=True)
sub_df = df.sample(n=subset_size, random_state=1)
sub_df.drop(columns=['GUARDRAIL_YN'], inplace=True)
sub_df.to_csv(output_file, index=False)
