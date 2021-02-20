import time
import os
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
                    default='/projects/ncdot/2018/machine_learning/model/guardrail_xception_2lane_epoch_10.h5',
                    help='model file with path to be load for prediction')
parser.add_argument('--output_file', type=str,
                    default='/projects/ncdot/NC_2018_Secondary/active_learning/guardrail/round0/predict/predict_d13.csv',
                    help='prediction output csv file')
parser.add_argument('--batch_size', type=int, default=512,
                    help='prediction batch size')


args = parser.parse_args()
data_dir = args.data_dir
model_file = args.model_file
output_file = args.output_file
batch_size = args.batch_size
cache_file = args.cache_file

setup_gpu_memory()

normalization_layer = tf.keras.layers.experimental.preprocessing.Rescaling(1./255)
AUTOTUNE = tf.data.experimental.AUTOTUNE
strategy = tf.distribute.MirroredStrategy()
with strategy.scope():
    # load the model
    model = tf.keras.models.load_model(model_file)

result_file_list = []
for subdir in os.listdir(data_dir):
    test_ds = image_dataset_from_directory(
        subdir, validation_split=None, subset=None, label_mode=None,
        shuffle=False, image_size=(299, 299), batch_size=batch_size)
    normalized_test_ds = test_ds.map(lambda x: normalization_layer(x))
    normalized_test_ds = normalized_test_ds.cache().prefetch(buffer_size=AUTOTUNE)
    ts = time.time()
    pred = model.predict(normalized_test_ds)
    te = time.time()
    print(f'batch prediction for {subdir} is done, time taken:', te-ts)
    pred_rounded = np.round(pred, decimals=2)

    results = pd.DataFrame({"MAPPED_IMAGE": test_ds.file_paths,
                            "PREDICT": pred[:, 0],
                            "ROUND_PREDICT": pred_rounded[:, 0]})
    results.MAPPED_IMAGE = results.MAPPED_IMAGE.str.replace('/projects/ncdot/NC_2018_Secondary/images/', '')
    result_file_list.append(f'{output_file}.{subdir}')
    results.to_csv(result_file_list[-1], index=False)
    # release memory
    del results
    del test_ds
    del normalized_test_ds
    del pred
    del pred_rounded

del model
# combine multiple results into one
res_df_list = []
for res_file in result_file_list:
    res_df_list.append(pd.read_csv(res_file, header=0, index_col=False))
combined_results = pd.concat(res_df_list)
combined_results.to_csv(output_file, index=False)
# remove subset files now that combines results are saved to file
for res_file in result_file_list:
    os.remove(res_file)
print('Done')
