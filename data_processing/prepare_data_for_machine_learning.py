import argparse
import os
import pandas as pd
from PIL import Image


parser = argparse.ArgumentParser(description='Process arguments.')
parser.add_argument('--input_metadata_path', type=str, default='../server/metadata/training_image_set_1370774.csv',
                    help='input metadata file with path for preparing training data')
parser.add_argument('--input_data_path', type=str, default='/projects/ncdot/2018/NC_2018_Images',
                    help='input image data path for preparing training data')
parser.add_argument('--feature_name', type=str, default='guardrail',
                    help='the name of the feature for the classifier, e.g., guardrail')
parser.add_argument('--output_path', type=str, default='/projects/ncdot/2018/machine_learning/data',
                    help='Output path for storing training, test, and validation data for machine learning')
parser.add_argument('--train_frac', type=float, default='0.98',
                    help='fraction of training data over all data')

args = parser.parse_args()

input_metadata_path = args.input_metadata_path
input_data_path = args.input_data_path
output_path = args.output_path
feature_name = args.feature_name
train_frac = args.train_frac


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


def get_image_names_with_path(mapped_image):
    if len(mapped_image) != 11:
        print("mapped image in metadata must have a length of 11")
        return '', '', '', ''
    set_str = mapped_image[:3]
    hour = mapped_image[3:5]
    minute = mapped_image[5:7]
    if hour not in ['00', '01', '02']:
        print("hour in the mapped image must be 00 or 01 or 02", mapped_image)
        return '', '', '', ''
    if int(minute) > 59:
        print("minute in the mapped image must be less than 60")
        return '', '', '', ''
    if hour == '00':
        # strip prefix 0 from minute if any
        minute_str = str(int(minute))
    else:  # hour == '01'
        minute_str = str(int(minute) + int(hour)*60)
    path = os.path.join(input_data_path, set_str, minute_str)
    left_image_name = '{}5.jpg'.format(mapped_image)
    front_image_name = '{}1.jpg'.format(mapped_image)
    right_image_name = '{}2.jpg'.format(mapped_image)
    return path, left_image_name, front_image_name, right_image_name


def prepare_image(mapped_image, label, data_type_subdir):
    path, left, front, right = get_image_names_with_path(mapped_image)
    if not path or not left or not front or not right:
        return

    left_image = os.path.join(path, left)
    front_image = os.path.join(path, front)
    right_image = os.path.join(path, right)
    if not os.path.exists(left_image) or not os.path.exists(front_image) or not os.path.exists(right_image):
        print("at least one of the images", left_image, front_image, right_image, "do not exist")
        return
    img_names = [left_image, front_image, right_image]
    imgs = []
    try:
        for idx in range(3):
            imgs.append(Image.open(img_names[idx]))

        dst = Image.new('RGB', (imgs[0].width+imgs[1].width+imgs[2].width, imgs[0].height))

        dst.paste(imgs[0], (0, 0))
        dst.paste(imgs[1], (imgs[0].width, 0))
        dst.paste(imgs[2], (imgs[0].width+imgs[1].width, 0))
    except OSError as ex:
        print(str(ex))
        return
    feature_dir = '{}_{}'.format(feature_name, 'yes' if label == 'Y' else 'no')
    dst_path = os.path.join(output_path, data_type_subdir, feature_dir, mapped_image[:3])
    os.makedirs(dst_path, exist_ok=True)
    dst_path_image = os.path.join(dst_path, '{}.jpg'.format(mapped_image))
    dst.save(dst_path_image)


df = pd.read_csv(input_metadata_path, header=0, index_col=False, usecols=['MAPPED_IMAGE', 'GUARDRAIL_YN'], dtype=str)
train_df, valid_df, test_df = split_to_train_valid_test(df, 'GUARDRAIL_YN')
print('training data:', len(train_df), 'validation data:', len(valid_df), 'test data:', len(test_df))
train_df.apply(lambda row: prepare_image(row['MAPPED_IMAGE'], row['GUARDRAIL_YN'], 'train'), axis=1)
valid_df.apply(lambda row: prepare_image(row['MAPPED_IMAGE'], row['GUARDRAIL_YN'], 'validation'), axis=1)
test_df.apply(lambda row: prepare_image(row['MAPPED_IMAGE'], row['GUARDRAIL_YN'], 'test'), axis=1)
print('Done')
