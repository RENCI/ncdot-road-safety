# common/utils.py
# This is a common module that contains constants and utilities for both data_processing
# and object_mapping modules

from math import radians, sin, cos, asin, sqrt

MAX_OBJ_DIST_FROM_CAM = 50


# haversine distance formula between two points specified by their GPS coordinates
def haversine(lon1, lat1, lon2, lat2):
    """
    Calculate the great circle distance between two points 
    on the earth (specified in decimal degrees) in meter
    """
    # convert decimal degrees to radians
    try:
        lon1, lat1, lon2, lat2 = map(radians, [float(lon1), float(lat1), float(lon2), float(lat2)])
        # haversine formula
        dist_lon = lon2 - lon1
        dist_lat = lat2 - lat1
        a = sin(dist_lat / 2) ** 2 + cos(lat1) * cos(lat2) * sin(dist_lon / 2) ** 2
        return 6367000. * 2 * asin(sqrt(a))
    except Exception as e:
        print(f'lon1: {lon1}, lat1: {lat1}, lon2: {lon2}, lat2: {lat2}')
        raise Exception(e)


def flatten_nested_list(nested_list):
    return [item for sublist in nested_list for item in (sublist if isinstance(sublist, list) else [sublist])]