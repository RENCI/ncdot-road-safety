################################################
# This script creates class weights for imbalanced training data which can be loaded when fitting a model to the data
################################################
import numpy as np
import argparse
import json
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from utils import setup_gpu_memory
from sklearn.utils import class_weight


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Process arguments.')
    parser.add_argument('--train_dir', type=str,
                        default='/projects/ncdot/NC_2018_Secondary/active_learning/guardrail/round5/data/train',
                        help='input dir of the training data')
    parser.add_argument('--batch_size', type=int, default=128,
                        help='batch size for training the model')
    parser.add_argument('--output_file', type=str,
                        default='/projects/ncdot/NC_2018_Secondary/active_learning/guardrail/round5/model/'
                                'class_weights.json',
                        help='class weight output file')

    args = parser.parse_args()
    # e.g., '/projects/ncdot/2018/machine_learning/data/train'
    train_dir = args.train_dir
    batch_size = args.batch_size
    output_file = args.output_file

    setup_gpu_memory()

    datagen = ImageDataGenerator(rescale=1 / 255)

    train_gen = datagen.flow_from_directory(
        train_dir,
        target_size=(299, 299),  # All images will be resized to 299 x 299
        class_mode='binary',
        batch_size=batch_size,
        follow_links=True,
        # Specify the classes explicitly
        classes=['no', 'yes'],
        shuffle=True)

    weights = class_weight.compute_class_weight('balanced', np.unique(train_gen.classes),
                                                train_gen.classes)
    train_class_weights = dict(enumerate(weights))
    with open(output_file, 'w') as fp:
        json.dump(train_class_weights, fp)
    print('Done')
