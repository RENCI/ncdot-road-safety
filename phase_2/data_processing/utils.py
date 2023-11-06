import numpy as np
from PIL import Image
from math import radians, cos, sin, asin, sqrt, atan2, degrees, pi
import pickle
import geopandas as gpd
from shapely.geometry import Point

ROAD = 1
POLE = 2
IMAGE_WIDTH = 2748
IMAGE_HEIGHT = 2198
ASPECT_RATIO = IMAGE_WIDTH/IMAGE_HEIGHT


def next_location(lat, lon, bearing, distance, is_degree=True):
    # Convert degrees to radians
    if is_degree:
        lat = radians(lat)
        lon = radians(lon)
        bearing = radians(bearing)

    # Earth's radius in meters
    radius = 6378137

    # Calculate the next latitude and longitude
    lat2 = asin(sin(lat) * cos(distance / radius) + cos(lat) * sin(distance / radius) * cos(bearing))
    lon2 = lon + atan2(sin(bearing) * sin(distance / radius) * cos(lat),
                            cos(distance / radius) - sin(lat) * sin(lat2))

    if is_degree:
        # Convert radians back to degrees
        lat2 = degrees(lat2)
        lon2 = degrees(lon2)

    return lat2, lon2


def get_next_road_index(input_idx, input_df, input_df_bearing_field):
    # find the next lidar road edge vertex index on the same side of the road as nearest_idx
    if input_idx == 0:
        next_idx = input_idx + 1
    elif input_idx == len(input_df) - 1:
        next_idx = input_idx - 1
    else:
        next_idx = input_idx - 1 if abs(input_df.iloc[input_idx - 1][input_df_bearing_field]) < \
                                    abs(input_df.iloc[input_idx + 1][input_df_bearing_field]) else input_idx + 1
    return next_idx


def consecutive(data, step_size=1):
    split_indices = np.where(np.diff(data) > step_size)[0]
    return split_indices, np.split(data, split_indices+1)


def split_into_lines(y_data, x_data):
    # find the indices of start of each new line in data
    split_indices = np.where(np.diff(y_data) == 1)[0]
    return np.split(y_data, split_indices+1), np.split(x_data, split_indices+1)


def get_data_from_image(input_image_name):
    with Image.open(input_image_name) as input_image:
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
    # normalize angle to be between 0 and 360
    if theta < 0:
        theta += 2 * pi
    theta = theta % (2 * pi)
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
    next_row = mapping_df.iloc[mapped_image_df.index + 1]
    if next_row.iloc[0]['ROUTEID'] != mapped_image_df.iloc[0]['ROUTEID']:
        # this image is the end of the route, use the previous camera location to compute bearing instead
        cam_lat2 = float(mapping_df.iloc[mapped_image_df.index - 1]['LATITUDE'])
        cam_lon2 = float(mapping_df.iloc[mapped_image_df.index - 1]['LONGITUDE'])
        # compute bearing
        cam_br = bearing_between_two_latlon_points(cam_lat2, cam_lon2, cam_lat, cam_lon, is_degree)
        # compute next interpolated camera location based on cam_br
        cam_lat2, cam_lon2 = next_location(cam_lat, cam_lon, cam_br, 8, is_degree)
        end_of_route = True
    else:
        cam_lat2 = float(next_row.iloc[0]['LATITUDE'])
        cam_lon2 = float(next_row.iloc[0]['LONGITUDE'])
        # compute bearing
        cam_br = bearing_between_two_latlon_points(cam_lat, cam_lon, cam_lat2, cam_lon2, is_degree)
        end_of_route = False

    return cam_lat, cam_lon, cam_br, cam_lat2, cam_lon2, end_of_route


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


def get_depth_data(loader, input_file):
    pfm = loader.load_pfm(input_file)
    # flip columns since they are inverse depth maps
    return np.flipud(pfm)


def get_depth_of_pixel(y, x, pfm_data, min_depth, max_depth, scaling=1):
    return (1 - (pfm_data[int(y + 0.5), int(x + 0.5)] - min_depth) / (max_depth - min_depth)) * scaling


def get_zoe_depth_data(image_name):
    with Image.open(image_name) as depth_img:
        return np.asarray(depth_img, dtype='uint32')


def get_zoe_depth_of_pixel(y, x, depth_data):
    # get depth of a pixel in feet
    return depth_data[y, x] * 3.28084 / 256.0


def get_aerial_lidar_road_geo_df(input_file, road_only=True):
    gdf = gpd.read_file(input_file)
    gdf.X = gdf.X.astype(float)
    gdf.Y = gdf.Y.astype(float)
    gdf.Z = gdf.Z.astype(float)
    if 'C' in gdf.columns:
        gdf.C = gdf.C.astype(int)
        if road_only:
            # 13 is LIDAR classification code for road
            gdf = gdf[gdf['C'] == 13]
    if 'Boundary' in gdf.columns:
        gdf.Boundary = gdf.Boundary.apply(lambda x: 1 if x == 'True' else 0)
    # Create a new geometry column with Point objects
    gdf.geometry = [Point(x, y, z) for x, y, z in zip(gdf['X'], gdf['Y'], gdf['Z'])]
    gdf.crs = 'epsg:6543'
    convert_geom_df = gdf.geometry.to_crs(epsg=4326)
    # geom_df is added as a geometry_y column in lidar_df while the initial geometry column is renamed as geometry_x
    gdf = gdf.merge(convert_geom_df, left_index=True, right_index=True)
    return gdf


def compute_match(x, y, series_x, series_y):
    # compute match indices in (series_x, series_y) pairs based on which point in all points represented in
    # (series_x, series_y) pairs has minimal distance to point(x, y)
    distances = (series_x - x) ** 2 + (series_y - y) ** 2
    min_idx = distances.idxmin()
    return [min_idx, distances[min_idx]]


def compute_match_3d(x, y, z, series_x, series_y, series_z):
    # compute match indices in (series_x, series_y, series_z) based on which point in all points represented in
    # (series_x, series_y, series_z) has minimal distance to point(x, y, z)

    distances = (series_x - x) ** 2 + (series_y - y) ** 2 + (series_z - z) ** 2
    min_idx = distances.idxmin()
    return [min_idx, distances[min_idx]]
