import time
import argparse
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras.callbacks import TensorBoard
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.callbacks import ModelCheckpoint, EarlyStopping, ReduceLROnPlateau
from sklearn.metrics import classification_report, confusion_matrix


parser = argparse.ArgumentParser(description='Process arguments.')
parser.add_argument('--train_dir', type=str, required=True, help='input dir of the training data')
parser.add_argument('--val_dir', type=str, required=True, help='input dir of the validation data')
parser.add_argument('--test_dir', type=str, required=True, help='input dir of the test data')
parser.add_argument('--feature_name', type=str, default='guardrail', help='feature name such as guardrail')
args = parser.parse_args()
# e.g., '/projects/ncdot/2018/machine_learning/data/train'
train_dir = args.train_dir
# e.g., '/projects/ncdot/2018/machine_learning/data/validation'
val_dir = args.val_dir
# e.g., '/projects/ncdot/2018/machine_learning/data/test'
test_dir = args.test_dir
feature_name = args.feature_name

# there are 2 GPUs with 32GB mem each on groucho. Need to set memory limit to 30G for each to avoid
# running exceptions
tf.config.experimental.set_memory_growth = True
gpus = tf.config.experimental.list_physical_devices('GPU')
if len(gpus) == 2:
  try:
    tf.config.experimental.set_virtual_device_configuration(
        gpus[0],
        [tf.config.experimental.VirtualDeviceConfiguration(memory_limit=1024*30)])
    tf.config.experimental.set_virtual_device_configuration(
        gpus[1],
        [tf.config.experimental.VirtualDeviceConfiguration(memory_limit=1024*30)])
    logical_gpus = tf.config.experimental.list_logical_devices('GPU')
    print(len(gpus), "Physical GPU,", len(logical_gpus), "Logical GPUs")
  except RuntimeError as e:
    # Virtual devices must be set before GPUs have been initialized
    print(e)

tensorboard = TensorBoard(log_dir="logs/{}".format(time()))

filepath = f'{feature_name}_model_checkpoint.h5'
checkpoint = ModelCheckpoint(filepath, monitor='val_loss', verbose=1, save_best_only=True, save_weights_only=False,
                             mode='auto', save_freq=1)
earlystop = EarlyStopping(monitor='binary_accuracy', patience=1)
reduce = ReduceLROnPlateau(monitor='val_loss', factor=0.1, patience=8)
callbacks_list = [earlystop, reduce, checkpoint, tensorboard]

batch_size = 128

# All images will be rescaled by 1./255
datagen = ImageDataGenerator(rescale=1/255)
# load and iterate training dataset in batches of 128 using datagen generator
train_generator = datagen.flow_from_directory(
        train_dir,  # This is the source directory for training images
        target_size=(299, 299),  # All images will be resized to 299 x 299
        batch_size=batch_size,
        # Specify the classes explicitly
        classes = [f'{feature_name}_no', f'{feature_name}_yes'],
        class_mode='binary', shuffle=True)
# load and iterate validation dataset. Important to set shuffle to False. Otherwise, labels will not
# match when doing prediction on validation set
validation_generator = datagen.flow_from_directory(val_dir,
                                                   target_size=(299, 299),
                                                   class_mode='binary',
                                                   classes = [f'{feature_name}_no',f'{feature_name}_yes'],
                                                   batch_size=batch_size,
                                                   shuffle=False)

# load and iterate test dataset. Important to set shuffle to False. Otherwise, labels will not
# match when doing prediction on test set
test_generator = datagen.flow_from_directory(test_dir,
                                             target_size=(299, 299),
                                             class_mode='binary',
                                             classes = [f'{feature_name}_no',f'{feature_name}_yes'],
                                             batch_size=batch_size,
                                             shuffle=False)

strategy = tf.distribute.MirroredStrategy()
with strategy.scope():
    base_model=keras.applications.Xception(weights='imagenet',include_top=False)
    base_model.trainable = False
    inputs = keras.Input(shape=(299, 299, 3))
    # make sure that the base_model is running in inference mode by passing `training=False`.
    # This is important for fine-tuning
    x = base_model(inputs, training=False)
    # add a mini network on top of the base model
    # Convert features of shape `base_model.output_shape[1:]` to vectors
    x = keras.layers.GlobalAveragePooling2D()(x)
    # add a dropout layer for regularization to avoid overfitting
    x = keras.layers.Dropout(0.25)(x)
    # A Dense classifier with a single unit (binary classification)
    outputs = keras.layers.Dense(1, activation='sigmoid')(x)
    model = keras.Model(inputs, outputs)
    print(model.summary())
    model.compile(optimizer=keras.optimizers.Adam(),
                  loss=keras.losses.BinaryCrossentropy(from_logits=True),
                  metrics=[keras.metrics.BinaryAccuracy()])
    ts = time.time()
    history = model.fit(train_generator, epochs=10, callbacks = callbacks_list,
                        steps_per_epoch=int(train_generator.samples/batch_size),
                        validation_data = validation_generator,
                        validation_steps=int(validation_generator.samples/batch_size))
    te = time.time()
    print('time taken for model fit:', te-ts)
    print(history.history)

    # fine tuning the model
    with strategy.scope():
        # Unfreeze the base model
        base_model.trainable = True
        model.compile(optimizer=keras.optimizers.Adam(1e-5),  # Very low learning rate
                      loss=keras.losses.BinaryCrossentropy(from_logits=True),
                      metrics=[keras.metrics.BinaryAccuracy()])
        history = model.fit(train_generator, epochs=10, callbacks=callbacks_list,
                            steps_per_epoch=int(train_generator.samples/batch_size),
                            validation_data=validation_generator,
                            validation_steps=int(validation_generator.samples/batch_size))

    print(history.history)
    model.save(f'{feature_name}_model.h5')

    predictions = model.predict(test_generator, steps=int(test_generator.samples/batch_size + 1),
                                verbose=1)
    y_pred = [1 if y[0] >= 0.5 else 0 for y in predictions]
    print('Confusion Matrix')
    print(confusion_matrix(test_generator.classes, y_pred))
    print('Classification Report')
    target_names = ['guardrail_no', 'guardrail_yes']
    print(classification_report(test_generator.classes, y_pred, target_names=target_names))
