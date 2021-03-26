import pandas as pd
import argparse
import os


parser = argparse.ArgumentParser(description='Process arguments.')
parser.add_argument('--input_file', type=str,
                    default='/projects/ncdot/NC_2018_Secondary/active_learning/guardrail/holdout_test/'
                            'annot_data/user_annoted_image_info_d4.txt',
                    help='input file with path for user annotated images to create image data')
parser.add_argument('--input_prefix_dir', type=str,
                    default='/projects/ncdot/NC_2018_Secondary/images',
                    help='root directory to create active learning data in')
parser.add_argument('--output_file', type=str,
                    default='/projects/ncdot/NC_2018_Secondary/active_learning/guardrail/holdout_test/'
                            'annot_data/user_annotated_balanced_image_info_d4.txt',
                    help='output file for selected test holdout data')
parser.add_argument('--balance_data', action='store_true', default=False,
                    help='if set, will balance data by randomly sampling negative set to make it '
                         'balanced with the positive set')
parser.add_argument('--output_root_dir', type=str,
                    default='/projects/ncdot/NC_2018_Secondary/active_learning/guardrail/holdout_test/data',
                    help='output root directory to create test holdout data in')


args = parser.parse_args()
input_file = args.input_file
input_prefix_dir = args.input_prefix_dir
output_file = args.output_file
output_root_dir = args.output_root_dir
balance_data = args.balance_data

df = pd.read_csv(input_file, header=0, index_col=False, dtype=str, usecols=['Image', 'Presence'])
df = df.drop_duplicates(subset=['Image'])
print(df.shape)
if balance_data:
    pos_df = df[df.Presence == 'True']
    pos_cnt = len(pos_df)
    neg_df = df[df.Presence == 'False']
    neg_df = neg_df.sample(n=pos_cnt, random_state=42)
    df = pd.concat([pos_df, neg_df])
    df.to_csv(output_file, index=False)


def prepare_image(src, dst):
    dst_path = os.path.dirname(dst)
    os.makedirs(dst_path, exist_ok=True)
    os.symlink(src, dst)
    return


df.apply(lambda row: prepare_image(os.path.join(input_prefix_dir, row['Image']),
                                   os.path.join(output_root_dir, 'yes' if row['Presence'] == 'True' else 'no',
                                                     row['Image'])), axis=1)
print('Done')
