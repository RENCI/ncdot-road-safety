import pandas as pd
import argparse
import os

from utils import split_to_train_valid_test_for_al, create_yes_no_sub_dirs


parser = argparse.ArgumentParser(description='Process arguments.')
parser.add_argument('--input_file', type=str,
                    default='/projects/ncdot/NC_2018_Secondary/active_learning/guardrail/round1/annot_data/user_annots.txt',
                    help='input file with path for user annotated images to create image data for active learning')
parser.add_argument('--cur_round', type=int, default=1,
                    help='the current round of active learning')
parser.add_argument('--train_frac', type=float, default='0.8',
                    help='fraction of training data over all data')
parser.add_argument('--feature_name', type=str, default='guardrail',
                    help='the name of the feature for the classifier, e.g., guardrail')
parser.add_argument('--input_prefix_dir', type=str,
                    default='/projects/ncdot/NC_2018_Secondary/images',
                    help='root directory to create active learning data in')
parser.add_argument('--root_dir', type=str,
                    default='/projects/ncdot/NC_2018_Secondary/active_learning',
                    help='root directory to create active learning data in')


args = parser.parse_args()
input_file = args.input_file
cur_round = args.cur_round
feature_name = args.feature_name
train_frac = args.train_frac
input_prefix_dir = args.input_prefix_dir
root_dir = args.root_dir
root_al_dir = os.path.join(root_dir, feature_name, f'round{cur_round}', 'data')
df = pd.read_csv(input_file, header=0, index_col=False, dtype=str, usecols=['Image', 'Presence'])
df.drop_duplicates(subset=['Image'])
print(df.shape)


def prepare_image(src, dst):
    dst_path = os.path.dirname(dst)
    os.makedirs(dst_path, exist_ok=True)
    os.symlink(src, dst)
    return


train_df, valid_df, test_df = split_to_train_valid_test_for_al(df, 'Presence', train_frac)
print('training data:', len(train_df), 'validation data:', len(valid_df), 'test data:', len(test_df))

train_path = f'{root_al_dir}/train/'
create_yes_no_sub_dirs(train_path)
train_df.apply(lambda row: prepare_image(os.path.join(input_prefix_dir, row['Image']),
                                         os.path.join(train_path, 'yes' if row['Presence'] == 'True' else 'no',
                                                      row['Image'])), axis=1)
valid_path = f'{root_al_dir}/validation/'
create_yes_no_sub_dirs(valid_path)
valid_df.apply(lambda row: prepare_image(os.path.join(input_prefix_dir, row['Image']),
                                         os.path.join(valid_path, 'yes' if row['Presence'] == 'True' else 'no',
                                                      row['Image'])), axis=1)
test_path = f'{root_al_dir}/test/'
create_yes_no_sub_dirs(test_path)
test_df.apply(lambda row: prepare_image(os.path.join(input_prefix_dir, row['Image']),
                                        os.path.join(test_path, 'yes' if row['Presence'] == 'True' else 'no',
                                                     row['Image'])), axis=1)
print('Done')
