import argparse
import os
import pandas as pd


parser = argparse.ArgumentParser(description='Process arguments.')
parser.add_argument('--input_metadata_path', type=str, default='../server/metadata/training_image_guardrail_yn_2lanes.csv',
                    help='input metadata file with path for preparing training data')
parser.add_argument('--input_data_path', type=str, default='/projects/ncdot/2018/machine_learning/data',
                    help='input training image data path for preparing 2-lanes only training data')
parser.add_argument('--input_path_file', type=str, default='/projects/ncdot/2018/NC_2018_Images/metadata/guardrail_image_path.txt',
                    help='input training image data path file for getting source guardrail training data path')
parser.add_argument('--feature_name', type=str, default='guardrail',
                    help='the name of the feature for the classifier, e.g., guardrail')
parser.add_argument('--output_path', type=str, default='/projects/ncdot/2018/machine_learning/data_2lanes',
                    help='Output path for storing training, test, and validation data for machine learning')
parser.add_argument('--train_frac', type=float, default='0.90',
                    help='fraction of training data over all data')

args = parser.parse_args()

input_metadata_path = args.input_metadata_path
input_data_path = args.input_data_path
output_path = args.output_path
feature_name = args.feature_name
train_frac = args.train_frac
input_path_file = args.input_path_file


def split_to_train_valid_test(data_df, label_column):
    labels = data_df[label_column].unique()
    split_train_df, split_valid_df, split_test_df = pd.DataFrame(), pd.DataFrame(), pd.DataFrame()
    for lbl in labels:
        lbl_df = data_df[data_df[label_column] == lbl]
        lbl_train_df = lbl_df.sample(frac=train_frac, random_state=1)
        lbl_valid_test_df = lbl_df.drop(lbl_train_df.index)
        # further split remaining data into two equal sets for validation and test
        lbl_valid_df = lbl_valid_test_df.sample(frac=0.5, random_state=1)
        lbl_test_df = lbl_valid_test_df.drop(lbl_valid_df.index)
        print(lbl, "total:", len(lbl_df), "train_df:", len(lbl_train_df), "valid_df", len(lbl_valid_df),
              "test_df:", len(lbl_test_df))
        split_train_df = split_train_df.append(lbl_train_df)
        split_valid_df = split_valid_df.append(lbl_valid_df)
        split_test_df = split_test_df.append(lbl_test_df)

    return split_train_df, split_valid_df, split_test_df


def prepare_image(mapped_image, label, data_type_subdir):
    df = pd.read_csv(input_path_file, header=None)
    df = df[df[0].str.endswith(f'{mapped_image}.jpg')]
    if df.shape != (1, 1):
        print(mapped_image, "cannot be found in the guardrail_image_path.txt", label, data_type_subdir)
        return
    image_path_list = list(df[0])
    image_path_src = image_path_list[0]
    feature_dir = '{}_{}'.format(feature_name, 'yes' if label == 'Y' else 'no')
    dst_path = os.path.join(output_path, data_type_subdir, feature_dir, mapped_image[:3])
    os.makedirs(dst_path, exist_ok=True)
    dst_path_image = os.path.join(dst_path, '{}.jpg'.format(mapped_image))
    os.symlink(image_path_src, dst_path_image)


df = pd.read_csv(input_metadata_path, header=0, index_col=False, usecols=['MAPPED_IMAGE', 'GUARDRAIL_YN'], dtype=str)
train_df, valid_df, test_df = split_to_train_valid_test(df, 'GUARDRAIL_YN')
print('training data:', len(train_df), 'validation data:', len(valid_df), 'test data:', len(test_df))
train_df.apply(lambda row: prepare_image(row['MAPPED_IMAGE'], row['GUARDRAIL_YN'], 'train'), axis=1)
valid_df.apply(lambda row: prepare_image(row['MAPPED_IMAGE'], row['GUARDRAIL_YN'], 'validation'), axis=1)
test_df.apply(lambda row: prepare_image(row['MAPPED_IMAGE'], row['GUARDRAIL_YN'], 'test'), axis=1)
print('Done')
