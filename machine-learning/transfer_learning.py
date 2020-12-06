import time
import argparse
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras.callbacks import TensorBoard
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.callbacks import ModelCheckpoint, EarlyStopping, ReduceLROnPlateau
from sklearn.metrics import classification_report, confusion_matrix
from utils import setup_gpu_memory


def get_call_backs_list(feat_name):
    tensorboard = TensorBoard(log_dir="logs/{}".format(time.time()))
    filepath = f'{feat_name}_model_checkpoint.h5'
    checkpoint = ModelCheckpoint(filepath, monitor='val_loss', verbose=1, save_best_only=True, save_weights_only=False,
                                 mode='auto', save_freq=1)
    earlystop = EarlyStopping(monitor='binary_accuracy', patience=1)
    reduce = ReduceLROnPlateau(monitor='val_loss', factor=0.1, patience=8)
    return [earlystop, reduce, checkpoint, tensorboard]


def get_train_val_test_generator(bat_size, feat_name):
    # All images will be rescaled by 1./255
    datagen = ImageDataGenerator(rescale=1 / 255)
    # load and iterate training dataset in batches of 128 using datagen generator
    train_gen = datagen.flow_from_directory(
        train_dir,  # This is the source directory for training images
        target_size=(299, 299),  # All images will be resized to 299 x 299
        batch_size=bat_size,
        # Specify the classes explicitly
        classes=[f'{feat_name}_no', f'{feat_name}_yes'],
        class_mode='binary', shuffle=True)
    # load and iterate validation dataset. Important to set shuffle to False. Otherwise, labels will not
    # match when doing prediction on validation set
    val_gen = datagen.flow_from_directory(val_dir,
                                          target_size=(299, 299),
                                          class_mode='binary',
                                          classes=[f'{feat_name}_no', f'{feat_name}_yes'],
                                          batch_size=bat_size,
                                          shuffle=False)

    # load and iterate test dataset. Important to set shuffle to False. Otherwise, labels will not
    # match when doing prediction on test set
    test_gen = datagen.flow_from_directory(test_dir,
                                           target_size=(299, 299),
                                           class_mode='binary',
                                           classes=[f'{feat_name}_no', f'{feat_name}_yes'],
                                           batch_size=bat_size,
                                           shuffle=False)
    return train_gen, val_gen, test_gen


def initial_train(initial_base_model, train_gen, callback_list, bat_size, val_gen):
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

    feature_model.compile(optimizer=keras.optimizers.Adam(),
                          loss=keras.losses.BinaryCrossentropy(from_logits=True),
                          metrics=[keras.metrics.BinaryAccuracy()])
    ts = time.time()
    hist = feature_model.fit(train_gen, epochs=10, callbacks=callback_list,
                             steps_per_epoch=int(train_gen.samples / bat_size),
                             validation_data=val_gen,
                             validation_steps=int(val_gen.samples / bat_size))
    te = time.time()
    print('time taken for model fit:', te - ts)
    print(hist.history)
    return feature_model


def make_inference(feature_model, test_gen, bat_size, feat_name, threshold=0.5):
    predictions = feature_model.predict(test_gen, steps=int(test_gen.samples / bat_size + 1), verbose=1)
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
    parser.add_argument('--model_file', type=str,
                        default='/projects/ncdot/2018/machine_learning/model/guardrail_xception_subset.h5',
                        help='model file with path to be loaded as the base model for further training')
    parser.add_argument('--output_model_file', type=str,
                        default='/projects/ncdot/2018/machine_learning/model/guardrail_xception.h5',
                        help='model file with path output by training')
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
    batch_size = 128

    setup_gpu_memory()

    callbacks_list = get_call_backs_list(feature_name)

    train_generator, validation_generator, test_generator = get_train_val_test_generator(batch_size, feature_name)

    strategy = tf.distribute.MirroredStrategy()
    with strategy.scope():
        base_model = keras.applications.Xception(weights='imagenet', include_top=False)
        if use_own_base_model:
            model = tf.keras.models.load_model(model_file)
        else:
            model = initial_train(base_model, train_generator, callbacks_list, batch_size, validation_generator)

        # fine tuning the model with small learning rate
        # Unfreeze the base model
        base_model.trainable = True
        # xCeption has 14 block layers, freeze block1 and block2 layers and open up higher layers for training
        for layer in base_model.layers:
            if layer.name.startswith('block1_') or layer.name.startswith('block2_'):
                layer.trainable = False
            else:
                layer.trainable = True
        layers = [(layer, layer.name, layer.trainable) for layer in base_model.layers]
        print(layers)
        ts = time.time()
        model.compile(optimizer=keras.optimizers.Adam(1e-5),  # Very low learning rate
                      loss=keras.losses.BinaryCrossentropy(from_logits=True),
                      metrics=[keras.metrics.BinaryAccuracy()])
        history = model.fit(train_generator, epochs=100, callbacks=callbacks_list,
                            steps_per_epoch=int(train_generator.samples/batch_size),
                            validation_data=validation_generator,
                            validation_steps=int(validation_generator.samples/batch_size))
        te = time.time()
        print('time taken for model fine tuning:', te - ts)
        print(history.history)
        model.save(f'{feature_name}_model.h5')
        model.save(output_model_file)
        ts = time.time()
        make_inference(model, train_generator, batch_size*2, feature_name)
        te = time.time()
        print('time taken for model inference on test set:', te - ts)
