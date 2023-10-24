import argparse
import os
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
    get lat and lon from dataframe with geometry column. It assumes the input dataframe has "Z" and "Boundary" columns
    and "Boundary" column is a boolean type
    :param idf: input dataframe
    :param geom_col: geometry column in input dataframe
    :param output_file_name: output file name for the latlon output dataframe
    :return:
    """
    idf['Latitude'] = idf[geom_col].apply(lambda point: point.y)
    idf['Longitude'] = idf[geom_col].apply(lambda point: point.x)
    out_df = idf[['Latitude', 'Longitude', 'Z', 'Boundary']]
    out_df.to_csv(output_file_name, index=False)
    base, ext = os.path.splitext(output_file_name)
    out_df[out_df.Boundary == True].drop(columns=['Boundary']).to_csv(
        f'{base}_boundary{ext}', index=False)
    out_df[out_df.Boundary == False].drop(columns=['Boundary']).to_csv(
        f'{base}_internal{ext}', index=False)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Process arguments.')
    parser.add_argument('--input_lidar', type=str,
                        default='data/d13_route_40001001011/lidar/route_40001001011_road_raster_10.csv',
                        help='input rasterized lidar file with road points x, y, z in EPSG:6543 coordinate projection')
    parser.add_argument('--output_lidar', type=str,
                        default='data/d13_route_40001001011/lidar/route_40001001011_road_raster_10_classified.csv',
                        help='output rasterized lidar file with road points classified as edge or not')
    parser.add_argument('--show_plot', action="store_true", help='show plot for verification')
    parser.add_argument('--output_latlon_lidar', type=str,
                        default='data/d13_route_40001001011/lidar/route_40001001011_road_raster_10_latlon.csv',
                        help='output rasterized lidar file with road points lat, lon, z in EPSG:4326 '
                             'coordinate projection')

    args = parser.parse_args()
    input_lidar = args.input_lidar
    output_lidar = args.output_lidar
    output_latlon_lidar = args.output_latlon_lidar
    show_plot = args.show_plot

    gdf = get_aerial_lidar_road_geo_df(input_lidar, road_only=True)
    y_grid_sp = 5
    points = gdf[['X', 'Y']].to_numpy()
    gdf['Boundary'] = gdf.apply(lambda row: is_boundary([row['X'], row['Y']], points, y_grid_sp), axis=1)
    df = gdf[['X', 'Y', 'Z', 'Boundary']]
    df.to_csv(output_lidar, index=False)
    if show_plot:
        # Plot result to verify
        plt.figure(figsize=(8, 8))
        plt.gca().invert_yaxis()
        sub_df = df[df.Y > 735000]
        print(df.shape, sub_df.shape)
        bound_df = sub_df[sub_df.Boundary == True]
        plt.scatter(sub_df['X'], sub_df['Y'], s=1, c='b')
        plt.scatter(bound_df['X'], bound_df['Y'], s=2, c='r')
        plt.show()
    output_latlon_from_geometry(gdf, 'geometry_y', output_latlon_lidar)
