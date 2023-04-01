import argparse
import geopandas as gpd
import pickle
from utils import haversine


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Process arguments.')
    parser.add_argument('--input_lidar_shp_with_path', type=str,
                        default='/home/hongyi/Downloads/NCRouteArcs_and_LiDAR_Road_Edge/RoadEdge_40001001011_vertices.shp',
                        help='input shp file that contains road x, y, z vertices from lidar')
    parser.add_argument('--output_file', type=str,
                        default='/home/hongyi/ncdot-road-safety/phase_2/data_processing/data/d13_route_40001001011/'
                                'oneformer/output/input_3d.pkl',
                        help='output path for 3D points to be corresponded with from 2D image points in pickle format')
    parser.add_argument('--camera_loc', type=str,
                        default=[35.7137581, -82.7346679],
                        help='camera loc to extract lidar vertices within a set threshold distance from')
    parser.add_argument('--distance_threshold', type=str,
                        default=385,
                        help='distance threshold in meter to filter out lidar vertices')

    args = parser.parse_args()
    input_lidar_shp_with_path = args.input_lidar_shp_with_path
    output_file = args.output_file
    clat, clon = args.camera_loc
    distance_threshold = args.distance_threshold

    # read shape file
    lidar_df = gpd.read_file(input_lidar_shp_with_path)
    # lidar_df should have columns Id, ORIG_FID, POINT_X, POINT_Y, POINT_Z, and geometry where geometry is
    # a point geometry, e.g., POINT Z (891488.760 734099.780 2018.620)
    # print(lidar_df.head())
    # total_bounds show minx, miny, maxx, maxy bounds of all geometry points
    # print(lidar_df.total_bounds)
    # convert lidar_df projection to WGS84 lat/lon CRS
    geom_df = lidar_df.geometry.to_crs(epsg=4326)
    # geom_df is added as a geometry_y column in lidar_df while the initial geometry column is renamed as geometry_x
    lidar_df = lidar_df.merge(geom_df, left_index=True, right_index=True)
    lidar_df['distance'] = lidar_df.apply(lambda row: haversine(clon, clat, row['geometry_y']), axis=1)
    print(lidar_df.shape)
    lidar_df = lidar_df[lidar_df['distance'] < distance_threshold]
    print(lidar_df.shape)
    lidar_df = lidar_df.drop(columns = ['Id', 'ORIG_FID', 'geometry_y', 'geometry_x', 'distance'])
    vertices = [lidar_df.to_numpy()]
    with open(output_file, 'wb') as f:
        pickle.dump(vertices, f)
