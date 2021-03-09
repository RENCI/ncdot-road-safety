import gc
import argparse
import tensorflow as tf
from tensorflow import keras
from utils import setup_gpu_memory


parser = argparse.ArgumentParser(description='Process arguments.')
parser.add_argument('--model_file', type=str,
                    default='/projects/ncdot/NC_2018_Secondary/active_learning/guardrail/round1/model/guardrail_1.h5',
                    help='model file with path to be load for splitting')
parser.add_argument('--output_feature_model_file', type=str,
                    default='/projects/ncdot/NC_2018_Secondary/active_learning/guardrail/'
                            'round1/model/guardrail_feature_extraction_1.h5',
                    help='feature vector extraction model file')
parser.add_argument('--output_classification_model_file', type=str,
                    default='/projects/ncdot/NC_2018_Secondary/active_learning/guardrail/'
                            'round1/model/guardrail_classification_head_1.h5',
                    help='classification head model file')

args = parser.parse_args()
model_file = args.model_file
output_feature_model_file = args.output_feature_model_file
output_classification_model_file = args.output_classification_model_file

setup_gpu_memory()

strategy = tf.distribute.MirroredStrategy()
with strategy.scope():
    model = tf.keras.models.load_model(model_file)

feature_vector_model = tf.keras.models.Model(model.input, model.layers[2].output)
feature_vector_model.save(output_feature_model_file)

x = keras.Input(shape=(2048,))
classification_head_model = tf.keras.models.Model(x, model.layers[4](x))
classification_head_model.save(output_classification_model_file)

count = gc.collect()
print('Done - count from return of gc.collect()', count)
