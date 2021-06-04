import pandas as pd
import argparse
import os

from utils import split_to_train_valid_for_al, create_yes_no_sub_dirs, sym_link_single_view_image


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
                    default='/projects/ncdot/NC_2018_Secondary/',
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
parser.add_argument('--original_image_without_join', action='store_true', default=False,
                    help='if set, original image rather than joined images are prepared for AL')
parser.add_argument('--include_all_neg_in_joined_pos', action='store_true', default=False,
                    help='if set, negative single images are part of total negative images to randomly sample '
                         'for a balanced train/validation set')
parser.add_argument('--no_exist_train', action='store_true', default=False,
                    help='if set, no existing training data is added for AL')
parser.add_argument('--neg_fps_file', type=str,
                    default='/projects/ncdot/NC_2018_Secondary/active_learning/guardrail/round5/annot_data/'
                            'annot_fps_from_round4_model.csv',
                    help='the fps file that contains FPs images to be included in the negative samples')
parser.add_argument('--neg_fence_percent', type=float, default=-1,
                    help='percentage of fence in the negative set - only valid when it is between 0 and 1')

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
original_image_without_join = args.original_image_without_join
include_all_neg_in_joined_pos = args.include_all_neg_in_joined_pos
no_exist_train = args.no_exist_train
neg_fence_percent = args.neg_fence_percent
neg_fps_file = args.neg_fps_file


def read_annotation_df(df_file):
    annot_df = pd.read_csv(df_file, header=0, index_col=False, dtype=str,
                           usecols=['Image', 'Presence', 'LeftView', 'FrontView', 'RightView', 'Flags'])
    annot_df = annot_df.drop_duplicates(subset=['Image'])
    annot_df['Full_Path_Image'] = input_prefix_dir + annot_df.Image
    annot_df = annot_df.set_index('Image')
    return annot_df


df = read_annotation_df(input_file)

if prior_input_file:
    # combine prior_input_file and input_file to create output_annot_file which is used to prepare images
    df_prior = read_annotation_df(prior_input_file)
    df_all = pd.concat([df, df_prior])
    df_all.to_csv(all_annot_file)
    # concatenate prior user annotation data with current round annotation data
    df = df_all
root_al_dir = os.path.join(root_dir, feature_name, f'round{cur_round}', 'data')

