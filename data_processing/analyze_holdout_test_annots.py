import pandas as pd
import argparse


parser = argparse.ArgumentParser(description='Process arguments.')
parser.add_argument('--label_file', type=str,
                    default='../server/metadata/holdout_test/user_annoted_image_info_d4.txt',
                    help='user annotated info file')
parser.add_argument('--balanced_label_file', type=str,
                    default='../server/metadata/holdout_test/user_annotated_balanced_image_info_d4.txt',
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
parser.add_argument('--output_file', type=str,
                    default='../server/metadata/holdout_test/user_annoted_image_info_for_holdout_d4.txt',
                    help='output file that contains images to be used as holdout test set')


args = parser.parse_args()
label_file = args.label_file
balanced_label_file = args.balanced_label_file
predict_file = args.predict_file
remain_images_file = args.remain_images_file
compare_with_remain_images = args.compare_with_remain_images
output_file = args.output_file


df_in = pd.read_csv(label_file, header=0, index_col=False, dtype={'Image': str, 'Presence': str},
                    usecols=['Image', 'Presence'])
df_in.drop_duplicates(subset=['Image'], inplace=True)
df_in['BaseImageName'] = df_in['Image'].str.split('/').str[-1]
if compare_with_remain_images:
    df_in['BaseImageName'] = df_in['BaseImageName'].str.replace('.jpg', '')
    df_in_balanced = pd.read_csv(balanced_label_file, header=0, index_col=False, dtype={'Image': str, 'Presence': str},
                                 usecols=['Image', 'Presence'])
    df_in_balanced['BaseImageName'] = df_in_balanced['Image'].str.split('/').str[-1]
    df_in_balanced['BaseImageName'] = df_in_balanced['BaseImageName'].str.replace('.jpg', '')
    df_remain_images = pd.read_csv(remain_images_file, header=0, index_col=False, dtype=str)
    df_in_remain = df_in[df_in['BaseImageName'].isin(df_remain_images.MAPPED_IMAGE)]
    df_concat = pd.concat([df_in_balanced, df_in_remain])
    print(df_in_balanced.shape, df_in_remain.shape, df_concat.shape)
    df_concat = df_concat.drop(columns=['BaseImageName'])
    df_concat.to_csv(output_file, index=False)
else:
    df_model = pd.read_csv(predict_file, header=0, index_col=False,
                        dtype={'MAPPED_IMAGE': str, 'ROUND_PREDICT': float},
                        usecols=['MAPPED_IMAGE', 'ROUND_PREDICT'])
    df_model['MAPPED_IMAGE'] = df_model['MAPPED_IMAGE'].str.split('/').str[-1]
    df_model = df_model[df_model.MAPPED_IMAGE.isin(df_in.BaseImageName)]
    df_in = df_in.drop(columns=['Image'])
    df_in = df_in.set_index('BaseImageName')
    df_model = df_model.set_index('MAPPED_IMAGE')
    print(df_in.shape)
    print(df_model.shape)
    df = pd.concat([df_in, df_model], axis=1)
    df = df.reset_index()
    print(df.shape)
    df_fns = df[(df['ROUND_PREDICT'] < 0.5) & (df['Presence']=='True')]
    df_fps = df[(df['ROUND_PREDICT'] >= 0.5) & (df['Presence']=='False')]
    print(df_fns.shape, df_fps.shape)

