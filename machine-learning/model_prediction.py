import time
import argparse
import os
from PIL import Image
import pandas as pd
import numpy as np
import tensorflow as tf


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

# load the model
model = tf.keras.models.load_model(model_file)
print(model.summary())

output_df = pd.DataFrame(columns=['Image', 'Probability'])


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
    path = os.path.join(data_dir, set_str, minute_str)
    left_image_name = '{}5.jpg'.format(mapped_image)
    front_image_name = '{}1.jpg'.format(mapped_image)
    right_image_name = '{}2.jpg'.format(mapped_image)
    return path, left_image_name, front_image_name, right_image_name


def predict(image_base_name):
    path, left, front, right = get_image_names_with_path(image_base_name)
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
        img = dst.resize((299, 299), Image.ANTIALIAS)
        img = tf.keras.preprocessing.image.img_to_array(img)
        img = tf.keras.applications.xception.preprocess_input(img)
        predictions = model.predict(np.array([img]))
        output_df.append({'Image': image_base_name, 'Probability': predictions[0][0]}, ignore_index=True)
    except OSError as ex:
        print(image_base_name, str(ex))
        return


# there are 2 GPUs with 32GB mem each on groucho. Need to set memory limit to 30G for each to avoid
# running exceptions
tf.config.experimental.set_memory_growth = True
gpus = tf.config.experimental.list_physical_devices('GPU')
if len(gpus) == 2:
  try:
    tf.config.experimental.set_virtual_device_configuration(
        gpus[0],
        [tf.config.experimental.VirtualDeviceConfiguration(memory_limit=1024*30)])
    tf.config.experimental.set_virtual_device_configuration(
        gpus[1],
        [tf.config.experimental.VirtualDeviceConfiguration(memory_limit=1024*30)])
    logical_gpus = tf.config.experimental.list_logical_devices('GPU')
    print(len(gpus), "Physical GPU,", len(logical_gpus), "Logical GPUs")
  except RuntimeError as e:
    # Virtual devices must be set before GPUs have been initialized
    print(e)

# read all image base names
if is_subset:
    df = pd.read_csv(image_base_names_file, header=0, index_col=False, nrows=18240,
                     usecols=["MAPPED_IMAGE"])
else:
    df = pd.read_csv(image_base_names_file, header=0, index_col=False, usecols=["MAPPED_IMAGE"])

ts = time.time()
strategy = tf.distribute.MirroredStrategy()
with strategy.scope():
    df.apply(lambda row: predict(row['MAPPED_IMAGE']), axis=1)
output_df.to_csv(output_file, index=False)

te = time.time()
print('time taken for model prediction:', te-ts)
