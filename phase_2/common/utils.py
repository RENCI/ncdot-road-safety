# common/utils.py
# This is a common module that contains constants and utilities for both data_processing
# and object_mapping modules

import numpy as np

MAX_OBJ_DIST_FROM_CAM = 50


# haversine distance formula between two points specified by their GPS coordinates
# supporting both scalar and vectorized inputs using numpy
def haversine(lon1, lat1, lon2, lat2):
    """
    Calculate the great circle distance between two points 
    on the earth (specified in decimal degrees) in meter
    """
    # convert decimal degrees to radians
    lon1, lat1, lon2, lat2 = map(np.radians, [lon1, lat1, lon2, lat2])
    # haversine formula
    dist_lon = lon2 - lon1
    dist_lat = lat2 - lat1
    a = np.sin(dist_lat / 2) ** 2 + np.cos(lat1) * np.cos(lat2) * np.sin(dist_lon / 2) ** 2
    # Earth's radius in meters (mean radius = 6,367 km)
    return 6367000. * 2 * np.asin(np.sqrt(a))


def flatten_nested_list(nested_list):
    return [item for sublist in nested_list for item in (sublist if isinstance(sublist, list) else [sublist])]