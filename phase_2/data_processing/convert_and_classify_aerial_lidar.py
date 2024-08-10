import argparse
import os
import sys
import pandas as pd
from utils import get_aerial_lidar_road_geo_df
import matplotlib.pyplot as plt


def is_boundary(pt, pts, grid_spacing):
    x, y = pt
    left_neigh = pts[(pts[:, 0] < x) & (pts[:, 1] >= y - grid_spacing) & (pts[:, 1] <= y + grid_spacing)]
    right_neigh = pts[(pts[:, 0] > x) & (pts[:, 1] >= y - grid_spacing) & (pts[:, 1] <= y + grid_spacing)]
    if left_neigh.size == 0 or right_neigh.size == 0:
        return True
    else:
        return False


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
    if 'I' in idf.columns:
        sub_list.append('I')
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
    parser.add_argument('--input_lidar', type=str,
                        default='',
                        help='input rasterized lidar file with road points x, y, z in EPSG:6543 coordinate projection')
    parser.add_argument('--input_lidar_bound', type=str,
                        default='data/d13_route_40001001012/route_40001001012_raster_1ft_with_edges_sr.csv',
                        help='input lidar file with road edge/bound points x, y, z in EPSG:6543 coordinate projection')
    parser.add_argument('--output_lidar_boundary', type=str,
                        default='',
                        # default='data/new_test_scene/new_test_scene_all_raster_10_classified.csv',
                        help='output rasterized lidar file with road points classified as edge or not')
    parser.add_argument('--lidar_class_to_keep',
                        # default=['6', '11', '15'],
                        default=[],
                        help='filter lidar data to only keep desired classes; if it is empty, keep all classes')
    parser.add_argument('--output_latlon_lidar_basename', type=str,
                        default='data/d13_route_40001001012/route_40001001012_raster_1ft_road_bounds',
                        # default='data/d13_route_40001001011/lidar/route_40001001011_all',
                        help='output lidar file with road points lat, lon, z in EPSG:4326 coordinate projection')

    args = parser.parse_args()
    input_lidar = args.input_lidar
    input_lidar_bound = args.input_lidar_bound
    output_lidar_boundary = args.output_lidar_boundary
    output_latlon_lidar_basename = args.output_latlon_lidar_basename
    lidar_class_to_keep = args.lidar_class_to_keep

    if input_lidar:
        gdf = get_aerial_lidar_road_geo_df(input_lidar)
        if 'C' in gdf.columns:
            print(gdf.C.unique())

            if lidar_class_to_keep:
                gdf = gdf[gdf.C.isin(lidar_class_to_keep)]

        if output_lidar_boundary:
            points = gdf[['X', 'Y']].to_numpy()
            y_grid_sp = 5
            gdf['Boundary'] = gdf.apply(lambda row: is_boundary([row['X'], row['Y']], points, y_grid_sp), axis=1)
            df = gdf[['X', 'Y', 'Z', 'Boundary']]
            df.to_csv(output_lidar_boundary, index=False)
            # Plot result to verify
            plt.figure(figsize=(8, 8))
            plt.gca().invert_yaxis()
            # sub_df = df[df.Y > 735000]
            sub_df = df
            print(df.shape, sub_df.shape)
            bound_df = sub_df[sub_df.Boundary == True]
            plt.scatter(sub_df['X'], sub_df['Y'], s=1, c='b')
            plt.scatter(bound_df['X'], bound_df['Y'], s=2, c='r')
            plt.show()

    if input_lidar_bound:
        gdf_bound = get_aerial_lidar_road_geo_df(input_lidar_bound)
        gdf_bound = gdf_bound[gdf_bound.BOUND == 1]
        print(f'gdf_bound shape: {gdf_bound.shape}')

    if input_lidar and input_lidar_bound:
        # combine two lidar points with an added column to indicate whether it belongs to edge/bound or not
        gdf['BOUND'] = 0
        gdf_bound['BOUND'] = 1
        gdf_bound['I'] = 0
        combined_df = pd.concat([gdf, gdf_bound], ignore_index=True)
        combined_df = combined_df.drop(columns=['geometry_x', 'geometry_y'])
        combined_df.to_csv(f'{output_latlon_lidar_basename}.csv', index=False)
    elif input_lidar:
        # output latlon csv file
        output_latlon_from_geometry(gdf, 'geometry_y', f'{output_latlon_lidar_basename}_latlon.csv')
    elif input_lidar_bound:
        output_latlon_from_geometry(gdf_bound, 'geometry_y', f'{output_latlon_lidar_basename}_bounds_latlon.csv')
    sys.exit()
