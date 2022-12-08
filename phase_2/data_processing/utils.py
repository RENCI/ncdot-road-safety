import numpy as np
from PIL import Image


POLE = 2


def consecutive(data, step_size=1):
    split_indices = np.where(np.diff(data) > step_size)[0]
    return split_indices, np.split(data, split_indices+1)


def get_object_data_from_image(input_image_name, object_level):
    input_image = Image.open(input_image_name)
    image_width = input_image.width
    image_height = input_image.height
    input_data = np.array(input_image)
    return image_width, image_height, np.where(input_data == object_level)
