import argparse
from utils import get_aerial_lidar_road_geo_df


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Process arguments.')
    parser.add_argument('--input_lidar', type=str,
                        default='data/d13_route_40001001011/lidar/test_scene_all_raster_10_bridge.csv',
                        help='input rasterized lidar file with road points x, y, z in EPSG:6543 coordinate projection')
    parser.add_argument('--output_lidar', type=str,
                        default='data/d13_route_40001001011/lidar/test_scene_all_raster_10_bridge_latlon.csv',
                        help='output rasterized lidar file with road points lat, lon, z in EPSG:4326 '
                             'coordinate projection')

    args = parser.parse_args()
    input_lidar = args.input_lidar
    output_lidar = args.output_lidar

    gdf = get_aerial_lidar_road_geo_df(input_lidar, road_only=True)
    gdf['Latitude'] = gdf['geometry_y'].apply(lambda point: point.y)
    gdf['Longitude'] = gdf['geometry_y'].apply(lambda point: point.x)
    df = gdf[['Latitude', 'Longitude', 'Z']]
    df.to_csv(output_lidar, index=False)
