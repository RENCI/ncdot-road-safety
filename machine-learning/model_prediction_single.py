import os
import time
import argparse
import pandas as pd
from PIL import Image
import numpy as np
import tensorflow as tf
from utils import setup_gpu_memory


parser = argparse.ArgumentParser(description='Process arguments.')
parser.add_argument('--data_dir', type=str,
                    default='/projects/ncdot/NC_2018_Secondary/single_images_missing/d01',
                    help='input dir of data to apply model prediction for')
parser.add_argument('--model_file', type=str,
                    # default='/projects/ncdot/NC_2018_Secondary/active_learning/pole/round4/model/pole_round4.h5',
                    default='/projects/ncdot/NC_2018_Secondary/active_learning/guardrail/round5/model/'
                            'guardrail_round5.h5',
                    help='model file with path to be load for prediction')
parser.add_argument('--output_file', type=str,
                    default='/projects/ncdot/secondary_road/predict/guardrail/predict_d01_single_missing.csv',
                    help='prediction output csv file')
parser.add_argument('--batch_size', type=int, default=512,
                    help='prediction batch size')


args = parser.parse_args()
data_dir = args.data_dir
model_file = args.model_file
output_file = args.output_file
batch_size = args.batch_size

setup_gpu_memory()

strategy = tf.distribute.MirroredStrategy()
with strategy.scope():
    # load the model for prediction only, no need to compile the model
    model = tf.keras.models.load_model(model_file, compile=False)
print(model.summary())

file_name_list = []
prob_list = []
ts = time.time()
for dir_name, subdir_list, file_list in os.walk(data_dir, followlinks=True):
    for file_name in file_list:
        if file_name.lower().endswith(('.jpg')):
            try:
                full_file_name = os.path.join(dir_name, file_name)
                img = Image.open(full_file_name)
                img = img.resize((299, 299), Image.ANTIALIAS)
                img = tf.keras.preprocessing.image.img_to_array(img)
                img = tf.keras.applications.xception.preprocess_input(img)
                predictions = model.predict(np.array([img]))
                prob_list.append(round(predictions[0][0], 2))
                file_name_list.append(full_file_name)
            except Exception as ex:
                print(full_file_name)
                continue
te = time.time()
print('Total time taken for prediction: ', te-ts)

df = pd.DataFrame({"MAPPED_IMAGE": file_name_list, "ROUND_PREDICT": prob_list})
df.MAPPED_IMAGE = df.MAPPED_IMAGE.str.replace('/projects/ncdot/NC_2018_Secondary/single_images_missing/', '')
df.to_csv(output_file, index=False)
print('Done')
