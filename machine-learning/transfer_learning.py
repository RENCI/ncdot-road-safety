import time
import argparse
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras.callbacks import TensorBoard
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.callbacks import ModelCheckpoint, EarlyStopping, ReduceLROnPlateau
from sklearn.metrics import classification_report, confusion_matrix
from utils import setup_gpu_memory


# All images will be rescaled by 1./255
datagen = ImageDataGenerator(rescale=1 / 255)


def get_call_backs_list():
    """
    return list of keras.callbacks.Callback instances that will be applied during training
    """
    tensorboard = TensorBoard(log_dir="logs/{}".format(time.time()))
    filepath = "weights-best.hdf5"
    checkpoint = ModelCheckpoint(filepath, monitor='val_loss', verbose=1, save_best_only=True,
                                 mode='min', save_freq='epoch')
    earlystop = EarlyStopping(monitor='val_loss', mode='min', patience=2)
    reduce = ReduceLROnPlateau(monitor='val_loss', factor=0.1, patience=1)
    return [earlystop, reduce, checkpoint, tensorboard]


def get_train_val_generator(bat_size, feat_name):
    """
    Get train and validation data generators
    :param bat_size: batch size
    :param feat_name: feature name that is used in label/class directory
    :return: train generator, validation generator
    """
    # load and iterate training dataset in batches of 128 using datagen generator
    train_gen = datagen.flow_from_directory(
        train_dir,  # This is the source directory for training images
        target_size=(299, 299),  # All images will be resized to 299 x 299
        batch_size=bat_size,
        follow_links=True,
        # Specify the classes explicitly
        classes=[f'{feat_name}_no', f'{feat_name}_yes'],
        class_mode='binary', shuffle=True)
    # load and iterate validation dataset. Important to set shuffle to False. Otherwise, labels will not
    # match when doing prediction on validation set
    val_gen = datagen.flow_from_directory(val_dir,
                                          target_size=(299, 299),
                                          class_mode='binary',
                                          follow_links=True,
                                          classes=[f'{feat_name}_no', f'{feat_name}_yes'],
                                          batch_size=bat_size,
                                          shuffle=False)

    return train_gen, val_gen


def initial_train(train_gen, callback_list, bat_size, val_gen):
    """
    Load Xception model trained on imagenet without the top classifier and add a new top classifier layer
    to train our model; freeze convolutional base feature extraction layers and only train the added top
    classification fully connected layer
    :param train_gen: training data generator
    :param callback_list: list of keras.callbacks.Callback instances to apply during training
    :param bat_size: batch size for training
    :param val_gen: validation data generator
    :return: the model for further fine-tuning after the initial top classifier training
    """
    initial_base_model = keras.applications.Xception(weights='imagenet', include_top=False)
    initial_base_model.trainable = False

    for layer in initial_base_model.layers:
        layer.trainable = False

    inputs = keras.Input(shape=(299, 299, 3))
    # make sure that the initial_base_model is running in inference mode by passing `training=False`.
    # This is important for fine-tuning
    x = initial_base_model(inputs, training=False)
    # add a mini network on top of the base model
    # Convert features of shape `initial_base_model.output_shape[1:]` to vectors
    x = keras.layers.GlobalAveragePooling2D()(x)
    # add a dropout layer for regularization to avoid overfitting
    x = keras.layers.Dropout(0.25)(x)
    # A Dense classifier with a single unit (binary classification)
    outputs = keras.layers.Dense(1, activation='sigmoid')(x)
    feature_model = keras.Model(inputs, outputs)
    print(feature_model.summary())

    feature_model.compile(optimizer=keras.optimizers.Adam(), # used the default 0.001 as learning rate
                          loss=keras.losses.BinaryCrossentropy(from_logits=True),
                          metrics=[keras.metrics.BinaryAccuracy()])
    ts = time.time()
    hist = feature_model.fit(train_gen, epochs=10, callbacks=callback_list,
                             steps_per_epoch=int(train_gen.samples / bat_size + 1),
                             validation_data=val_gen,
                             validation_steps=int(val_gen.samples / bat_size + 1))
    te = time.time()
    print('time taken for model fit:', te - ts)
    print(hist.history)
    # fine tuning the model with small learning rate
    # Unfreeze the base model
    feature_model.trainable = True
    # xCeption has 14 block layers, freeze block1 and block2 layers and open up higher layers for training
    for layer in feature_model.layers:
        if layer.name.startswith('block1_') or layer.name.startswith('block2_'):
            layer.trainable = False
        else:
            layer.trainable = True
    return feature_model


