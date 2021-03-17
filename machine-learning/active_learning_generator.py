import time
import argparse
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.callbacks import ModelCheckpoint, EarlyStopping, ReduceLROnPlateau
from sklearn.metrics import classification_report, confusion_matrix
from utils import setup_gpu_memory


datagen = ImageDataGenerator(rescale=1/255)


def get_call_backs_list():
    filepath = "weights-best.hdf5"
    checkpoint = ModelCheckpoint(filepath, monitor='val_loss', verbose=1, save_best_only=True,
                                 mode='min', save_freq='epoch')
    earlystop = EarlyStopping(monitor='binary_accuracy', patience=1)
    reduce = ReduceLROnPlateau(monitor='val_loss', factor=0.1, patience=5)
    return [earlystop, reduce, checkpoint]


def get_train_val_data(bat_size):
    # All images will be rescaled by 1./255
    # load and iterate training dataset in batches of 128
    train_gen = datagen.flow_from_directory(
        train_dir,
        target_size=(299, 299),  # All images will be resized to 299 x 299
        class_mode='binary',
        batch_size=bat_size,
        follow_links=True,
        # Specify the classes explicitly
        classes=['no', 'yes'],
        shuffle=True)
    val_gen = datagen.flow_from_directory(
        val_dir,
        target_size=(299, 299),
        follow_links=True,
        class_mode='binary',
        shuffle=False,
        # Specify the classes explicitly
        classes=['no', 'yes'],
        batch_size=bat_size)
    return train_gen, val_gen


def get_model(input_file):
    feature_model = tf.keras.models.load_model(input_file)
    # print(feature_model.summary())
    feature_model.trainable = False
    # only make the top dense classification layer (2049 parameters) trainable
    for layer in feature_model.layers[:-1]:
        layer.trainable = False
    feature_model.layers[-1].trainable = True

    feature_model.compile(optimizer=keras.optimizers.Adam(1e-5),
                          loss=keras.losses.BinaryCrossentropy(from_logits=True),
                          metrics=[keras.metrics.BinaryAccuracy()])
    return feature_model


def make_inference(feature_model, bat_size, threshold=0.5):
    # load and iterate test dataset. Important to set shuffle to False. Otherwise, labels will not
    # match when doing prediction on test set
    # load and iterate test dataset in batches of 128
    test_gen = datagen.flow_from_directory(test_dir,
                                           target_size=(299, 299),
                                           class_mode='binary',
                                           follow_links=True,
                                           classes=['no', 'yes'],
                                           batch_size=bat_size,
                                           shuffle=False)
    ts = time.time()
    predictions = feature_model.predict(test_gen, steps=int(test_gen.samples / bat_size + 1), verbose=1)
    te = time.time()
    print('time taken for model inference on test set:', te - ts)
    y_pred = [1 if y[0] >= threshold else 0 for y in predictions]
    #labels = []
    #for image_batch, labl_batch in test_ds:
    #    for lbl in labl_batch:
    #        labels.append(lbl.numpy()[0])
    print('Confusion Matrix')
    print(confusion_matrix(test_gen.classes, y_pred))
    print('Classification Report')
    target_names = ['no', 'yes']
    print(classification_report(test_gen.classes, y_pred, target_names=target_names))


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Process arguments.')
    parser.add_argument('--train_dir', type=str, required=True, help='input dir of the training data')
    parser.add_argument('--val_dir', type=str, required=True, help='input dir of the validation data')
    parser.add_argument('--test_dir', type=str, required=True, help='input dir of the test data')
    parser.add_argument('--num_of_epoch', type=int, default=10,
                        help='the number of total epoch to train the model')
    parser.add_argument('--batch_size', type=int, default=128,
                        help='batch size for training the model')
    parser.add_argument('--model_file', type=str,
                        default='/projects/ncdot/2018/machine_learning/model/guardrail_xception_2lane_epoch_10.h5',
                        help='model file with path to be loaded as the base model for further training')
    parser.add_argument('--output_model_file', type=str,
                        default='/projects/ncdot/NC_2018_Secondary/active_learning/guardrail/round1/model/guardrail_round1.h5',
                        help='model file with path output by training')
    parser.add_argument('--make_inference_only', action='store_false', default=False,
                        help='if set, will make inference only')

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

    setup_gpu_memory()
    strategy = tf.distribute.MirroredStrategy()
    if not make_inference_only:
        callbacks_list = get_call_backs_list()

        train_generator, validation_generator = get_train_val_data(batch_size)

        with strategy.scope():
            model = get_model(model_file)

        ts = time.time()
        history = model.fit(train_generator, epochs=num_of_epoch, callbacks=callbacks_list,
                            steps_per_epoch=int(train_generator.samples / batch_size + 1),
                            validation_data=validation_generator,
                            validation_steps=int(validation_generator.samples/batch_size + 1))
        te = time.time()
        print('time taken for model fine tuning:', te - ts)
        print(history.history)
        model.save(output_model_file)
    else:
        with strategy.scope():
            model = tf.keras.models.load_model(model_file)
    make_inference(model, batch_size*2)
    print('Done')
