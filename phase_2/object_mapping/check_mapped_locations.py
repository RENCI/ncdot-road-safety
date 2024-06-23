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
from data_processing.utils import get_aerial_lidar_road_geo_df, LIDARClass
from common.utils import haversine


def compute_min_distance(ilon, ilat, lon_lat_geom_series):
    lon_lat_df = pd.DataFrame(lon_lat_geom_series)
    lon_lat_df['DISTANCE'] = lon_lat_df.apply(lambda row: haversine(ilon, ilat,
                                                                    row['geometry_y'].x, row['geometry_y'].y), axis=1)
    return lon_lat_df['DISTANCE'].min() * 3.28084


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Process arguments.')
    parser.add_argument('--geotag_file', type=str,
                        default='../data_processing/data/new_test_scene/full_route_test/'
                                'test_mapping_output_further_clustering.csv',
                        help='input geotagged pole file name with path')
    parser.add_argument('--input_lidar_with_path', type=str,
                        default='../data_processing/data/new_test_scene/new_test_scene_all_lidar_with_road_bounds.csv',
                        help='input file that contains road x, y, z vertices from lidar')
    parser.add_argument('--threshold_to_road', type=int, default=5,
                        help='distance threshold in feet of geotagged pole to road edge to filter out geotagged pole '
                             'smaller than the threshold in geotag_file input')
    parser.add_argument('--output_geotag_file', type=str,
                        default='../data_processing/data/new_test_scene/full_route_test/'
                                'test_mapping_output_processed.csv',
                        help='output geotagged pole file name with path')

    args = parser.parse_args()
    geotag_file = args.geotag_file
    input_lidar_with_path = args.input_lidar_with_path
    threshold_to_road = args.threshold_to_road
    output_geotag_file = args.output_geotag_file

    ldf = get_aerial_lidar_road_geo_df(input_lidar_with_path)
    ldf = ldf[(ldf.C == LIDARClass.ROAD.value) & (ldf.BOUND == 1)]
    geotag_df = pd.read_csv(geotag_file, dtype=str)
    geotag_df['DISTANCE'] = geotag_df.apply(lambda row: compute_min_distance(row['lon'], row['lat'],
                                                                             ldf['geometry_y']), axis=1)
    print(f'geotag_df before filtering: {geotag_df}')
    geotag_df = geotag_df[geotag_df.DISTANCE > threshold_to_road]
    print(f'geotag_df shape after filtering: {geotag_df.shape}')
    geotag_df.drop(columns=['DISTANCE'], inplace=True)
    geotag_df.to_csv(output_geotag_file, index=False)
    sys.exit(0)
