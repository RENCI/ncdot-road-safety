import time
import json
import gc
import argparse
import pandas as pd
import numpy as np
import tensorflow as tf
from utils import setup_gpu_memory


parser = argparse.ArgumentParser(description='Process arguments.')
parser.add_argument('--input_file', type=str,
                    default='/projects/ncdot/NC_2018_Secondary/image_features/d13_image_features.csv',
                    help='input file of feature vector data to apply model prediction for')
parser.add_argument('--model_file', type=str,
                    default='/projects/ncdot/2018/machine_learning/model/guardrail_xception_classification_head_model.h5',
                    help='model file with path to be load for prediction')
parser.add_argument('--output_file', type=str,
                    default='/projects/ncdot/NC_2018_Secondary/active_learning/guardrail/round0/predict/predict_d13.csv',
                    help='prediction output csv file')


args = parser.parse_args()
input_file = args.input_file
model_file = args.model_file
output_file = args.output_file


# read feature vectors from input file
in_df = pd.read_csv(input_file, header=0, index_col=False, dtype={'MAPPED_IMAGE': str, 'FEATURES': object},
                    memory_map=True)
in_df['FEATURES'] = in_df['FEATURES'].apply(lambda row: np.array(json.loads(row)))
# use np.stack to convert array of array into 2 dimentional np array for converting to tensors
test_ds = tf.data.Dataset.from_tensors(np.stack(in_df['FEATURES'].values))

setup_gpu_memory()

strategy = tf.distribute.MirroredStrategy()
with strategy.scope():
    # load the model for prediction only, no need to compile the model
    model = tf.keras.models.load_model(model_file, compile=False)

ts = time.time()
pred = model.predict(test_ds)
pred_rounded = np.round(pred, decimals=2)
te = time.time()
print('Total time taken for prediction: ', te-ts)
in_df = in_df.drop(columns=['FEATURES'])
in_df['ROUND_PREDICT'] = pred_rounded[:, 0]
in_df.to_csv(output_file, index=False)
count = gc.collect()
print('Done - count from return of gc.collect()', count)
