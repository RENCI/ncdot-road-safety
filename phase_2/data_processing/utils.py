import numpy as np
from PIL import Image
from math import radians, cos, sin, asin, atan2, degrees, pi
import pickle
import pandas as pd
import geopandas as gpd
from shapely.geometry import Point
from enum import Enum


class SegmentationClass(Enum):
    # ROAD 1 and POLE 2 are classification code for old test route
    # ROAD = 1
    # POLE = 2
    # ROAD 0 and POLE 5 are classification code for new test route
    ROAD = 0
    POLE = 5
    BUILDING = 2
    SIDEWALK = 1
    SIGN = 7
    WALL = 3
    FENCE = 4


class LIDARClass(Enum):
    ROAD = 11
    BUILDING = 6
    POLE = 15
    GROUND = 2
    BRIDGE = 17
    LOW_VEG = 3
    MEDIUM_VEG = 4
    HIGH_VEG = 5


def add_lidar_x_y_from_lat_lon(df):
    """
    add X, Y columns representing LIDAR X, Y projection from LONGITUDE and LATITUDE columns in input df
    :param df: input dataframe that must include LONGITUDE and LATITUDE columns
    :return: df with added X, Y columns representing LIDAR X, Y projection converted from input LATITUDE and LONGITUDE
    """
    mapped_image_gdf = gpd.GeoDataFrame(df, geometry=gpd.points_from_xy(df.LONGITUDE, df.LATITUDE),
                                        crs='EPSG:4326')
    return mapped_image_gdf.geometry.to_crs(epsg=6543)


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


def get_image_resolution(input_image_name):
    with Image.open(input_image_name) as input_image:
        return input_image.width, input_image.height


def save_data_to_image(data, output_image_name):
    Image.fromarray(np.uint8(data), 'L').save(output_image_name)


def normalize(rad_angle, is_degree):
    """
    normalize rad_angle in radians to the range of (0, 2*pi) and convert it to degree as needed
    :param rad_angle: input angle in radians
    :param is_degree: whether to return normalized angle in degree or not
    :return: normalized angle
    """
    if rad_angle < 0:
        rad_angle += 2 * pi
    rad_angle = rad_angle % (2 * pi)
    if is_degree:
        return degrees(rad_angle)
    else:
        return rad_angle


def bearing_between_two_latlon_points(lat1, lon1, lat2, lon2, is_degree):
    lon_delta_rad = radians(lon2-lon1)
    lat1_rad = radians(lat1)
    lat2_rad = radians(lat2)
    y = sin(lon_delta_rad) * cos(lat2_rad)
    x = cos(lat1_rad)*sin(lat2_rad) - sin(lat1_rad)*cos(lat2_rad)*cos(lon_delta_rad)
    theta = atan2(y, x)
    # normalize angle to be between 0 and 360
    return normalize(theta, is_degree=is_degree)


def get_mapping_dataframe(mapping_file, route_id=''):
    mapping_df = pd.read_csv(mapping_file,
                             usecols=['ROUTEID', 'MAPPED_IMAGE', 'LATITUDE', 'LONGITUDE'], dtype=str)
    if route_id:
        mapping_df = mapping_df[mapping_df['ROUTEID'] == route_id]
    mapping_df.sort_values(by=['ROUTEID', 'MAPPED_IMAGE'], inplace=True, ignore_index=True)
    return mapping_df


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
        map_base_img2 = mapping_df.iloc[mapped_image_df.index - 1]['MAPPED_IMAGE']
        end_of_route = True
    else:
        cam_lat2 = float(next_row.iloc[0]['LATITUDE'])
        cam_lon2 = float(next_row.iloc[0]['LONGITUDE'])
        # compute bearing
        cam_br = bearing_between_two_latlon_points(cam_lat, cam_lon, cam_lat2, cam_lon2, is_degree)
        map_base_img2 = next_row.iloc[0]['MAPPED_IMAGE']
        end_of_route = False

    return cam_lat, cam_lon, cam_br, cam_lat2, cam_lon2, map_base_img2, end_of_route


def load_pickle_data(input_data_file):
    with open(input_data_file, 'rb') as f:
        data = pickle.load(f)[0]
    return data


def get_depth_data(loader, input_file):
    pfm = loader.load_pfm(input_file)
    # flip columns since they are inverse depth maps
    return np.flipud(pfm)


def get_depth_of_pixel(y, x, data, min_depth, max_depth, scaling=1):
    return (1 - (data[int(y + 0.5), int(x + 0.5)] - min_depth) / (max_depth - min_depth)) * scaling


def get_zoe_depth_data(image_name):
    with Image.open(image_name) as depth_img:
        return np.asarray(depth_img, dtype='uint32')


