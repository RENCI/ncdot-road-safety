import argparse
import sys
import geopandas as gpd
import pickle
import cv2
import numpy as np
import math
from scipy.spatial import Delaunay
from utils import bearing_between_two_latlon_points, get_next_road_index, get_aerial_lidar_road_geo_df
from common.utils import haversine


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


def extract_lidar_3d_points_for_camera(df, cam_loc, next_cam_loc, dist_th=(20, 190), end_of_route=False,
                                       include_all_cols=False):
    clat, clon = cam_loc
    next_clat, next_clon = next_cam_loc
    df['distance'] = df.apply(lambda row: haversine(clon, clat, row['geometry_y'].x, row['geometry_y'].y), axis=1)
    cam_bearing = bearing_between_two_latlon_points(clat, clon, next_clat, next_clon, is_degree=False)
    df['bearing_diff'] = df.apply(lambda row: abs(cam_bearing - bearing_between_two_latlon_points(
        clat, clon, row['geometry_y'].y, row['geometry_y'].x, is_degree=False)), axis=1)
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

    df = df[(df['distance'] > dist_th[0]) & (df['distance'] < dist_th[1]) & (df['bearing_diff'] < math.pi / 3)]
    if include_all_cols:
        df = df.drop(columns=['bearing_diff'])
        return df.copy(), cam_bearing, df.columns
    else:
        if 'X' in df.columns:
            if 'C' in df.columns:
                inc_cols = ['X', 'Y', 'Z', 'C']
            else:
                inc_cols = ['X', 'Y', 'Z']
            if 'I' in df.columns:
                inc_cols.append('I')
            if 'BOUND' in df.columns:
                inc_cols.append('BOUND')
        elif 'C' in df.columns:
            inc_cols = ['POINT_X', 'POINT_Y', 'POINT_Z', 'C']
        else:
            inc_cols = ['POINT_X', 'POINT_Y', 'POINT_Z']
        df = df[inc_cols]
        return [df.to_numpy()], cam_bearing, inc_cols


def get_convex_hull_and_convexity_defects(points, image_width):
    # normalize points to a range for visualizing
    x_min, x_max = np.min(points[:, 0]), np.max(points[:, 0])
    y_min, y_max = np.min(points[:, 1]), np.max(points[:, 1])
    x_range, y_range = x_max - x_min + 1, y_max - y_min + 1
    scaling_range = x_range if x_range > y_range else y_range
    scaling_factor = image_width / scaling_range
    normalized_x = np.round((points[:, 0] - x_min) * scaling_factor).astype(np.int32)
    normalized_y = np.round((points[:, 1] - y_min) * scaling_factor).astype(np.int32)
    normalized_points = np.column_stack((normalized_x, normalized_y))
    hull_image = np.zeros((image_width + 1, image_width + 1), dtype=np.uint8)
    hull_image[normalized_points[:, 1], normalized_points[:, 0]] = 100

    triangulation = Delaunay(normalized_points)

    # Filter out large triangles based on side length
    max_side_length = 50
    filtered_simplices = []
    for simplex in triangulation.simplices:
        side_lengths = np.linalg.norm(
            triangulation.points[simplex] - np.roll(triangulation.points[simplex], shift=-1, axis=0), axis=1)
        if all(side_length < max_side_length for side_length in side_lengths):
            filtered_simplices.append(simplex)
    simplices_contour = np.vstack([triangulation.points[s] for s in filtered_simplices])
    print(simplices_contour.shape)
    # Extract the boundary contour
    boundary_contour = np.round(np.unique(simplices_contour.reshape(-1, 2), axis=0)).astype(np.int32)
    print(boundary_contour.shape)
    hull_image[boundary_contour[:, 1], boundary_contour[:, 0]] = 255

    # Convert the contour to integer (required by cv2.convexHull)
    hull_indices = cv2.convexHull(boundary_contour, returnPoints=False)
    # Extract the convex hull points
    # hull_points = boundary_contour[hull_indices.flatten()]
    # cv2.polylines(hull_image, [hull_points], isClosed=True, color=255, thickness=1)
    hull_indices[::-1].sort(axis=0)
    defects = cv2.convexityDefects(boundary_contour, hull_indices)

    # Create an empty image to draw the convexity defects
    if defects is not None:
        for defect in defects:
            sp, ep, fp, fdist = defect[0]
            print(fdist)
            if fdist > 20000:
                start = tuple(boundary_contour[sp])
                end = tuple(boundary_contour[ep])
                far = tuple(boundary_contour[fp])
                # cv2.line(hull_image, start, far, color=255, thickness=2)
                # cv2.line(hull_image, far, end, color=255, thickness=2)
                cv2.circle(hull_image, far, radius=5, color=255, thickness=-1)
    cv2.imshow("convexity defects", hull_image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Process arguments.')
    parser.add_argument('--input_lidar_with_path', type=str,
                        # default='/home/hongyi/Downloads/NCRouteArcs_and_LiDAR_Road_Edge/'
                        #         'RoadEdge_40001001011_vertices.shp',
                        default='data/new_test_scene/new_test_scene_road_raster_10_classified.csv',
                        help='input file that contains road x, y, z vertices from lidar')
    parser.add_argument('--output_file', type=str,
                        # default='/home/hongyi/ncdot-road-safety/phase_2/data_processing/data/d13_route_40001001011/'
                        #       'oneformer/output/input_3d.pkl',
                        default='data/new_test_scene/input_3d.pkl',
                        help='output path for 3D points to be corresponded with from 2D image points in pickle format')
    parser.add_argument('--camera_loc', type=str,
                        # default=[35.7137581, -82.7346679],
                        default=[35.6848124, -81.5217857],
                        help='camera loc to extract lidar vertices within a set threshold distance from')
    parser.add_argument('--next_camera_loc', type=str,
                        # default=[35.7136764,-82.7346359],
                        default=[35.6847461, -81.5218077],
                        help='next camera loc to define camera/driving bearing direction')
    parser.add_argument('--distance_threshold', type=str,
                        default=(20, 154),
                        help='distance threshold in meter to filter out lidar vertices')

    args = parser.parse_args()
    input_lidar_with_path = args.input_lidar_with_path
    output_file = args.output_file
    camera_loc = args.camera_loc
    next_camera_loc = args.next_camera_loc
    distance_threshold = args.distance_threshold
    if input_lidar_with_path.endswith('.shp'):
        lidar_df = get_lidar_data_from_shp(input_lidar_with_path)
    else:
        lidar_df = get_aerial_lidar_road_geo_df(input_lidar_with_path)
    vertices, _, _ = extract_lidar_3d_points_for_camera(lidar_df, camera_loc, next_camera_loc,
                                                        dist_th=distance_threshold)
    get_convex_hull_and_convexity_defects(vertices[0], 1000)
    with open(output_file, 'wb') as f:
        pickle.dump(vertices, f)
    sys.exit()
