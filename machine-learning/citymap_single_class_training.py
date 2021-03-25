import time
import argparse
import pandas as pd
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.callbacks import ModelCheckpoint, EarlyStopping, ReduceLROnPlateau
from sklearn.metrics import classification_report, confusion_matrix
from utils import setup_gpu_memory


def get_call_backs_list():
    filepath = "weights-best.hdf5"
    checkpoint = ModelCheckpoint(filepath, monitor='val_loss', verbose=1, save_best_only=True,
                                 mode='min', save_freq='epoch')
    earlystop = EarlyStopping(monitor='binary_accuracy', patience=1)
    reduce = ReduceLROnPlateau(monitor='val_loss', factor=0.1, patience=5)
    return [earlystop, reduce, checkpoint]


def get_train_val_data(bat_size, main_df, class_name):
    # All images will be rescaled by 1./255
    # load and iterate training dataset in batches of 128
    train_datagen = ImageDataGenerator(rescale=1/255, validation_split=0.05)

    # I am going to use the 'val' set as the test data later, just because it's easier to use the built in
    # ImageDataGenerator function to split into train/val from the single 'train' dataframe.
    train_df = main_df[main_df['set'] != 'val']
    train_gen = train_datagen.flow_from_dataframe(
        train_df,
        x_col='image_path',
        y_col=class_name,
        subset='training',
        target_size=(299, 299),  # All images will be resized to 299 x 299
        class_mode='binary',
        classes=['no','yes'],
        batch_size=bat_size,
        shuffle=True,
        seed=42)
    val_gen = train_datagen.flow_from_dataframe(
        train_df,
        x_col='image_path',
        y_col=class_name,
        subset='validation',
        target_size=(299, 299),  # All images will be resized to 299 x 299
        class_mode='binary',
        classes=['no','yes'],
        batch_size=bat_size,
        shuffle=True,
        seed=42)

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


def make_inference(feature_model, bat_size, main_df, class_name, threshold=0.5):
    # load and iterate test dataset. Important to set shuffle to False. Otherwise, labels will not
    # match when doing prediction on test set
    # load and iterate test dataset in batches of 128
    test_datagen = ImageDataGenerator(rescale=1/255)

    # We are using the 'val' set for test data because the test data have no annotations
    test_df = main_df[main_df['set'] == 'val']
    test_gen = test_datagen.flow_from_dataframe(
        test_df,
        x_col='image_path',
        y_col=class_name,
        target_size=(299, 299),  # All images will be resized to 299 x 299
        class_mode='binary',
        classes=['no','yes'],
        batch_size=bat_size,
        shuffle=False)

    print('Starting prediction')
    ts = time.time()
    predictions = feature_model.predict(test_gen, steps=int(test_gen.samples / bat_size + 1), verbose=1)
    te = time.time()
    print('time taken for model inference on test set:', te - ts)
    y_pred = [1 if y[0] >= threshold else 0 for y in predictions]
    print('Confusion Matrix')
    print(confusion_matrix(test_gen.classes, y_pred))
    print('Classification Report')
    target_names = ['no', 'yes']
    print(classification_report(test_gen.classes, y_pred, target_names=target_names))


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Process arguments.')
    parser.add_argument('--class_name', type=str, required=True, help='column of dataframe to include in training')
    parser.add_argument('--num_of_epoch', type=int, default=10,
                        help='the number of total epoch to train the model')
    parser.add_argument('--batch_size', type=int, default=128,
                        help='batch size for training the model')
    parser.add_argument('--model_file', type=str,
                        default='/projects/ncdot/2018/machine_learning/model/guardrail_xception_2lane_epoch_10.h5',
                        help='model file with path to be loaded as the base model for further training')
    parser.add_argument('--output_model_file', type=str,
                        default='/projects/ncdot/2018/machine_learning/model/citymap_xception_pole.h5',
                        help='model file with path output by training')
    parser.add_argument('--make_inference_only', action='store_true', default=False,
                        help='if set, will make inference only')
    parser.add_argument('--df_path', type=str, help='path to main dataset df', 
                        default='/projects/ncdot/segmentation_models/cityscapes_mapillary_paths_and_labels.csv')


    args = parser.parse_args()
    # e.g., '/projects/ncdot/2018/machine_learning/data/test'
    class_name = args.class_name
    model_file = args.model_file
    output_model_file = args.output_model_file
    num_of_epoch = args.num_of_epoch
    batch_size = args.batch_size
    make_inference_only = args.make_inference_only
    df_path = args.df_path

    # Define which columns to read from main dataframe and read in
    cols = ['image', 'set', 'image_path']
    cols.append(class_name)
    main_df = pd.read_csv(df_path, usecols=cols)
    # For 'binary' class mode, columns must be strings. This converts from one-hot to str
    for i,image in enumerate(main_df['image']):
        main_df.loc[i,class_name] = 'yes' if main_df.loc[i,class_name] == 1 else 'no'

    setup_gpu_memory()
    strategy = tf.distribute.MirroredStrategy()
    if not make_inference_only:
        callbacks_list = get_call_backs_list()

        train_generator, validation_generator = get_train_val_data(batch_size, main_df, class_name)

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
    make_inference(model, batch_size, main_df, class_name)
    print('Done')
