import argparse
import os
import numpy as np
import pandas as pd
from utils import (classify_points_base_on_centerline,
                   get_aerial_lidar_road_geo_df, get_mapping_dataframe, add_lidar_x_y_from_lat_lon)


def output_latlon_from_geometry(idf, geom_col, output_file_name):
    """
    get lat and lon from dataframe with geometry column. It assumes the input dataframe has "Z" column
    and "Boundary" column is a boolean type
    :param idf: input dataframe
    :param geom_col: geometry column in input dataframe
    :param output_file_name: output file name for the latlon output dataframe
    :return:
    """
    idf['Latitude'] = idf[geom_col].apply(lambda point: point.y)
    idf['Longitude'] = idf[geom_col].apply(lambda point: point.x)
    sub_list = ['Latitude', 'Longitude', 'Z', 'X', 'Y']
    if 'C' in idf.columns:
        sub_list.append('C')
    if 'SIDE' in idf.columns:
        sub_list.append('SIDE')
    if 'Boundary' in idf.columns:
        sub_list.append('Boundary')
    out_df = idf[sub_list]
    out_df.to_csv(output_file_name, index=False)
    if 'Boundary' in idf.columns:
        base, ext = os.path.splitext(output_file_name)
        out_df[out_df.Boundary == True].drop(columns=['Boundary']).to_csv(
            f'{base}_boundary{ext}', index=False)
        out_df[out_df.Boundary == False].drop(columns=['Boundary']).to_csv(
            f'{base}_internal{ext}', index=False)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Process arguments.')
    parser.add_argument('--input_lidar_with_bound', type=str,
                        default='data/d13_route_40001001012/route_40001001012_voxel_raster_1ft_with_edges_normalized_sr.csv',
                        help='input lidar file with road edge/bound points x, y, z in EPSG:6543 coordinate projection')
    parser.add_argument('--input_sensor_mapping_file', type=str,
                        default='data/d13_route_40001001011/other/mapped_2lane_sr_images_d13.csv',
                        help='input csv file that includes mapped camera image lat/lon info')
    parser.add_argument('--route_id', default='40001001012', help='input route id for processed data')
    parser.add_argument('--lidar_class_to_keep',
                        # default=['6', '11', '15'],
                        default=[],
                        help='filter lidar data to only keep desired classes; if it is empty, keep all classes')
    parser.add_argument('--output_latlon_lidar_basename', type=str,
                        default='',
                        # default='data/d13_route_40001001012/route_40001001012_voxel_raster_1ft_with_edges_bounds',
                        help='output lidar file with road points lat, lon, z in EPSG:4326 coordinate projection')

    args = parser.parse_args()
    input_lidar_with_bound = args.input_lidar_with_bound
    route_id = args.route_id
    input_sensor_mapping_file = args.input_sensor_mapping_file
    output_latlon_lidar_basename = args.output_latlon_lidar_basename
    lidar_class_to_keep = args.lidar_class_to_keep

    gdf_with_bound = get_aerial_lidar_road_geo_df(input_lidar_with_bound)
    if 'C' in gdf_with_bound.columns and lidar_class_to_keep:
        print(gdf_with_bound.C.unique())
        gdf_with_bound = gdf_with_bound[gdf_with_bound.C.isin(lidar_class_to_keep)]
    gdf_bound = gdf_with_bound[gdf_with_bound.BOUND == 1]
    print(f'gdf_bound shape: {gdf_bound.shape}')

    if input_sensor_mapping_file:
        map_df = get_mapping_dataframe(input_sensor_mapping_file, route_id=route_id)
        cam_geom_series = add_lidar_x_y_from_lat_lon(map_df)
        cam_geom_df = pd.DataFrame({
            'x': cam_geom_series.apply(lambda p: p.x),
            'y': cam_geom_series.apply(lambda p: p.y)
        })
        # Build a KDTree for fast nearest neighbor search
        camline_points = np.vstack([cam_geom_df['x'].values, cam_geom_df['y'].values]).T

        mask = gdf_with_bound['BOUND'] == 1
        re_points = gdf_with_bound.loc[mask, ['X', 'Y']].values  # Extract X, Y as a NumPy array
        classified_sides = classify_points_base_on_centerline(re_points, cam_geom_df)
        gdf_with_bound.loc[mask, 'SIDE'] = classified_sides
        gdf_with_bound.loc[~mask, 'SIDE'] = -1
        gdf_with_bound.drop(columns=['geometry_x', 'geometry_y'], inplace=True)
        gdf_with_bound['SIDE'] = gdf_with_bound.SIDE.astype(int)
        gdf_with_bound.to_csv(f'{os.path.splitext(input_lidar_with_bound)[0]}_sides.csv', index=False)

    if output_latlon_lidar_basename:
        output_latlon_from_geometry(gdf_with_bound[gdf_with_bound.BOUND == 1].copy(), 'geometry_y',
                                    f'{output_latlon_lidar_basename}_bounds_latlon.csv')
    exit()
