import argparse
import sys
import os
import pandas as pd
from utils import get_image_resolution


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Process arguments.')
    parser.add_argument('--input_file', type=str,
                        default='/projects/ncdot/secondary_road/output/d13/mapped_2lane_sr_images_d13_updated.csv',
                        help='input file name with path')

    args = parser.parse_args()
    input_file = args.input_file

    input_df = pd.read_csv(input_file)
    input_df.sort_values(by=['MAPPED_IMAGE'], inplace=True)
    input_df.reset_index(drop=True, inplace=True)
    input_df['ROUTEID_diff'] = input_df['ROUTEID'].diff()
    input_df['MILE_diff'] = input_df['MILE_POST'].diff()
    route_df = input_df[input_df['ROUTEID_diff'] != 0]
    duplicated_routeids = route_df[route_df.duplicated(subset=['ROUTEID'], keep=False)]
    print(f'total routes: {len(input_df.ROUTEID.unique())}')
    print(f"duplicated/interrupted routes along the driving route: {duplicated_routeids[['ROUTEID', 'MAPPED_IMAGE']]}")
    gap_within_route = input_df[(input_df.ROUTEID_diff == 0) & (input_df.MILE_diff > 0.012)]
    print(f'there are {len(gap_within_route)} instances where gaps within the same route occur. The largest gap '
          f'distance is {gap_within_route.MILE_diff.abs().max()}')
    adjacent_routes = route_df[route_df.MILE_diff.abs() < 0.002]
    sys.exit(0)
