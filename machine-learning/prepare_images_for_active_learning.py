import pandas as pd
import argparse
import os

from utils import split_to_train_valid_for_al, create_yes_no_sub_dirs


parser = argparse.ArgumentParser(description='Process arguments.')
parser.add_argument('--input_file', type=str,
                    default='/projects/ncdot/NC_2018_Secondary/active_learning/guardrail/round4/annot_data/user_annots.txt',
                    help='input file with path for current user annotated images to create image data for active learning')
parser.add_argument('--prior_input_file', type=str,
                    default='/projects/ncdot/NC_2018_Secondary/active_learning/guardrail/round3/annot_data/all_user_annots.txt',
                    help='input file with path for previous user annotated images to create image data for active learning')
parser.add_argument('--all_annot_file', type=str,
                    default='/projects/ncdot/NC_2018_Secondary/active_learning/guardrail/round4/annot_data/all_user_annots.txt',
                    help='the combined user annotated file that contain all user annotated images so far')
parser.add_argument('--cur_round', type=int, default=4,
                    help='the current round of active learning')
parser.add_argument('--train_frac', type=float, default=0.8,
                    help='fraction of training data over all data')
parser.add_argument('--feature_name', type=str, default='guardrail',
                    help='the name of the feature for the classifier, e.g., guardrail')
parser.add_argument('--input_prefix_dir', type=str,
                    default='/projects/ncdot/NC_2018_Secondary/images/',
                    help='root directory to create active learning data in - make sure it ends with slash')
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
parser.add_argument('--exist_train_percent', type=float, default=0.06,
                    help='existing train percentage to add to the AL round annotation data for the larger class count')
parser.add_argument('--output_annot_train_file', type=str,
                    default='/projects/ncdot/NC_2018_Secondary/active_learning/guardrail/round4/'
                            'annot_data/all_user_annots_train.csv',
                    help='annotated data used for AL training which is used for computing centroid of training data')
parser.add_argument('--cur_round_annot_only', action='store_true', default=False,
                    help='if set, only current round annotation is used while prior round annotations are treated as '
                         'existing training data; if false, all previous round annotations up to the current round are '
                         'used as training data')

args = parser.parse_args()
input_file = args.input_file
prior_input_file = args.prior_input_file
all_annot_file = args.all_annot_file
cur_round = args.cur_round
feature_name = args.feature_name
train_frac = args.train_frac
input_prefix_dir = args.input_prefix_dir
root_dir = args.root_dir
exist_train_yes_file = args.exist_train_yes_file
exist_train_no_file = args.exist_train_no_file
exist_train_percent = args.exist_train_percent
output_annot_train_file = args.output_annot_train_file
cur_round_annot_only = args.cur_round_annot_only

df = pd.read_csv(input_file, header=0, index_col=False, dtype=str, usecols=['Image', 'Presence'])
df = df.drop_duplicates(subset=['Image'])
df['Full_Path_Image'] = input_prefix_dir + df.Image
df = df.set_index('Image')

exist_train_yes_df = pd.read_csv(exist_train_yes_file, header=None, index_col=False, dtype=str,
                                 names=['Full_Path_Image'])
exist_train_yes_df['Presence'] = 'True'
exist_train_yes_df['Image'] = exist_train_yes_df.Full_Path_Image.str.split('/').str[-1]
exist_train_yes_df = exist_train_yes_df.set_index('Image')

exist_train_no_df = pd.read_csv(exist_train_no_file, header=None, index_col=False, dtype=str,
                                names=['Full_Path_Image'])
exist_train_no_df['Presence'] = 'False'
exist_train_no_df['Image'] = exist_train_no_df.Full_Path_Image.str.split('/').str[-1]
exist_train_no_df = exist_train_no_df.set_index('Image')
if prior_input_file:
    # combine prior_input_file and input_file to create output_annot_file which is used to prepare images
    df_prior = pd.read_csv(prior_input_file, header=0, index_col=False, dtype=str, usecols=['Image', 'Presence'])
    df_prior = df_prior.drop_duplicates(subset=['Image'])
    df_prior['Full_Path_Image'] = input_prefix_dir + df_prior.Image
    df_prior = df_prior.set_index('Image')
    df_all = pd.concat([df, df_prior])
    df_all.to_csv(all_annot_file)
    if cur_round_annot_only:
        exist_train_yes_df = pd.concat([exist_train_yes_df, df_prior[df_prior.Presence=='True']])
        exist_train_no_df = pd.concat([exist_train_no_df, df_prior[df_prior.Presence=='False']])
    else:
        # concatenate prior user annotation data with current round annotation data
        df = df_all
root_al_dir = os.path.join(root_dir, feature_name, f'round{cur_round}', 'data')

df_yes_cnt = len(df[df.Presence == 'True'])
df_no_cnt = len(df[df.Presence == 'False'])
print(df.shape, df_yes_cnt, df_no_cnt)

# use negative training set as the basis to add exist_train_percent to the negative set
exist_train_cnt = len(exist_train_no_df)
exist_train_cnt_to_add = (int)(exist_train_cnt * exist_train_percent)
df_total_cnt = df_no_cnt + exist_train_cnt_to_add
exist_train_yes_cnt_to_add = df_total_cnt - df_yes_cnt
exist_train_no_cnt_to_add = df_total_cnt - df_no_cnt

exist_train_yes_df_to_add = exist_train_yes_df.sample(n=exist_train_yes_cnt_to_add, random_state=42)
train_df_user, valid_df_user = split_to_train_valid_for_al(df, 'Presence', train_frac)
train_df_user.drop(columns=['Full_Path_Image']).to_csv(output_annot_train_file)
train_exist_df_yes, valid_exist_df_yes = split_to_train_valid_for_al(exist_train_yes_df_to_add, 'Presence', train_frac)
if exist_train_no_cnt_to_add > 0:
    exist_train_no_df_to_add = exist_train_no_df.sample(n=exist_train_no_cnt_to_add, random_state=42)
    train_exist_df_no, valid_exist_df_no = split_to_train_valid_for_al(exist_train_no_df_to_add, 'Presence', train_frac)
    train_df = pd.concat([train_df_user, train_exist_df_yes, train_exist_df_no])
    valid_df = pd.concat([valid_df_user, valid_exist_df_yes, valid_exist_df_no])
else:
    train_df = pd.concat([train_df_user, train_exist_df_yes])
    valid_df = pd.concat([valid_df_user, valid_exist_df_yes])

train_df = train_df.reset_index()
valid_df = valid_df.reset_index()


def prepare_image(src, dst):
    dst_path = os.path.dirname(dst)
    os.makedirs(dst_path, exist_ok=True)
    os.symlink(src, dst)
    return


train_path = f'{root_al_dir}/train/'
create_yes_no_sub_dirs(train_path)
train_df.apply(lambda row: prepare_image(row['Full_Path_Image'],
                                         os.path.join(train_path, 'yes' if row['Presence'] == 'True' else 'no',
                                                      row['Image'])), axis=1)
valid_path = f'{root_al_dir}/validation/'
create_yes_no_sub_dirs(valid_path)
valid_df.apply(lambda row: prepare_image(row['Full_Path_Image'],
                                         os.path.join(valid_path, 'yes' if row['Presence'] == 'True' else 'no',
                                                      row['Image'])), axis=1)
print('Done')
