import numpy as np
from PIL import Image
from math import radians, cos, sin, asin, sqrt, atan2, degrees
import pickle

ROAD = 1
POLE = 2
IMAGE_WIDTH = 2748
IMAGE_HEIGHT = 2198
ASPECT_RATIO = IMAGE_WIDTH/IMAGE_HEIGHT


def consecutive(data, step_size=1):
    split_indices = np.where(np.diff(data) > step_size)[0]
    return split_indices, np.split(data, split_indices+1)


def split_into_lines(y_data, x_data):
    # find the indices of start of each new line in data
    split_indices = np.where(np.diff(y_data) == 1)[0]
    return np.split(y_data, split_indices+1), np.split(x_data, split_indices+1)


def get_data_from_image(input_image_name):
    input_image = Image.open(input_image_name)
    image_width = input_image.width
    image_height = input_image.height
    input_data = np.array(input_image)
    return image_width, image_height, input_data


def save_data_to_image(data, output_image_name):
    Image.fromarray(np.uint8(data), 'L').save(output_image_name)


def bearing_between_two_latlon_points(lat1, lon1, lat2, lon2, is_degree):
    lon_delta_rad = radians(lon2-lon1)
    lat1_rad = radians(lat1)
    lat2_rad = radians(lat2)
    y = sin(lon_delta_rad) * cos(lat2_rad)
    x = cos(lat1_rad)*sin(lat2_rad) - sin(lat1_rad)*cos(lat2_rad)*cos(lon_delta_rad)
    theta = atan2(y, x)
    if is_degree:
        return degrees(theta)
    else:
        return theta


def get_camera_latlon_and_bearing_for_image_from_mapping(mapping_df, mapped_image, is_degree=True):
    mapped_image_df = mapping_df[mapping_df['MAPPED_IMAGE'] == mapped_image]
    if len(mapped_image_df) != 1:
        # no camera location
        return None, None, None
    cam_lat = float(mapped_image_df.iloc[0]['LATITUDE'])
    cam_lon = float(mapped_image_df.iloc[0]['LONGITUDE'])
    # find the next camera lat/lon for computing bearing
    cam_lat2 = float(mapping_df.iloc[mapped_image_df.index + 1]['LATITUDE'])
    cam_lon2 = float(mapping_df.iloc[mapped_image_df.index + 1]['LONGITUDE'])
    # compute bearing
    cam_br = bearing_between_two_latlon_points(cam_lat, cam_lon, cam_lat2, cam_lon2, is_degree)
    return cam_lat, cam_lon, cam_br


# haversine distance formula between two points specified by their GPS coordinates
def haversine(lon1, lat1, geom):
    """
    Calculate the great circle distance between two points
    on the earth (specified in decimal degrees) in meter
    """
    lat2 = geom.y
    lon2 = geom.x
    # convert decimal degrees to radians
    lon1, lat1, lon2, lat2 = map(radians, [float(lon1), float(lat1), float(lon2), float(lat2)])
    # haversine formula
    dist_lon = lon2 - lon1
    dist_lat = lat2 - lat1
    a = sin(dist_lat / 2) ** 2 + cos(lat1) * cos(lat2) * sin(dist_lon / 2) ** 2
    return 6367000. * 2 * asin(sqrt(a))


def load_pickle_data(input_data_file):
    with open(input_data_file, 'rb') as f:
        data = pickle.load(f)[0]
    return data