def make_inference(feature_model, bat_size, feat_name, threshold=0.5):
    """
    make model inference on test data and print confusion matrix and classification report
    :param feature_model: the model used for making inference
    :param bat_size: batch size for making inference
    :param feat_name: feature name such as guardrail
    :param threshold: threshold used to separate binary classes, 0.5 by default
    :return:
    """
    # load and iterate test dataset. Important to set shuffle to False. Otherwise, labels will not
    # match test data in returned predictions
    test_gen = datagen.flow_from_directory(test_dir,
                                           target_size=(299, 299),
                                           class_mode='binary',
                                           classes=[f'{feat_name}_no', f'{feat_name}_yes'],
                                           batch_size=bat_size,
                                           follow_links=True,
                                           shuffle=False)
    ts = time.time()
    predictions = feature_model.predict(test_gen, steps=int(test_gen.samples / bat_size + 1), verbose=1)
    te = time.time()
    print('time taken for model inference on test set:', te - ts)
    y_pred = [1 if y[0] >= threshold else 0 for y in predictions]
    print('Confusion Matrix')
    print(confusion_matrix(test_gen.classes, y_pred))
    print('Classification Report')
    target_names = [f'{feat_name}_no', f'{feat_name}_yes']
    print(classification_report(test_gen.classes, y_pred, target_names=target_names))


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Process arguments.')
    parser.add_argument('--train_dir', type=str, required=True, help='input dir of the training data')
    parser.add_argument('--val_dir', type=str, required=True, help='input dir of the validation data')
    parser.add_argument('--test_dir', type=str, required=True, help='input dir of the test data')
    parser.add_argument('--feature_name', type=str, default='guardrail', help='feature name such as guardrail')
    parser.add_argument('--use_own_base_model', action='store_true', default=True,
                        help='use own base model for further training rather than Xception base model')
    parser.add_argument('--num_of_epoch', type=int, default=30,
                        help='the number of total epoch to train the model')
    parser.add_argument('--batch_size', type=int, default=128,
                        help='batch size for training the model')
    parser.add_argument('--model_file', type=str,
                        default='/projects/ncdot/2018/machine_learning/model/guardrail_xception_base.h5',
                        help='model file with path to be loaded as the base model for further training')
    parser.add_argument('--output_model_file', type=str,
                        default='/projects/ncdot/2018/machine_learning/model/guardrail_xception.h5',
                        help='model file with path output by training')
    parser.add_argument('--make_inference_only', action='store_false', default=False,
                        help='if set together with model_file parameter, will make inference only '
                             'without further training the model')

    args = parser.parse_args()
    # e.g., '/projects/ncdot/2018/machine_learning/data/train'
    train_dir = args.train_dir
    # e.g., '/projects/ncdot/2018/machine_learning/data/validation'
    val_dir = args.val_dir
    # e.g., '/projects/ncdot/2018/machine_learning/data/test'
    test_dir = args.test_dir
    feature_name = args.feature_name
    use_own_base_model = args.use_own_base_model
    model_file = args.model_file
    output_model_file = args.output_model_file
    num_of_epoch = args.num_of_epoch
    batch_size = args.batch_size
    make_inference_only = args.make_inference_only

    setup_gpu_memory()
    if not make_inference_only:
        callbacks_list = get_call_backs_list()

        train_generator, validation_generator = get_train_val_generator(batch_size, feature_name)

        strategy = tf.distribute.MirroredStrategy()
        with strategy.scope():
            # Everthing that creates variables should be under the strategy scope
            if use_own_base_model:
                model = tf.keras.models.load_model(model_file)
                model.trainable = True
            else:
                model = initial_train(train_generator, callbacks_list, batch_size, validation_generator)

            layers = [(layer, layer.name, layer.trainable) for layer in model.layers]
            print(layers)
            # fine tune the model with a very low learning rate 1e-5
            model.compile(optimizer=keras.optimizers.Adam(1e-5),  # very low learning rate
                          loss=keras.losses.BinaryCrossentropy(from_logits=True),
                          metrics=[keras.metrics.BinaryAccuracy()])

        ts = time.time()
        history = model.fit(train_generator, epochs=num_of_epoch, callbacks=callbacks_list,
                            steps_per_epoch=int(train_generator.samples/batch_size + 1),
                            validation_data=validation_generator,
                            validation_steps=int(validation_generator.samples/batch_size + 1))
        te = time.time()
        print('time taken for model fine tuning:', te - ts)
        print(history.history)
        model.save(f'{feature_name}_model.h5')
        model.save(output_model_file)
    else:
        model = tf.keras.models.load_model(model_file)
    make_inference(model, batch_size*2, feature_name)
    print('Done')
