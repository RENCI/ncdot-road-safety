# Reference: https://machinelearningmastery.com/reproducible-results-neural-networks-keras/
from numpy.random import seed
seed(42)

import time
import argparse
import tensorflow as tf
from tensorflow import keras
from image_dataset import image_dataset_from_directory
from tensorflow.keras.callbacks import ModelCheckpoint, EarlyStopping, ReduceLROnPlateau
from sklearn.metrics import classification_report, confusion_matrix
from utils import setup_gpu_memory


tf.compat.v1.random.set_random_seed(42)
normalization_layer = tf.keras.layers.experimental.preprocessing.Rescaling(1./255)
AUTOTUNE = tf.data.experimental.AUTOTUNE


def get_call_backs_list():
    """
    return list of keras.callbacks.Callback instances that will be applied during training
    """
    filepath = "weights-best.h5"
    checkpoint = ModelCheckpoint(filepath, monitor='val_loss', verbose=1, save_best_only=True,
                                 mode='min', save_freq='epoch')
    earlystop = EarlyStopping(monitor='val_loss', mode='min', patience=10)
    reduce = ReduceLROnPlateau(monitor='val_loss', factor=0.1, patience=2)
    return [earlystop, reduce, checkpoint]


def get_train_val_data(bat_size):
    """
    Get normalized train and validation datasets
    :param bat_size: batch size for loading dataset in batches
    :return: normalized train dataset, size of train dataset, normalized validation dataset, size of validation dataset
    """
    # All images will be rescaled by 1./255
    # load and iterate training dataset in batches
    train_ds = image_dataset_from_directory(
        train_dir,
        validation_split=None,
        subset=None,
        label_mode='binary',
        shuffle=True,
        seed=42,
        # specify the classes explicitly
        class_names=['no', 'yes'],
        image_size=(299, 299),
        batch_size=bat_size)
    val_ds = image_dataset_from_directory(
        val_dir,
        validation_split=None,
        subset=None,
        label_mode='binary',
        shuffle=False,
        # specify the classes explicitly
        class_names=['no', 'yes'],
        image_size=(299, 299),
        batch_size=bat_size)
    normalized_train_ds = train_ds.map(lambda x, y: (normalization_layer(x), y))
    normalized_valid_ds = val_ds.map(lambda x, y: (normalization_layer(x), y))
    normalized_train_ds = normalized_train_ds.cache().prefetch(buffer_size=AUTOTUNE)
    normalized_valid_ds = normalized_valid_ds.cache().prefetch(buffer_size=AUTOTUNE)
    return normalized_train_ds, len(train_ds), normalized_valid_ds, len(val_ds)


def get_model(input_file):
    """
    Get the model for active learning with random weights for the top classification head layer
    :param input_file: the model file to load model from
    :return: the model instance
    """
    feature_model = tf.keras.models.load_model(input_file)
    # print(feature_model.summary())
    feature_model.trainable = True
    # only make the top dense classification layer (2049 parameters) trainable
    for layer in feature_model.layers[:-1]:
        layer.trainable = False

    # randomize classification head layer's weights and make it trainable
    head_layer = feature_model.layers[-1]
    weight_initializer = tf.keras.initializers.GlorotUniform(seed=42)
    bias_initializer = tf.keras.initializers.Zeros()
    old_weights, old_biases = head_layer.get_weights()
    head_layer.set_weights([
        weight_initializer(shape=old_weights.shape),
        bias_initializer(shape=old_biases.shape)])
    head_layer.trainable = True

    # use a small learning rate 1e-5 given the active learning training dataset is relatively small
    feature_model.compile(optimizer=keras.optimizers.Adam(1e-5),
                          loss=keras.losses.BinaryCrossentropy(from_logits=True),
                          metrics=[keras.metrics.BinaryAccuracy()])
    print(feature_model.summary())
    return feature_model


def make_inference(feature_model, bat_size, threshold=0.5):
    """
    make model inference on test data and print confusion matrix and classification report
    :param feature_model: the model used for making inference
    :param bat_size: batch size for making inference
    :param threshold: threshold used to separate binary classes, 0.5 by default
    :return:
    """
    # load and iterate test dataset in batches. Important to set shuffle to False. Otherwise, labels will not
    # match test set in returned predictions
    test_ds = image_dataset_from_directory(
        test_dir,
        validation_split=None,
        subset=None,
        label_mode='binary',
        shuffle=False,
        # specify the classes explicitly
        class_names=['no', 'yes'],
        image_size=(299, 299),
        batch_size=bat_size)
    normalized_test_ds = test_ds.map(lambda x, y: (normalization_layer(x), y))
    normalized_test_ds = normalized_test_ds.cache().prefetch(buffer_size=AUTOTUNE)
    ts = time.time()
    predictions = feature_model.predict(normalized_test_ds)
    te = time.time()
    print('time taken for model inference on test set:', te - ts)
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
    parser.add_argument('--train_dir', type=str, required=True, help='input dir of the training data')
    parser.add_argument('--val_dir', type=str, required=True, help='input dir of the validation data')
    parser.add_argument('--test_dir', type=str, required=True, help='input dir of the test data')
    parser.add_argument('--num_of_epoch', type=int, default=100,
                        help='the number of total epoch to train the model')
    parser.add_argument('--batch_size', type=int, default=128,
                        help='batch size for training the model')
    parser.add_argument('--model_file', type=str,
                        default='/projects/ncdot/2018/machine_learning/model/guardrail_xception_2lane_epoch_10.h5',
                        help='model file with path to be loaded as the base model for further training')
    parser.add_argument('--output_model_file', type=str,
                        default='/projects/ncdot/NC_2018_Secondary/active_learning/guardrail/round1/model/guardrail_round1.h5',
                        help='model file with path output by training')
    parser.add_argument('--make_inference_only', action='store_true', default=False,
                        help='if set, will make inference only')
    parser.add_argument('--class_weights', type=dict,
                        default={0: 0.5996278377372535, 1: 3.0093388121031004},
                        help='class weights to pass in fit() for unbalanced training data')

    args = parser.parse_args()
    # e.g., '/projects/ncdot/2018/machine_learning/data/train'
    train_dir = args.train_dir
    # e.g., '/projects/ncdot/2018/machine_learning/data/validation'
    val_dir = args.val_dir
    # e.g., '/projects/ncdot/2018/machine_learning/data/test'
    test_dir = args.test_dir
    model_file = args.model_file
    output_model_file = args.output_model_file
    num_of_epoch = args.num_of_epoch
    batch_size = args.batch_size
    make_inference_only = args.make_inference_only
    class_weights = args.class_weights

    setup_gpu_memory()
    strategy = tf.distribute.MirroredStrategy()
    if not make_inference_only:
        callbacks_list = get_call_backs_list()

        norm_train_ds, train_ds_len, norm_val_ds, val_ds_len = get_train_val_data(batch_size)

        with strategy.scope():
            model = get_model(model_file)

        ts = time.time()
        if class_weights:
            history = model.fit(norm_train_ds, epochs=num_of_epoch, callbacks=callbacks_list,
                                class_weight=class_weights,
                                validation_data=norm_val_ds)
        else:
            history = model.fit(norm_train_ds, epochs=num_of_epoch, callbacks=callbacks_list,
                                validation_data=norm_val_ds)
        te = time.time()
        print('time taken for model fine tuning:', te - ts)
        print(history.history)
        model.save(output_model_file)
    else:
        with strategy.scope():
            model = tf.keras.models.load_model(model_file)
    make_inference(model, batch_size*2)
    print('Done')
