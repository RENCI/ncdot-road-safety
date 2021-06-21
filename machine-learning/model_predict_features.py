import time
import json
import os
import gc
import argparse
import pandas as pd
import numpy as np
import tensorflow as tf
from utils import setup_gpu_memory


def read_input_file_into_df(input_file):
    # read feature vectors from input file
    if input_file.endswith('.csv'):
        df = pd.read_csv(input_file, header=0, index_col=False, dtype={'MAPPED_IMAGE': str, 'FEATURES': object},
                         memory_map=True)
        df['FEATURES'] = df['FEATURES'].apply(lambda row: np.array(json.loads(row)))
        return df
    elif input_file.endswith('.parquet'):
        df = pd.read_parquet(input_file, engine='fastparquet')
        df['FEATURES'] = df['FEATURES'].apply(lambda row: np.array(row))
        return df
    else:
        return None


def predict_on_dataset(in_model, ds, df):
    ts = time.time()
    pred = in_model.predict(ds)
    pred_rounded = np.round(pred, decimals=2)
    te = time.time()
    print('Total time taken for prediction: ', te - ts)
    df = df.drop(columns=['FEATURES'])
    df['ROUND_PREDICT'] = pred_rounded[:, 0]
    return df


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Process arguments.')
    parser.add_argument('--input_file_or_dir', type=str,
                        default='/projects/ncdot/NC_2018_Secondary/image_features/d13_image_features.csv',
                        help='input file or directory of feature vector data to apply model prediction for')
    parser.add_argument('--model_file', type=str,
                        default='/projects/ncdot/2018/machine_learning/model/guardrail_xception_classification_head_model.h5',
                        help='model file with path to be load for prediction')
    parser.add_argument('--output_file', type=str,
                        default='/projects/ncdot/NC_2018_Secondary/active_learning/guardrail/round0/predict/predict_d13.csv',
                        help='prediction output csv file')


    args = parser.parse_args()
    input_file_or_dir = args.input_file
    model_file = args.model_file
    output_file = args.output_file

    in_df = read_input_file_into_df(input_file_or_dir)

    setup_gpu_memory()
    strategy = tf.distribute.MirroredStrategy()
    with strategy.scope():
        # load the model for prediction only, no need to compile the model
        model = tf.keras.models.load_model(model_file, compile=False)

    if in_df is None:
        # it is a directory
        res_df_list = []
        for f in os.listdir(input_file_or_dir):
            in_df = read_input_file_into_df(os.path.join(input_file_or_dir, f))
            test_ds = tf.data.Dataset.from_tensors(np.stack(in_df['FEATURES'].values))
            res_df_list.append(predict_on_dataset(model, test_ds, in_df))
            count = gc.collect()
            print('count from return of gc.collect()', count)
        combined_df = pd.concat(res_df_list)
        combined_df.to_csv(output_file, index=False)
    else:
        # use np.stack to convert array of array into 2 dimentional np array for converting to tensors
        test_ds = tf.data.Dataset.from_tensors(np.stack(in_df['FEATURES'].values))
        in_df = predict_on_dataset(model, test_ds, in_df)
        in_df.to_csv(output_file, index=False)
    count = gc.collect()
    print('Done - count from return of gc.collect()', count)