if no_exist_train:
    # under-sample majority class to make a balanced training set
    if original_image_without_join:
        df_yes = df[(df.LeftView == 'p') | (df.LeftView == 'i') | (df.FrontView == 'p') |
                    (df.FrontView == 'i') | (df.RightView == 'p') | (df.RightView == 'i')]
        df_yes.Presence = 'True'
        df_yes_single_yes_cnt = len(df_yes[df_yes.LeftView == 'p']) + len(df_yes[df_yes.FrontView == 'p']) + \
            len(df_yes[df_yes.RightView == 'p']) + len(df_yes[df_yes.LeftView == 'i']) + \
            len(df_yes[df_yes.FrontView == 'i']) + len(df_yes[df_yes.RightView == 'i'])
        df_yes_single_no_cnt = len(df_yes[df_yes.LeftView == 'a']) + len(df_yes[df_yes.FrontView == 'a']) + \
            len(df_yes[df_yes.RightView == 'a'])
        if include_all_neg_in_joined_pos:
            if df_yes_single_yes_cnt > df_yes_single_no_cnt:
                df_yes_single_diff_cnt = df_yes_single_yes_cnt - df_yes_single_no_cnt

                df_no = df[(df.LeftView == 'a') & (df.FrontView == 'a') & (df.RightView == 'a')]
                df_no_joined_cnt = df_yes_single_diff_cnt // 3 + 1
                if neg_fps_file:
                    neg_fps = pd.read_csv(neg_fps_file, index_col=False, dtype=str)
                    df_no['MAPPED_IMAGE'] = df_no.index.str.split('/').str[-1].str.split('.').str[0]
                    df_no_fps = df_no[df_no.MAPPED_IMAGE.isin(neg_fps.MAPPED_IMAGE)]
                    df_no_other = df_no[~df_no.MAPPED_IMAGE.isin(neg_fps.MAPPED_IMAGE)]
                    df_no_other = df_no_other.sample(n=df_no_joined_cnt-len(df_no_fps), random_state=42)
                    df_no = pd.concat([df_no_fps, df_no_other])
                    print('df_no_fps: ', len(df_no_fps), ', df_no_other:', len(df_no_other), 'df_no:', len(df_no))
                elif 0 < neg_fence_percent < 1:
                    df_no_fence = df_no[df_no.Flags == 'Fence']
                    df_no_fence_cnt = len(df_no_fence)
                    fence_cnt = int(df_no_joined_cnt * neg_fence_percent)
                    if df_no_fence_cnt < fence_cnt:
                        fence_cnt = df_no_fence_cnt
                    else:
                        df_no_fence = df_no_fence.sample(n=fence_cnt, random_state=42)
                    df_no_other = df_no[df_no.Flags != 'Fence'].sample(n=df_no_joined_cnt-fence_cnt, random_state=42)
                    df_no = pd.concat([df_no_fence, df_no_other])
                else:
                    df_no = df_no.sample(n=df_no_joined_cnt, random_state=42)
                df_no.Presence = 'False'
        else:
            # put negative images from the positive joined images into the total negative image sample pool
            df_yes_no = df_yes[(df_yes.LeftView == 'a') | (df_yes.FrontView == 'a') | (df_yes.RightView == 'a')]
            df_yes_no.Presence = 'False'
            # half sample from df_yes_no and the other half sample from df_no
            sample_cnt = df_yes_single_yes_cnt // 2
            no_ratio = df_yes_single_no_cnt / (df_yes_single_yes_cnt + df_yes_single_no_cnt)
            df_yes_no = df_yes_no.sample(n=int(sample_cnt * no_ratio) + 1, random_state=42)
            df_no = df[(df.LeftView == 'a') & (df.FrontView == 'a') & (df.RightView == 'a')]
            df_no.Presence = 'False'
            df_no = df_no.sample(n=sample_cnt // 3 + 1, random_state=42)
            df_no = pd.concat([df_yes_no, df_no])
    else:
        df_yes = df[df.Presence == 'True']
        df_no = df[(df.Presence == 'False') & (df.LeftView != 'i') & (df.FrontView != 'i') & (df.RightView != 'i')]
        df_yes_cnt = len(df_yes)
        df_no = df_no.sample(n=df_yes_cnt, random_state=42)

    if not include_all_neg_in_joined_pos:
        # have to reset index since negative single images from the joined positive images could have the same
        # image names as the positive single images, which would be lost without reset_index call
        df.reset_index(inplace=True)

    if include_all_neg_in_joined_pos and df_yes_single_yes_cnt <= df_yes_single_no_cnt:
        df = df_yes
    else:
        df = pd.concat([df_yes, df_no])

    train_df_user, valid_df_user = split_to_train_valid_for_al(df, 'Presence', train_frac)
    train_df = train_df_user
    valid_df = valid_df_user
else:
    train_df_user, valid_df_user = split_to_train_valid_for_al(df, 'Presence', train_frac)
    train_df_user.drop(columns=['Full_Path_Image']).to_csv(output_annot_train_file)

if not no_exist_train:
    df_yes_cnt = len(df[df.Presence == 'True'])
    df_no_cnt = len(df[df.Presence == 'False'])
    print(df.shape, df_yes_cnt, df_no_cnt)
    exist_train_yes_df = pd.read_csv(exist_train_yes_file, header=None, index_col=False, dtype=str,
                                     names=['Full_Path_Image'])
    exist_train_yes_df['Presence'] = 'True'
    exist_train_yes_df['Image'] = exist_train_yes_df.Full_Path_Image.str.replace('/projects/ncdot/2018/machine_learning'
                                                                                 '/data_2lanes/train/', '')
    exist_train_yes_df = exist_train_yes_df.set_index('Image')

    exist_train_no_df = pd.read_csv(exist_train_no_file, header=None, index_col=False, dtype=str,
                                    names=['Full_Path_Image'])
    exist_train_no_df['Presence'] = 'False'
    exist_train_no_df['Image'] = exist_train_no_df.Full_Path_Image.str.replace('/projects/ncdot/2018/machine_learning/'
                                                                               'data_2lanes/train/', '')
    exist_train_no_df = exist_train_no_df.set_index('Image')
    # use negative training set as the basis to add exist_train_percent to the negative set
    exist_train_cnt = len(exist_train_no_df)
    exist_train_cnt_to_add = (int)(exist_train_cnt * exist_train_percent)
    df_total_cnt = df_no_cnt + exist_train_cnt_to_add
    exist_train_yes_cnt_to_add = df_total_cnt - df_yes_cnt
    exist_train_no_cnt_to_add = df_total_cnt - df_no_cnt

    exist_train_yes_df_to_add = exist_train_yes_df.sample(n=exist_train_yes_cnt_to_add, random_state=42)
    train_exist_df_yes, valid_exist_df_yes = split_to_train_valid_for_al(exist_train_yes_df_to_add, 'Presence',
                                                                         train_frac)

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


def prepare_image(src, dst, left, front, right, presence, prepare_opposite=True):
    dst_path = os.path.dirname(dst)
    os.makedirs(dst_path, exist_ok=True)
    if original_image_without_join and src.startswith(input_prefix_dir):
        sym_link_single_view_image(src, dst, left, front, right, presence, irelevant_as_false=False,
                                   prepare_opposite=prepare_opposite)
    else:
        os.symlink(src, dst)
    return


train_path = f'{root_al_dir}/train/'
create_yes_no_sub_dirs(train_path)
train_df.apply(lambda row: prepare_image(row['Full_Path_Image'],
                                         os.path.join(train_path, 'yes' if row['Presence'] == 'True' else 'no',
                                                      row['Image']),
                                         row['LeftView'], row['FrontView'], row['RightView'], row['Presence'],
                                         prepare_opposite=True if include_all_neg_in_joined_pos else False), axis=1)
valid_path = f'{root_al_dir}/validation/'
create_yes_no_sub_dirs(valid_path)
valid_df.apply(lambda row: prepare_image(row['Full_Path_Image'],
                                         os.path.join(valid_path, 'yes' if row['Presence'] == 'True' else 'no',
                                                      row['Image']),
                                         row['LeftView'], row['FrontView'], row['RightView'], row['Presence'],
                                         prepare_opposite=True if include_all_neg_in_joined_pos else False), axis=1)
print('Done')
