import pandas as pd
import argparse
from data_processing.utils import LIDARClass


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Input/output arguments')
    parser.add_argument('--input_lidar_raw', type=str,
                        default='data/new_test_scene/new_test_scene_all_raster_10.csv',
                        help='input file that contains rasterized raw lidar points')
    parser.add_argument('--input_lidar_road_edges', type=str,
                        default='data/new_test_scene/new_test_scene_road_bounds_NEW.csv',
                        help='input file that contains road edge lidar points')
    parser.add_argument('--output_file', type=str,
                        default='data/new_test_scene/new_test_scene_all_raster_10_with_new_road_bounds.csv',
                        help='output path for 3D points to be corresponded with from 2D image points in pickle format')

    args = parser.parse_args()
    input_lidar_raw = args.input_lidar_raw
    input_lidar_road_edges = args.input_lidar_road_edges
    output_file = args.output_file

    df_raw = pd.read_csv(input_lidar_raw)
    df_road_edges = pd.read_csv(input_lidar_road_edges)
    df_road_edges['C'] = LIDARClass.ROAD.value
    merged_df = pd.merge(df_raw, df_road_edges, how='outer', on=['X', 'Y', 'Z', 'C'], indicator=True)
    merged_df['BOUND'] = merged_df['_merge'].apply(lambda x: 1 if x in ['right_only', 'both'] else 0)
    merged_df.drop(columns=['_merge'], inplace=True)
    merged_df.to_csv(output_file, index=False)
