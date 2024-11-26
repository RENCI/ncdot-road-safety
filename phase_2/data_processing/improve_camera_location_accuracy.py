import argparse
import pandas as pd
import numpy as np
from geopy.distance import geodesic


def interpolate_along_path(df, lat_col='LATITUDE', lon_col='LONGITUDE'):
    """
    Interpolates points at even intervals along the piecewise path defined by the original locations.

    Args:
        df (pd.DataFrame): DataFrame with LATITUDE and LONGITUDE columns.
        lat_col (str): Name of the latitude column.
        lon_col (str): Name of the longitude column.

    Returns:
        pd.DataFrame: DataFrame with interpolated points lying exactly on the path.
    """
    # Extract latitudes and longitudes as NumPy arrays
    lats = df[lat_col].to_numpy()
    lons = df[lon_col].to_numpy()

    # Calculate distances between consecutive points
    num_points = len(lats)
    distances = np.array([
        geodesic((lats[i], lons[i]), (lats[i + 1], lons[i + 1])).meters
        for i in range(num_points - 1)
    ])

    # Compute cumulative distances
    cumulative_distances = np.insert(np.cumsum(distances), 0, 0)

    # Total path length and interpolated distances
    total_distance = cumulative_distances[-1]
    spacing_m = total_distance / (num_points - 1)
    print(f'spacing for interpolation in feet: {spacing_m * 3.28084}')
    interpolated_distances = np.arange(0, total_distance + spacing_m, spacing_m)

    # Find the segment indices for each interpolated distance
    segment_indices = np.searchsorted(cumulative_distances, interpolated_distances, side='right') - 1

    # Clip segment indices to ensure they stay within bounds
    segment_indices = np.clip(segment_indices, 0, len(distances) - 1)

    # Get the start and end latitudes, longitudes, and distances for each segment
    segment_start_distances = cumulative_distances[segment_indices]
    segment_end_distances = cumulative_distances[segment_indices + 1]
    segment_start_lats = lats[segment_indices]
    segment_start_lons = lons[segment_indices]
    segment_end_lats = lats[segment_indices + 1]
    segment_end_lons = lons[segment_indices + 1]

    # Calculate interpolation proportion
    proportions = (interpolated_distances - segment_start_distances) / (
        segment_end_distances - segment_start_distances
    )

    # Interpolate latitude and longitude
    interpolated_lats = segment_start_lats + proportions * (segment_end_lats - segment_start_lats)
    interpolated_lons = segment_start_lons + proportions * (segment_end_lons - segment_start_lons)

    # Return results as a DataFrame
    return pd.DataFrame({lat_col: interpolated_lats, lon_col: interpolated_lons})


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Process arguments.')
    parser.add_argument('--input_file', type=str,
                        default='data/d13_route_40001001012/route_40001001012_input.csv',
                        help='input file name with path')
    parser.add_argument('--output_file', type=str,
                        default='data/d13_route_40001001012/route_40001001012_input_corrected.csv',
                        help='output file name with path')

    args = parser.parse_args()
    input_file = args.input_file
    output_file = args.output_file

    input_df = pd.read_csv(input_file)
    input_df[['LATITUDE', 'LONGITUDE']] = interpolate_along_path(input_df)
    input_df.to_csv(output_file, index=False)
    exit(0)