def get_zoe_depth_of_pixel(y, x, depth_data):
    # get depth of a pixel in feet
    return depth_data[y, x] * 3.28084 / 256.0


def get_aerial_lidar_road_geo_df(input_file):
    gdf = gpd.read_file(input_file)
    gdf.X = gdf.X.astype(float)
    gdf.Y = gdf.Y.astype(float)
    gdf.Z = gdf.Z.astype(float)
    if 'C' in gdf.columns:
        gdf.C = gdf.C.astype(int)
    if 'BOUND' in gdf.columns:
        gdf.BOUND = gdf.BOUND.astype(int)
    if 'EDGE' in gdf.columns:
        gdf.EDGE = gdf.EDGE.str.lower().map({'true': 1, 'false': 0})
        gdf = gdf.rename(columns={'EDGE': 'BOUND'})
    if 'Boundary' in gdf.columns:
        gdf.Boundary = gdf.Boundary.apply(lambda x: 1 if x == 'True' else 0)

    # Create a new geometry column with Point objects
    gdf.geometry = [Point(x, y, z) for x, y, z in zip(gdf['X'], gdf['Y'], gdf['Z'])]
    gdf.crs = 'epsg:6543'
    convert_geom_df = gdf.geometry.to_crs(epsg=4326)
    # convert_geom_df is added as a geometry_y column in lidar_df while the initial geometry column is
    # renamed as geometry_x
    gdf = gdf.merge(convert_geom_df, left_index=True, right_index=True)
    return gdf


def create_gdf_from_df(input_df, x_col_name='X', y_col_name='Y'):
    """
    create geographic dataframe in LIDAR coordinate system with EPSG:6543 from X, Y column in input dataframe
    :param input_df: input dataframe that must include x_col_name and y_col_name columns
    :param x_col_name: x column name with default value X
    :param y_col_name: y column name with default value Y
    :return: geographic dataframe that includes geometry column in LIDAR EPSG:6543 projection and projected
    geometry_y column in EPSG:4326 lat/lon projection
    """
    gdf = gpd.GeoDataFrame(input_df, geometry=gpd.points_from_xy(input_df[x_col_name], input_df[y_col_name]),
                           crs='EPSG:6543')
    geom_df = gdf.geometry.to_crs(epsg=4326)
    # geom_df is added as a geometry_y column in lidar_df while the initial geometry column is renamed as geometry_x
    return gdf.merge(geom_df, left_index=True, right_index=True)


def convert_xy_to_lat_lon(x, y):
    input_df = pd.DataFrame(data={'X': [x], 'Y': [y]})
    input_gdf = create_gdf_from_df(input_df)
    # calculate the bearing of each 3D point to the camera
    lat_lon_geom = input_gdf['geometry_y'].iloc[0]
    return lat_lon_geom.y, lat_lon_geom.x


def compute_match(x, y, series_x, series_y, grid=False):
    # compute match indices in (series_x, series_y) pairs based on which point in all points represented in
    # (series_x, series_y) pairs has minimal distance to point(x, y). If grid is set to True, grid-based matching
    # will be applied meaning only those values of series_x and series_y within a grid will be used for matching
    if grid is True:
        grid_th = 100
        match_df = pd.DataFrame({'series_x': series_x, 'series_y': series_y})
        match_df['distance_x'] = abs(match_df['series_x'] - x)
        match_df['distance_y'] = abs(match_df['series_y'] - y)
        max_grid_x, max_grid_y = max(match_df['distance_x']), max(match_df['distance_y'])
        grid_df = match_df[(match_df.distance_x < grid_th) & (match_df.distance_y < grid_th)]
        if len(grid_df) <= 0:
            # no possible for a match within the grid
            return [-1, max(max_grid_x, max_grid_y)]
        distances = (grid_df['series_x'] - x) ** 2 + (grid_df['series_y'] - y) ** 2
    else:
        distances = (series_x - x) ** 2 + (series_y - y) ** 2
    min_dist = np.min(distances)
    # min_idx = distances.idxmin()
    min_indices = np.where(distances == min_dist)[0]
    return [min_indices, min_dist]


def compute_match_3d(x, y, z, series_x, series_y, series_z):
    # compute match indices in (series_x, series_y, series_z) based on which point in all points represented in
    # (series_x, series_y, series_z) has minimal distance to point(x, y, z)

    distances = (series_x - x) ** 2 + (series_y - y) ** 2 + (series_z - z) ** 2
    min_idx = distances.idxmin()
    return [min_idx, distances[min_idx]]


def angle_between(v1, v2):
    """Calculate the angle in radians between two vectors."""
    return degrees(np.arccos(np.clip(np.dot(v1, v2) / (np.linalg.norm(v1) * np.linalg.norm(v2)), -1.0, 1.0)))
