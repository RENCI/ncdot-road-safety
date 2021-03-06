import pandas as pd
import argparse
import os

from utils import split_to_train_valid_for_al, create_yes_no_sub_dirs


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
                    default='/projects/ncdot/NC_2018_Secondary/images/',
                    help='root directory to create active learning data in - make sure it ends with the slash')
parser.add_argument('--root_dir', type=str,
                    default='/projects/ncdot/NC_2018_Secondary/active_learning',
                    help='root directory to create active learning data in')
parser.add_argument('--exist_train_yes_file', type=str,
                    default='/projects/ncdot/NC_2018_Secondary/active_learning/guardrail/round0/'
                            'data_info/train_guardrail_yes_2lane.csv',
                    help='existing train positive data to select to add to the AL')
parser.add_argument('--exist_train_no_file', type=str,
                    default='/projects/ncdot/NC_2018_Secondary/active_learning/guardrail/round0/'
                            'data_info/train_guardrail_no_2lane.csv',
                    help='existing train negative data to select to add to the AL')
parser.add_argument('--exist_train_percent', type=float, default=0.01,
                    help='existing train percentage to add to the AL round annotation data for the larger class count')

args = parser.parse_args()
input_file = args.input_file
cur_round = args.cur_round
feature_name = args.feature_name
train_frac = args.train_frac
input_prefix_dir = args.input_prefix_dir
root_dir = args.root_dir
exist_train_yes_file = args.exist_train_yes_file
exist_train_no_file = args.exist_train_no_file
exist_train_percent = args.exist_train_percent

root_al_dir = os.path.join(root_dir, feature_name, f'round{cur_round}', 'data')
df = pd.read_csv(input_file, header=0, index_col=False, dtype=str, usecols=['Image', 'Presence'])
df = df.drop_duplicates(subset=['Image'])
df.Image = input_prefix_dir + df.Image
print(df.shape)
df_yes_cnt = len(df[df.Presence == 'True'])
df_no_cnt = len(df[df.Presence == 'False'])

exist_train_yes_df = pd.read_csv(exist_train_yes_file, header=None, index_col=False, dtype = str, names=['Image'])
exist_train_yes_df['Presence'] = 'True'
exist_train_no_df = pd.read_csv(exist_train_no_file, header=None, index_col=False, dtype = str, names=['Image'])
exist_train_no_df['Presence'] = 'False'
# train data is balanced, so it suffices to get count from either class
exist_train_cnt = len(exist_train_no_df)
exist_train_cnt_to_add = (int)(exist_train_cnt * exist_train_percent)
df_total_cnt = df_yes_cnt + exist_train_cnt_to_add if df_yes_cnt > df_no_cnt else df_no_cnt + exist_train_cnt_to_add
exist_train_yes_cnt_to_add = df_total_cnt - df_yes_cnt
exist_train_no_cnt_to_add = df_total_cnt - df_no_cnt
exist_train_yes_df_to_add = exist_train_yes_df.sample(n=exist_train_yes_cnt_to_add, random_state=42)
exist_train_no_df_to_add = exist_train_no_df.sample(n=exist_train_no_cnt_to_add, random_state=42)
df = df.set_index('Image')
exist_train_yes_df_to_add = exist_train_yes_df_to_add.set_index('Image')
exist_train_no_df_to_add = exist_train_no_df_to_add.set_index('Image')
df_all = pd.concat([df, exist_train_yes_df_to_add, exist_train_no_df_to_add])


def prepare_image(src, dst):
    dst_path = os.path.dirname(dst)
    os.makedirs(dst_path, exist_ok=True)
    os.symlink(src, dst)
    return


train_df, valid_df = split_to_train_valid_for_al(df_all, 'Presence', train_frac)
print('training data:', len(train_df), 'validation data:', len(valid_df))

train_path = f'{root_al_dir}/train/'
create_yes_no_sub_dirs(train_path)
train_df.apply(lambda row: prepare_image(row['Image'],
                                         os.path.join(train_path, 'yes' if row['Presence'] == 'True' else 'no',
                                                      row['Image'])), axis=1)
valid_path = f'{root_al_dir}/validation/'
create_yes_no_sub_dirs(valid_path)
valid_df.apply(lambda row: prepare_image(row['Image'],
                                         os.path.join(valid_path, 'yes' if row['Presence'] == 'True' else 'no',
                                                      row['Image'])), axis=1)
print('Done')
