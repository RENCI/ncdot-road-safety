import argparse
import geopandas as gpd
import pickle


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Process arguments.')
    parser.add_argument('--input_lidar_shp_with_path', type=str,
                        default='/home/hongyi/Downloads/NCRouteArcs_and_LiDAR_Road_Edge/RoadEdge_40001001011_vertices.shp',
                        help='input shp file that contains road x, y, z vertices from lidar')
    parser.add_argument('--output_file', type=str,
                        default='/home/hongyi/ncdot-road-safety/phase_2/data_processing/data/d13_route_40001001011/'
                                'oneformer/output/input_3d.pkl',
                        help='output path for 3D points to be corresponded with from 2D image points in pickle format')

    args = parser.parse_args()
    input_lidar_shp_with_path = args.input_lidar_shp_with_path
    output_file = args.output_file

    # read shape file
    lidar_df = gpd.read_file(input_lidar_shp_with_path)
    # lidar_df should have columns Id, ORIG_FID, POINT_X, POINT_Y, POINT_Z, and geometry where geometry is
    # a point geometry, e.g., POINT Z (891488.760 734099.780 2018.620)
    # print(lidar_df.head())
    # total_bounds show minx, miny, maxx, maxy bounds of all geometry points
    # print(lidar_df.total_bounds)
    lidar_df = lidar_df.drop(columns = ['Id', 'ORIG_FID', 'geometry'])
    vertices = [lidar_df.to_numpy()]
    with open(output_file, 'wb') as f:
        pickle.dump(vertices, f)
