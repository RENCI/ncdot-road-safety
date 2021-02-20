import time
import argparse
import pandas as pd
import numpy as np
import tensorflow as tf
from image_dataset import image_dataset_from_directory
from utils import setup_gpu_memory


parser = argparse.ArgumentParser(description='Process arguments.')
parser.add_argument('--data_dir', type=str,
                    default='/projects/ncdot/NC_2018_Secondary/images/d4',
                    help='input dir of data to apply model prediction for')
parser.add_argument('--model_file', type=str,
                    default='/projects/ncdot/2018/machine_learning/model/guardrail_xception_2lane_epoch_10.h5',
                    help='model file with path to be load for prediction')
parser.add_argument('--output_file', type=str,
                    default='/projects/ncdot/secondary_road/model_2lane_predict_d4.csv',
                    help='prediction output csv file')
parser.add_argument('--batch_size', type=int, default=1024,
                    help='prediction batch size')
parser.add_argument('--cache_file', type=str, default='/projects/ncdot/NC_2018_Secondary/cache.txt',
                    help='cache file on disk since data is too large to fit into memory for cache')


args = parser.parse_args()
data_dir = args.data_dir
model_file = args.model_file
output_file = args.output_file
batch_size = args.batch_size
cache_file = args.cache_file

setup_gpu_memory()

normalization_layer = tf.keras.layers.experimental.preprocessing.Rescaling(1./255)
AUTOTUNE = tf.data.experimental.AUTOTUNE
test_ds = image_dataset_from_directory(
    data_dir, validation_split=None, subset=None, label_mode=None,
    shuffle=False, image_size=(299, 299), batch_size=batch_size)
normalized_test_ds = test_ds.map(lambda x: normalization_layer(x))
normalized_test_ds = normalized_test_ds.cache(cache_file).prefetch(buffer_size=AUTOTUNE)

strategy = tf.distribute.MirroredStrategy()
pred = None
with strategy.scope():
    # load the model
    model = tf.keras.models.load_model(model_file)

ts = time.time()
pred = model.predict(normalized_test_ds)
te = time.time()
print('batch prediction is done, time taken:', te-ts)
pred_rounded = np.round(pred, decimals=2)

results = pd.DataFrame({"MAPPED_IMAGE": test_ds.file_paths,
                        "PREDICT": pred[:, 0],
                        "ROUND_PREDICT": pred_rounded[:, 0]})
results.to_csv(output_file, index=False)
print('Done')
