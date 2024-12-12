import numpy as np
import time
from PIL import Image
from math import radians, cos, sin, asin, atan2, degrees
import pickle
import pandas as pd
import geopandas as gpd
from shapely.geometry import Point
from enum import Enum
from scipy.spatial.distance import cdist


METER_TO_FEET = 3.28054

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


class ROADSIDE(Enum):
    LEFT = 0
    RIGHT = 1


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
    normalize rad_angle in radians to the range of (0, 2*pi) and convert it to degree if needed.
    Supports both scalar and vectorized inputs using numpy
    :param rad_angle: input angle in radians
    :param is_degree: whether to return normalized angle in degree or not
    :return: normalized angle
    """
    rad_angle = np.mod(rad_angle + 2 * np.pi, 2 * np.pi)  # Ensure the angle is within 0 to 2*pi range
    if is_degree:
        return np.degrees(rad_angle)
    else:
        return rad_angle


def bearing_between_two_latlon_points(lat1, lon1, lat2, lon2, is_degree):
    """
    Calculate the bearing between two points on the Earth using their latitude and longitude.
    Supports both scalar and vectorized inputs using NumPy.
    :param lat1: Latitude of the first point (in degrees)
    :param lon1: Longitude of the first point (in degrees)
    :param lat2: Latitude of the second point (in degrees)
    :param lon2: Longitude of the second point (in degrees)
    :param is_degree: Whether to return the bearing in degrees (True) or radians (False)
    :return: The bearing from the first point to the second, either in degrees or radians
    """
    lon_delta_rad = np.radians(lon2-lon1)
    lat1_rad = np.radians(lat1)
    lat2_rad = np.radians(lat2)
    y = np.sin(lon_delta_rad) * np.cos(lat2_rad)
    x = np.cos(lat1_rad) * np.sin(lat2_rad) - np.sin(lat1_rad) * np.cos(lat2_rad) * np.cos(lon_delta_rad)
    theta = np.atan2(y, x)
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
        cam_lat2 = float(mapping_df.iloc[mapped_image_df.index - 1].iloc[0]['LATITUDE'])
        cam_lon2 = float(mapping_df.iloc[mapped_image_df.index - 1].iloc[0]['LONGITUDE'])
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
    return depth_data[y, x] * METER_TO_FEET / 256.0


def get_aerial_lidar_road_geo_df(input_file):
    t1 = time.time()
    gdf = gpd.read_file(input_file, engine='pyogrio')
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
    if 'SIDE' in gdf.columns:
        gdf['SIDE'] = gdf['SIDE'].astype(int)
    # Create a new geometry column with Point objects
    geom_series = gpd.GeoSeries([Point(x, y, z) for x, y, z in zip(gdf['X'], gdf['Y'], gdf['Z'])], crs=6543)
    convert_geom_series = geom_series.to_crs(4326)
    gdf['geometry_x'] = geom_series
    gdf['geometry_y'] = convert_geom_series
    print(f'time taken to load the whole lidar data with geometry coordinate conversion: {time.time() - t1}s')
    return gdf


def create_df_from_lidar_points(input_points, input_cols):
    df = pd.DataFrame(data=input_points, columns=input_cols)

    if 'BOUND' in input_cols:
        df['BOUND'] = df['BOUND'].astype(int)

    df['X'] = df['X'].astype(float)
    df['Y'] = df['Y'].astype(float)
    df['Z'] = df['Z'].astype(float)
    if 'C' in input_cols:
        df['C'] = df['C'].astype(int)
    return df


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


def compute_match(x, y, series_x, series_y):
    # compute match indices in (series_x, series_y) pairs based on which point in all points represented in
    # (series_x, series_y) pairs has minimal distance to point(x, y)
    distances = (series_x - x) ** 2 + (series_y - y) ** 2
    min_dist = np.min(distances)
    # min_idx = distances.idxmin()
    min_indices = np.where(distances == min_dist)[0]
    return min_indices, min_dist


def angle_between(v1, v2):
    """Calculate the angle in radians between two vectors."""
    return degrees(np.arccos(np.clip(np.dot(v1, v2) / (np.linalg.norm(v1) * np.linalg.norm(v2)), -1.0, 1.0)))


def classify_road_edge_points_to_sides(middle_axis, middle_centroid, edge_points):
    """
    Classify each road edge point as either left or right side based on the middle axis and middle_centroid point.
    """
    return np.array([
        ROADSIDE.RIGHT.value if np.cross(middle_axis, point - middle_centroid) > 0 else ROADSIDE.LEFT.value
        for point in edge_points])


# classify points (e.g., LIDAR points or road edge segmentation boundary points) into left or right sides
# based on closest centerline segment (e.g., camera centerline segment)
def classify_points_base_on_centerline(points, cl_df):
    # Find the closest centerline points to the input points
    centerline_points = cl_df[['x', 'y']].values
    # Calculate pairwise distances between input points and centerline points
    distances = cdist(points, centerline_points)
    # Find the closest centerline point for each input point
    closest_idx = np.argmin(distances, axis=1)

    # Get idx1 and idx2 arrays for the segments
    # If the closest point is the first centerline point, use its next point to create centerline segment; otherwise,
    # use its previous point to create centerline segment
    idx1_ary = np.where(closest_idx == 0, closest_idx, closest_idx - 1)
    idx2_ary = np.where(closest_idx == 0, closest_idx + 1, closest_idx)

    # Get the corresponding p1 and p2 points for each segment
    p1 = centerline_points[idx1_ary]
    p2 = centerline_points[idx2_ary]
    # Calculate segment vectors (p2 - p1) and point vectors (points - p1)
    segment_vec = p2 - p1
    point_vec = points - p1
    # Compute the cross product between the segment vectors and the point vectors
    cross_product = np.cross(segment_vec, point_vec)
    # Classify based on the cross product (left or right)
    classification = np.where(cross_product > 0, ROADSIDE.LEFT.value, ROADSIDE.RIGHT.value)
    return classification


def get_set_minute_sub_path(image_name):
    set_str = image_name[:3]
    hour = image_name[3:5]
    minute = image_name[5:7]
    if hour not in ['00', '01', '02']:
        print(f"{image_name}: hour in the image base name must be 00 or 01 or 02")
        return set_str, None
    if int(minute) > 59:
        print(f"{image_name}: minute in the image base name must be less than 60")
        return set_str, None
    if hour == '00':
        # strip prefix 0 from minute if any
        minute_str = str(int(minute))
    else:  # hour == '01'
        minute_str = str(int(minute) + int(hour) * 60)
    return set_str, minute_str
