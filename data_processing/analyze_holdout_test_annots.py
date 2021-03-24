import pandas as pd
import argparse


parser = argparse.ArgumentParser(description='Process arguments.')
parser.add_argument('--label_file', type=str,
                    default='../server/metadata/holdout_test/user_annoted_image_info_d13_d14.txt',
                    help='user annotated info file')
parser.add_argument('--balanced_label_file', type=str,
                    default='../server/metadata/holdout_test/user_annotated_balanced_image_info_d13_d14.csv',
                    help='user annotated info file that are picked as balanced 650 set')
parser.add_argument('--remain_images_file', type=str,
                    default='../server/metadata/remain_image_base_names.csv',
                    help='file that contains remaining image base names after AL annotation rounds')
parser.add_argument('--predict_file', type=str,
                    default='../server/metadata/model-related/secondary_road/round2/predict_d4.csv',
                    help='predicted data from model')
parser.add_argument('--compare_with_remain_images', type=bool,
                    default=True,
                    help='indicating whether to only compare with remain images or not')


args = parser.parse_args()
label_file = args.label_file
balanced_label_file = args.balanced_label_file
predict_file = args.predict_file
remain_images_file = args.remain_images_file
compare_with_remain_images = args.compare_with_remain_images


df_in = pd.read_csv(label_file, header=0, index_col=False, dtype={'Image': str, 'Presence': str},
                    usecols=['Image', 'Presence'])
df_in.drop_duplicates(subset=['Image'], inplace=True)
df_in['Image'] = df_in['Image'].str.split('/').str[-1]
if compare_with_remain_images:
    df_in['Image'] = df_in['Image'].str.replace('.jpg', '')
    df_in_balanced = pd.read_csv(balanced_label_file, header=0, index_col=False, dtype={'Image': str, 'Presence': str},
                                 usecols=['Image', 'Presence'])
    df_in_balanced['Image'] = df_in_balanced['Image'].str.split('/').str[-1]
    df_in_balanced['Image'] = df_in_balanced['Image'].str.replace('.jpg', '')
    df_in = df_in[~df_in['Image'].isin(df_in_balanced.Image)]
    df_remain_images = pd.read_csv(remain_images_file, header=0, index_col=False, dtype=str)
    df_in_remain = df_in[df_in['Image'].isin(df_remain_images.MAPPED_IMAGE)]
    print(df_in.shape, df_in_remain.shape, len(df_in)-len(df_in_remain))
else:
    df_model = pd.read_csv(predict_file, header=0, index_col=False,
                        dtype={'MAPPED_IMAGE': str, 'ROUND_PREDICT': float},
                        usecols=['MAPPED_IMAGE', 'ROUND_PREDICT'])
    df_model['MAPPED_IMAGE'] = df_model['MAPPED_IMAGE'].str.split('/').str[-1]
    df_model = df_model[df_model.MAPPED_IMAGE.isin(df_in.Image)]
    df_in = df_in.set_index('Image')
    df_model = df_model.set_index('MAPPED_IMAGE')
    print(df_in.shape)
    print(df_model.shape)
    df = pd.concat([df_in, df_model], axis=1)
    df = df.reset_index()
    print(df.shape)
    df_fns = df[(df['ROUND_PREDICT'] < 0.5) & (df['Presence']=='True')]
    df_fps = df[(df['ROUND_PREDICT'] >= 0.5) & (df['Presence']=='False')]
    print(df_fns.shape, df_fps.shape)

