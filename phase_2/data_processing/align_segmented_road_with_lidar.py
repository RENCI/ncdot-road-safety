import argparse
import geopandas as gpd
from math import radians, cos, sin, asin, sqrt
import numpy as np
from shapely.geometry import MultiLineString


DIST_THRESHOLD = 30  # in meter, which is about 100 feet


# haversine distance formula between two points specified by their GPS coordinates
def haversine(lon1, lat1, geom):
    """
    Calculate the great circle distance between two points
    on the earth (specified in decimal degrees) in meter
    """
    lat2 = geom.y
    lon2 = geom.x
    # convert decimal degrees to radians
    lon1, lat1, lon2, lat2 = map(radians, [float(lon1), float(lat1), float(lon2), float(lat2)])
    # haversine formula
    dist_lon = lon2 - lon1
    dist_lat = lat2 - lat1
    a = sin(dist_lat / 2) ** 2 + cos(lat1) * cos(lat2) * sin(dist_lon / 2) ** 2
    return 6367000. * 2 * asin(sqrt(a))


def compute_geometry(row, ldf):
    # compute distance between each input lat/lon location and LIDAR projected geometry lat/lon
    ldf['distance'] = ldf['geometry_y'].apply(lambda geom: haversine(row['lon'], row['lat'], geom))
    ldf_sorted = ldf.sort_values(by=['distance'])
    ldf_select = ldf_sorted[ldf_sorted.distance <= DIST_THRESHOLD]
    if len(ldf_select) < 4:
        # there is not enough LIDAR road points within DIST_THRESHOLD, get four closet LIDAR road points instead
        ldf_select = ldf_sorted[:4]
    ldf_select = ldf_select.sort_index()
    # get indices where the geometry point starts on the other side of the road
    indices = np.where(abs(np.diff(ldf_select.POINT_Y)) <= 5)
    if len(indices[0]) != 1:
        print(f'ldf_select has {len(indices[0])} indices where the geometry points starts on the '
              f'other side of the road: {ldf_select}')
        return None
    index = indices[0][0]
    ldf_select.reset_index(inplace=True)
    line_coords = [[], []]
    for i in range(0, len(ldf_select)):
        if i <= index:
            line_coords[0].append((ldf_select.iloc[i].POINT_X, ldf_select.iloc[i].POINT_Y, ldf_select.iloc[i].POINT_Z))
        else:  # i > index
            line_coords[1].append((ldf_select.iloc[i].POINT_X, ldf_select.iloc[i].POINT_Y, ldf_select.iloc[i].POINT_Z))
    for i in range(2):
        line_coords[i] = tuple(line_coords[i])
    if len(line_coords[0]) > 0 and len(line_coords[1]) > 0:
        return MultiLineString(line_coords)
    else:
        return None


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Process arguments.')
    parser.add_argument('--input_lidar_shp_with_path', type=str,
                        default='/home/hongyi/Downloads/NCRouteArcs_and_LiDAR_Road_Edge/RoadEdge_40001001011_vertices.shp',
                        help='input shp file that contains road x, y, z vertices from lidar')
    parser.add_argument('--object_input_with_path', type=str,
                        default='/home/hongyi/ncdot-road-safety/phase_2/object_mapping/data/pole_input.csv',
                        help='input csv file that includes detected object input feeding to the object tagging algorithm')
    parser.add_argument('--output_file', type=str,
                        default='/home/hongyi/ncdot-road-safety/phase_2/data_processing/data/d13_route_40001001011/'
                                'oneformer/output/pole_input_geometry.shp',
                        help='output path for aligned road info')

    args = parser.parse_args()
    input_lidar_shp_with_path = args.input_lidar_shp_with_path
    object_input_with_path = args.object_input_with_path
    output_file = args.output_file

    df = gpd.read_file(object_input_with_path)
    # remove last digit which represents left, front, or right view, then remove duplicates
    df['imageBaseName'] = df['imageBaseName'].str[:-1]
    df = df.drop_duplicates(subset=['imageBaseName'], keep='first')
    print(f'object input size after dropping duplicates: {df.shape}')

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

    df['geometry'] = df.apply(lambda row: compute_geometry(row, lidar_df), axis=1)
    df.to_file(output_file)
