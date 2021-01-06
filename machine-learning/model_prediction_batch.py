import time
import argparse
import pandas as pd
import numpy as np
import tensorflow as tf
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from utils import setup_gpu_memory


parser = argparse.ArgumentParser(description='Process arguments.')
parser.add_argument('--data_dir', type=str, default='/projects/ncdot/NC_2018_Secondary/images/d4',
                    help='input dir of image data to apply model prediction for')
parser.add_argument('--model_file', type=str,
                    default='/projects/ncdot/2018/machine_learning/model/guardrail_xception_2lane_epoch_10.h5',
                    help='model file with path to be load for prediction')
parser.add_argument('--output_file', type=str,
                    default='/projects/ncdot/secondary_road/model_2lane_predict_d4.csv',
                    help='prediction output csv file')
parser.add_argument('--batch_size', type=int, default=2000, help='prediction batch size')

args = parser.parse_args()
data_dir = args.data_dir
model_file = args.model_file
output_file = args.output_file
batch_size = args.batch_size

setup_gpu_memory()

# load the model
model = tf.keras.models.load_model(model_file)
print(model.summary())

datagen = ImageDataGenerator(rescale=1 / 255)
test_gen = datagen.flow_from_directory(data_dir,
                                       target_size=(299, 299),
                                       class_mode='binary',
                                       batch_size=batch_size,
                                       follow_links=False,
                                       shuffle=False)
ts = time.time()
strategy = tf.distribute.MirroredStrategy()
pred = None
with strategy.scope():
    pred=model.predict_generator(test_gen, steps=int(test_gen.samples/batch_size + 1), verbose=1)
te = time.time()
print('batch prediction is done, time taken:', te-ts)
pred_rounded = np.round(pred, decimals=2)

results=pd.DataFrame({"file":test_gen.filenames,"prediction":pred[:,0], "class":pred_rounded[:,0]})
results.to_csv(output_file, index=False)
print('Done')
