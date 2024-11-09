########################################
# This module checks the geotagged pole location output from object_mapping.py against the LIDAR road edge vertices
# to filter out those geotagged pole locations that are too close to the road edge. This post-processing is needed
# since when poles are very close to one another, object mapping module may use different poles close by appearing in
# consecutive images to compute intersection of view-rays for pole geotagging treating different poles close by as
# the same pole, which would result in a wrong intersection location which may be too close to the road edges
########################################
import sys
import argparse
import pandas as pd
import numpy as np
from data_processing.utils import get_aerial_lidar_road_geo_df, LIDARClass, add_lidar_x_y_from_lat_lon
from scipy.spatial import KDTree


def compute_min_distance(in_row, in_tree):
    input_x = in_row['geometry'].x
    input_y = in_row['geometry'].y
    dist, _ = in_tree.query([input_x, input_y])
    return dist


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Process arguments.')
    parser.add_argument('--geotag_file', type=str,
                        default='../data_processing/data/d13_route_40001001012/'
                                'route_40001001012_mapping_output_further_clustering.csv',
                        help='input geotagged pole file name with path')
    parser.add_argument('--input_lidar_with_path', type=str,
                        default='../data_processing/data/d13_route_40001001012/'
                                'route_40001001012_voxel_raster_1ft_with_edges_normalized_sr_sides.csv',
                        help='input file that contains road x, y, z vertices from lidar')
    parser.add_argument('--threshold_to_road', type=int, default=5,
                        help='distance threshold in feet of geotagged pole to road edge to filter out geotagged pole '
                             'smaller than the threshold in geotag_file input')
    parser.add_argument('--output_geotag_file', type=str,
                        default='../data_processing/data/d13_route_40001001012/'
                                'route_40001001012_mapping_output_processed.csv',
                        help='output geotagged pole file name with path')

    args = parser.parse_args()
    geotag_file = args.geotag_file
    input_lidar_with_path = args.input_lidar_with_path
    threshold_to_road = args.threshold_to_road
    output_geotag_file = args.output_geotag_file

    ldf = get_aerial_lidar_road_geo_df(input_lidar_with_path)
    print(f'ldf shape: {ldf.shape}')
    ldf = ldf[ldf.C == LIDARClass.ROAD.value]
    print(f'ldf road shape: {ldf.shape}')
    geotag_df = pd.read_csv(geotag_file)
    geotag_df.rename(columns={'lat': 'LATITUDE', 'lon': 'LONGITUDE'}, inplace=True)
    geotag_df['geometry'] = add_lidar_x_y_from_lat_lon(geotag_df)

    lidar_tree = KDTree(np.array(ldf[['X', 'Y']]))
    geotag_df['DISTANCE'] = geotag_df.apply(lambda row: compute_min_distance(row, lidar_tree), axis=1)
    print(f'geotag_df before filtering: {geotag_df}')
    geotag_df = geotag_df[geotag_df.DISTANCE > threshold_to_road]
    print(f'geotag_df shape after filtering: {geotag_df.shape}')
    geotag_df.drop(columns=['DISTANCE'], inplace=True)
    geotag_df.to_csv(output_geotag_file, index=False)
    sys.exit(0)
