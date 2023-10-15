import argparse
import geopandas as gpd
import pickle

from utils import haversine, bearing_between_two_latlon_points, get_next_road_index
import math


def get_lidar_data_from_shp(lidar_shp_file_path):
    # read shape file
    df = gpd.read_file(lidar_shp_file_path)
    # lidar_df should have columns Id, ORIG_FID, POINT_X, POINT_Y, POINT_Z, and geometry where geometry is
    # a point geometry, e.g., POINT Z (891488.760 734099.780 2018.620)
    # print(lidar_df.head())
    # total_bounds show minx, miny, maxx, maxy bounds of all geometry points
    # print(lidar_df.total_bounds)
    # convert lidar_df projection to WGS84 lat/lon CRS
    geom_df = df.geometry.to_crs(epsg=4326)
    # geom_df is added as a geometry_y column in lidar_df while the initial geometry column is renamed as geometry_x
    return df.merge(geom_df, left_index=True, right_index=True)


def extract_lidar_3d_points_for_camera(df, cam_loc, next_cam_loc, dist_th=190, end_of_route=False):
    clat, clon = cam_loc
    next_clat, next_clon = next_cam_loc
    df['distance'] = df.apply(lambda row: haversine(clon, clat, row['geometry_y']), axis=1)
    cam_bearing = bearing_between_two_latlon_points(clat, clon, next_clat, next_clon, is_degree=False)
    df['bearing_diff'] = df.apply(lambda row: abs(cam_bearing - bearing_between_two_latlon_points(
        clat, clon, row['geometry_y'].y, row['geometry_y'].x, is_degree=False)), axis=1)
    print(df.shape)
    if end_of_route:
        # use lidar road edge as camera bearing direction instead since next_cam_loc is interpolated and does not
        # accurately reflect camera bearing direction
        lidx = df['distance'].idxmin()
        nidx = get_next_road_index(lidx, df, 'bearing_diff')
        cam_bearing = bearing_between_two_latlon_points(df.iloc[lidx]['geometry_y'].y,
                                                        df.iloc[lidx]['geometry_y'].x,
                                                        df.iloc[nidx]['geometry_y'].y,
                                                        df.iloc[nidx]['geometry_y'].x,
                                                        is_degree=False)
        df['bearing_diff'] = df.apply(lambda row: abs(cam_bearing - bearing_between_two_latlon_points(
            clat, clon, row['geometry_y'].y, row['geometry_y'].x, is_degree=False)), axis=1)
    df = df[(df['distance'] < dist_th) & (df['bearing_diff'] < math.pi / 3)]
    print(df.shape)
    if 'X' in df.columns:
        df = df[['X', 'Y', 'Z']]
    else:
        df = df[['POINT_X', 'POINT_Y', 'POINT_Z']]
    return [df.to_numpy()], cam_bearing


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Process arguments.')
    parser.add_argument('--input_lidar_shp_with_path', type=str,
                        default='/home/hongyi/Downloads/NCRouteArcs_and_LiDAR_Road_Edge/'
                                'RoadEdge_40001001011_vertices.shp',
                        help='input shp file that contains road x, y, z vertices from lidar')
    parser.add_argument('--output_file', type=str,
                        default='/home/hongyi/ncdot-road-safety/phase_2/data_processing/data/d13_route_40001001011/'
                                'oneformer/output/input_3d.pkl',
                        help='output path for 3D points to be corresponded with from 2D image points in pickle format')
    parser.add_argument('--camera_loc', type=str,
                        default=[35.7137581, -82.7346679],
                        help='camera loc to extract lidar vertices within a set threshold distance from')
    parser.add_argument('--next_camera_loc', type=str,
                        default=[35.7136764,-82.7346359],
                        help='next camera loc to define camera/driving bearing direction')
    parser.add_argument('--distance_threshold', type=str,
                        #default=385,
                        default=190,
                        help='distance threshold in meter to filter out lidar vertices')

    args = parser.parse_args()
    input_lidar_shp_with_path = args.input_lidar_shp_with_path
    output_file = args.output_file
    camera_loc = args.camera_loc
    next_camera_loc = args.next_camera_loc
    distance_threshold = args.distance_threshold
    lidar_df = get_lidar_data_from_shp(input_lidar_shp_with_path)
    vertices, _ = extract_lidar_3d_points_for_camera(lidar_df, camera_loc, next_camera_loc, dist_th=distance_threshold)

    with open(output_file, 'wb') as f:
        pickle.dump(vertices, f)
