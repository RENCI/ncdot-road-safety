import time
import os
import gc
import argparse
import pandas as pd
import numpy as np
import tensorflow as tf
from image_dataset import image_dataset_from_directory
from utils import setup_gpu_memory


parser = argparse.ArgumentParser(description='Process arguments.')
parser.add_argument('--data_dir', type=str,
                    default='/projects/ncdot/NC_2018_Secondary/images/d13',
                    help='input dir of data to apply model prediction for')
parser.add_argument('--model_file', type=str,
                    default='/projects/ncdot/2018/machine_learning/model/guardrail_xception_feature_extraction_model.h5',
                    help='model file with path to be load for feature extraction')
parser.add_argument('--output_file', type=str,
                    default='/projects/ncdot/NC_2018_Secondary/image_features/d13_image_features.csv',
                    help='prediction output csv file')
parser.add_argument('--batch_size', type=int, default=512,
                    help='prediction batch size')
parser.add_argument('--is_one_division', type=bool, default=True,
                    help='whether to predict for one division or for all divisions under the data_dir input directory')


args = parser.parse_args()
data_dir = args.data_dir
model_file = args.model_file
output_file = args.output_file
batch_size = args.batch_size
is_one_division = args.is_one_division

setup_gpu_memory()

normalization_layer = tf.keras.layers.experimental.preprocessing.Rescaling(1./255)
AUTOTUNE = tf.data.experimental.AUTOTUNE
strategy = tf.distribute.MirroredStrategy()
with strategy.scope():
    # load the model for prediction only, no need to compile the model
    model = tf.keras.models.load_model(model_file, compile=False)

res_df_list = []
time_list = []
divisions = []
if is_one_division:
    divisions.append(data_dir)
else:
    for subdir in os.listdir(data_dir):
        divisions.append(os.path.join(data_dir, subdir))

for div_dir in divisions:
    for subdir in os.listdir(div_dir):
        test_ds = image_dataset_from_directory(
            os.path.join(div_dir, subdir), validation_split=None, subset=None, label_mode=None,
            shuffle=False, image_size=(299, 299), batch_size=batch_size)
        normalized_test_ds = test_ds.map(lambda x: normalization_layer(x))
        normalized_test_ds = normalized_test_ds.cache().prefetch(buffer_size=AUTOTUNE)
        ts = time.time()
        pred = model.predict(normalized_test_ds)
        te = time.time()
        time_list.append(te-ts)
        res_df_list.append(pd.DataFrame({"MAPPED_IMAGE": test_ds.file_paths,
                                         "FEATURES": pred.tolist()}))
        res_df_list[-1].MAPPED_IMAGE = res_df_list[-1].MAPPED_IMAGE.str.replace(
            '/projects/ncdot/NC_2018_Secondary/images/', '')
        # release memory
        del test_ds
        del normalized_test_ds
        del pred

print('Total time taken for prediction: ', sum(time_list))
# combine multiple results into one
combined_results = pd.concat(res_df_list)
combined_results.to_csv(output_file, index=False)
count = gc.collect()
print('Done - count from return of gc.collect()', count)
