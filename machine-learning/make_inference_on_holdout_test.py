import time
import os
import pandas as pd
import numpy as np
import argparse
import tensorflow as tf
from image_dataset import image_dataset_from_directory
from sklearn.metrics import classification_report, confusion_matrix
from utils import setup_gpu_memory


def make_inference(feature_model, bat_size, threshold=0.5):
    normalization_layer = tf.keras.layers.experimental.preprocessing.Rescaling(1./255)
    AUTOTUNE = tf.data.experimental.AUTOTUNE
    # load and iterate test dataset. Important to set shuffle to False. Otherwise, labels will not
    # match when doing prediction on test set
    test_ds = image_dataset_from_directory(test_dir,
                                           validation_split=None, subset=None, label_mode='binary',
                                           shuffle=False, class_names=['no', 'yes'], image_size=(299, 299), batch_size=bat_size)
    normalized_test_ds = test_ds.map(lambda x, y: (normalization_layer(x), y))
    normalized_test_ds = normalized_test_ds.cache().prefetch(buffer_size=AUTOTUNE)
    ts = time.time()
    predictions = feature_model.predict(normalized_test_ds, verbose=True)
    te = time.time()
    print('time taken for model inference on test set:', te - ts)
    pred_rounded = np.round(predictions, decimals=2)
    df = pd.DataFrame({"MAPPED_IMAGE": test_ds.file_paths,
                       "ROUND_PREDICT": pred_rounded[:, 0]})
    df.MAPPED_IMAGE = df.MAPPED_IMAGE.str.replace(os.path.join(test_dir, 'yes') + '/', '')
    df.MAPPED_IMAGE = df.MAPPED_IMAGE.str.replace(os.path.join(test_dir, 'no') + '/', '')
    df.to_csv(output_file, index=False)
    y_pred = [1 if y[0] >= threshold else 0 for y in predictions]
    # labels = []
    # for image_batch, labl_batch in test_ds:
    #     for lbl in labl_batch:
    #         labels.append(lbl.numpy()[0])
    labels = test_ds.labels
    print('Confusion Matrix')
    print(confusion_matrix(labels, y_pred))
    print('Classification Report')
    target_names = ['no', 'yes']
    print(classification_report(labels, y_pred, target_names=target_names))


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Process arguments.')
    parser.add_argument('--test_dir', type=str, required=True, help='input dir of the test data')
    parser.add_argument('--batch_size', type=int, default=128,
                        help='batch size for training the model')
    parser.add_argument('--model_file', type=str,
                        default='/projects/ncdot/2018/machine_learning/model/guardrail_xception_2lane_epoch_10.h5',
                        help='model file with path to be loaded as the base model for further training')
    parser.add_argument('--output_file', type=str,
                    default='/projects/ncdot/NC_2018_Secondary/active_learning/guardrail/round0/predict/model_predict_test.csv',
                    help='prediction output csv file')

    args = parser.parse_args()
    test_dir = args.test_dir
    model_file = args.model_file
    batch_size = args.batch_size
    output_file = args.output_file

    setup_gpu_memory()
    strategy = tf.distribute.MirroredStrategy()
    with strategy.scope():
        model = tf.keras.models.load_model(model_file, compile=False)
    make_inference(model, batch_size*2)
    print('Done')
