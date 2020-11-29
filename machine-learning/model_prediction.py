import time
import argparse
import os
from PIL import Image
import pandas as pd
import numpy as np
import tensorflow as tf
from utils import setup_gpu_memory, get_image_names_with_path, join_images


parser = argparse.ArgumentParser(description='Process arguments.')
parser.add_argument('--data_dir', type=str, default='/projects/ncdot/2018/NC_2018_Images',
                    help='input dir of the videolog data to apply model prediction for')
parser.add_argument('--model_file', type=str,
                    default='/projects/ncdot/2018/machine_learning/model/guardrail_xception_subset.h5',
                    help='model file with path to be load for prediction')
parser.add_argument('--output_file', type=str,
                    default='/projects/ncdot/2018/machine_learning/output/guardrail_classification.csv',
                    help='prediction output csv file')
parser.add_argument('--image_base_names_file', type=str,
                    default='/projects/ncdot/2018/NC_2018_Images/metadata/sensor_data_mapped_unique_3584576.csv',
                    help='file that contains image base names of images in data_dir')
parser.add_argument('--image_base_name_length', type=int,
                    default='11',
                    help='the length of the image base name string')
parser.add_argument('--is_subset', action='store_true', default=False,
                    help='make predictions on subset data for development db ingestion')

args = parser.parse_args()
data_dir = args.data_dir
model_file = args.model_file
output_file = args.output_file
image_base_names_file = args.image_base_names_file
image_base_name_length = args.image_base_name_length
is_subset = args.is_subset

setup_gpu_memory()

# load the model
model = tf.keras.models.load_model(model_file)
print(model.summary())


def predict(image_base_name):
    path, left, front, right = get_image_names_with_path(data_dir, image_base_name)
    if not path or not left or not front or not right:
        return

    left_image = os.path.join(path, left)
    front_image = os.path.join(path, front)
    right_image = os.path.join(path, right)
    dst_img = join_images(left_image, front_image, right_image)
    if dst_img:
        img = dst_img.resize((299, 299), Image.ANTIALIAS)
        img = tf.keras.preprocessing.image.img_to_array(img)
        img = tf.keras.applications.xception.preprocess_input(img)
        predictions = model.predict(np.array([img]))
        return predictions[0][0]
    else:
        return np.nan

# read all image base names
if is_subset:
    df = pd.read_csv(image_base_names_file, dtype=str, header=0, index_col=False, nrows=18240,
                     usecols=["MAPPED_IMAGE"])
else:
    df = pd.read_csv(image_base_names_file, dtype=str, header=0, index_col=False, usecols=["MAPPED_IMAGE"])

ts = time.time()
strategy = tf.distribute.MirroredStrategy()
with strategy.scope():
    df['Probability'] = df.apply(lambda row: predict(row['MAPPED_IMAGE']), axis=1)

df.to_csv(output_file, index=False)

te = time.time()
print('time taken for model prediction:', te-ts)
