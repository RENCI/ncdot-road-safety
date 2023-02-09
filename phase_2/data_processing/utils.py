import numpy as np
from PIL import Image
import math

ROAD = 1
POLE = 2


def consecutive(data, step_size=1):
    split_indices = np.where(np.diff(data) > step_size)[0]
    return split_indices, np.split(data, split_indices+1)


def get_data_from_image(input_image_name):
    input_image = Image.open(input_image_name)
    image_width = input_image.width
    image_height = input_image.height
    input_data = np.array(input_image)
    return image_width, image_height, input_data


def bearing_between_two_latlon_points(lat1, lon1, lat2, lon2):
    lon_delta_rad = math.radians(lon2-lon1)
    lat1_rad = math.radians(lat1)
    lat2_rad = math.radians(lat2)
    y = math.sin(lon_delta_rad) * math.cos(lat2_rad)
    x = math.cos(lat1_rad)*math.sin(lat2_rad) - math.sin(lat1_rad)*math.cos(lat2_rad)*math.cos(lon_delta_rad)
    theta = math.atan2(y, x)
    return math.degrees(theta)
