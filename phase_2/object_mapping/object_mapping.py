# ------------------------------------------
# This module contains the adapted implementation of the MRF-based triangulation procedure introduced in
# "Automatic Discovery and Geotagging of Objects from Street View Imagery" https://arxiv.org/abs/1708.08417.
# See https://github.com/vlkryl/streetview_objectmapping/blob/master/objectmapping.py for the original
# implementation and copyright info of the approach.
#
# This object mapping module takes a csv file as input where each line in
# the csv file defines a detected object with FOUR floating point values: camera positions (GPS latitude and
# longitude), bearing from north clockwise in degrees towards the object in the panoramic image and the depth estimate.
#
# The module performs triangulation, MRF optimization to establish the optimal object configuration and clustering.
#
# The output csv file contains the list of GPS-coordinates (latitude and longitude) of identified objects of interests
# and a score value for each of these. The score is the number of individual views contributing to an object
# (greater than or equal to 2).
# ------------------------------------------

import argparse
import os
import sys
import os.path
import time
import numpy as np
import pandas as pd
import itertools
from math import radians, cos, sin, asin, sqrt, dist
from utils import lat_lon_to_meters, meters_to_lat_lon, hierarchical_clustering, \
    get_max_degree_dist_in_cluster_from_lat_lon
from common.utils import haversine

# preset parameters
# Max distance from camera to objects (in meters). May need to increase it if trying to geolocate poles more than
# 25 meters away from the camera, e.g., it needs to be set to 105 in order to geolocate the test pole in the new
# test scene since the test pole is about 100 meters away from the camera. This parameter needs to be adjusted
# in conjunction with the depth scaling factor in compute_mapping_input.py since the predicted depth is used as
# a constraint with computed distance from the camera to computed intersection points
MAX_OBJ_DIST_FROM_CAM = 100
MAX_DIST_IN_CLUSTER = 1  # Maximal size of clusters employed (in meters)
# this SCALING_FACTOR is applied to the predicted depth, then the product is compared with the distance between
# the camera and the intersection point for energy, so if the real distance from camera to the geotagged location
# is around 100, the predicted absolute depth needs to be about 55 (i.e., about one half of the real distance),
# in order to have a small difference between the computed distance and the predicted depth
SCALING_FACTOR = 640.0 / 256

# MRF optimization parameters
DEPTH_WEIGHT = 0.199  # weight alpha in Eq.(4)
OBJ_MULTI_VIEW = 0.2  # weight beta in  Eq.(4)
STANDALONE_PRICE = max(1 - DEPTH_WEIGHT - OBJ_MULTI_VIEW, 0)  # weight (1-alpha-beta) in Eq. (4)

# indices as constants in the input data array
LAT_P1, LON_P1, BEARING, DEPTH, LAT_C, LON_C, LAT_P, LON_P, BASE_IMAGE_NAME = 0, 1, 2, 3, 5, 6, 7, 8, 9


# calculating the intersection point between two rays (specified each by camera position and depth-estimated object
# location). Refer to https://en.wikipedia.org/wiki/Line%E2%80%93line_intersection where u = y, t = x
def compute_intersect(obj1, obj2):
    lat_c1_x1, lon_c1_y1 = obj1[LAT_C], obj1[LON_C]
    lat_c2_x3, lon_c2_y3 = obj2[LAT_C], obj2[LON_C]
    # normalized object lat/lon which does not take into account input depth
    lat_p1_x2, lon_p1_y2 = obj1[LAT_P1], obj1[LON_P1]
    lat_p2_x4, lon_p2_y4 = obj2[LAT_P1], obj2[LON_P1]

    a1, b1, c1 = lat_p1_x2 - lat_c1_x1, lat_p2_x4 - lat_c2_x3, lat_c2_x3 - lat_c1_x1
    a2, b2, c2 = lon_p1_y2 - lon_c1_y1, lon_p2_y4 - lon_c2_y3, lon_c2_y3 - lon_c1_y1

    # d is determinant
    d = a2 * b1 - b2 * a1
    if d:
        y = (a1 * c2 - a2 * c1) / d
    else:
        return -1, -1, 0, 0

    if a1 != 0:
        x = (b1 * y + c1) / a1
    else:
        x = (b2 * y + c2) / a2
    if (x < 0) or (y < 0):
        return -2, -2, 0, 0
    if (x > MAX_OBJ_DIST_FROM_CAM) or (y > MAX_OBJ_DIST_FROM_CAM):
        return -3, -3, 0, 0
    mx, my = a1 * x + lat_c1_x1, a2 * x + lon_c1_y1
    # if obj1[BASE_IMAGE_NAME] == '926005500131' or obj2[BASE_IMAGE_NAME] == '926005500131':
    #    print(f'Object1: {obj1[BASE_IMAGE_NAME]}, Object2: {obj2[BASE_IMAGE_NAME]}, {x}, {y}, {mx}, {my}')

    # x and y are the distances of intersection to cameras C1 and C2, respectively,
    # and mx, my are (x, y) coordinate of intersection
    return x, y, mx, my


# calculate the MRF energy of an intersection
def compute_energy(objs_dist, objs, objs_connectivity, obj):
    inters = np.count_nonzero(objs_connectivity[obj, :])
    if inters == 0:
        # increase energy if the view ray object has no intersection with other view ray objects
        return STANDALONE_PRICE
    energy = 0
    depth_min, depth_max = 1000, 0
    for i in range(len(objs)):
        if objs_connectivity[obj, i]:
            # increase energy by penalizing distance between triangulated distance and depth estimate
            depth_pen = DEPTH_WEIGHT * abs(objs_dist[obj, i] - (objs[obj])[DEPTH])
            print(f'{objs_dist[obj, i]} - {(objs[obj])[DEPTH]} - depth_pen: {depth_pen}')
            energy += depth_pen
            # if Object == 63 or Object == 64:
            #     print(f"object depth: {objs[obj][DEPTH]}, i: {i}, dist: {objs_dist[obj, i]}, depth_pen: {depth_pen}")
            if objs_dist[obj, i] < depth_min:
                depth_min = objs_dist[obj, i]
            if objs_dist[obj, i] > depth_max:
                depth_max = objs_dist[obj, i]
    # increase energy by penalizing excessive spread for an object with multiple view ray intersections
    print(f'energy: {energy}, depth_min: {depth_min}, depth_max: {depth_max}')
    return energy + OBJ_MULTI_VIEW * (depth_max - depth_min)


# calculate the averaged object location (used after clustering)
def compute_avg_object(intersects, objs_connectivity, obj):
    res = np.zeros(2)
    cnt = 0
    idx_list = []
    for i in range(intersects.shape[0]):
        if objs_connectivity[obj, i]:
            res[:] += intersects[obj, i, :]
            idx_list.append(i)
            cnt += 1
    if cnt:
        return res / cnt, idx_list
    return res, idx_list


def get_input_object(lat, lon, bearing, depth, base_img, planar):
    # calculating the object positions from camera position + bearing + depth_estimate
    br1 = radians(bearing)
    if not planar:
        mx, my = lat_lon_to_meters(lat, lon)
        y_obj_pos = my + depth * cos(br1) * SCALING_FACTOR  # depth-based positions
        x_obj_pos = mx + depth * sin(br1) * SCALING_FACTOR
        lat_obj_p, lon_obj_p = meters_to_lat_lon(x_obj_pos, y_obj_pos)
        y_obj_pos = my + 1.0 * cos(br1) * SCALING_FACTOR  # normalized positions (at 1m distance from camera)
        x_obj_pos = mx + 1.0 * sin(br1) * SCALING_FACTOR
        lat_obj_p1, lon_obj_p1 = meters_to_lat_lon(x_obj_pos, y_obj_pos)
        return (lat_obj_p1, lon_obj_p1, bearing, depth, 0, lat, lon, lat_obj_p, lon_obj_p, base_img)
    else:
        mx, my = lat, lon
        y_obj_p = my + depth * cos(br1)  # depth-based positions
        x_obj_p = mx + depth * sin(br1)
        y_obj_p1 = my + 1.0 * cos(br1)  # normalized positions (at 1m distance from camera)
        x_obj_p1 = mx + 1.0 * sin(br1)
        return (x_obj_p1, y_obj_p1, bearing, depth, 0, mx, my, x_obj_p, y_obj_p, base_img)


def main(input_filename, output_filename, output_intersect=False, is_planar=False):
    start = time.time()
    objects_base = []

    if not os.path.isfile(input_filename):
        print('Input file not found. Aborting.')
        return

    if os.path.isfile(output_filename):
        os.remove(output_filename)

    ###############################
    # A L L  O B J E C T S        #
    ###############################
    input_df = pd.read_csv(input_filename, usecols=['imageBaseName', 'lat', 'lon', 'bearing', 'depth'],
                           dtype={'imageBaseName': str, 'lat': float, 'lon': float, 'bearing': float, 'depth': float})
    input_df.apply(lambda row: objects_base.append(get_input_object(
        row['lat'], row['lon'], row['bearing'], row['depth'], row['imageBaseName'], is_planar)), axis=1)
    print("All detected objects: {0:d}".format(len(objects_base)))
    #############################
    # A D M I S S I B L E       #
    #############################

    # the maximal distance between the two camera positions observing the same object
    max_cam_dist = 1.5 * MAX_OBJ_DIST_FROM_CAM

    num_intersects = 0
    objects_dist = np.zeros((len(objects_base), len(objects_base)))
    objects_intersects = np.zeros((len(objects_base), len(objects_base), 2))
    # compute PAIRWISE intersections
    for i in range(len(objects_base)):
        if i % 1000 == 0 and i > 0:
            print('Parsed {} object entries ({:.2f}%)'.format(i, 100. * i / len(objects_base)))
        objects_dist[i, i] = -5
        for j in range(i + 1, len(objects_base)):
            if not is_planar:
                cam_dist = haversine(objects_base[i][LON_C], objects_base[i][LAT_C], objects_base[j][LON_C],
                                     objects_base[j][LAT_C])
            else:
                cam_dist = dist([objects_base[i][LAT_C], objects_base[i][LON_C]], [objects_base[j][LAT_C],
                                                                                   objects_base[j][LON_C]])

            # cam_positions - same (less than 1m apart) or too far
            if cam_dist < 0.5 or cam_dist > max_cam_dist:
                objects_dist[i, j] = -4
                objects_dist[j, i] = -4
                continue
            objects_dist[i, j], objects_dist[j, i], objects_intersects[i, j, 0], objects_intersects[i, j, 1] = \
                compute_intersect(objects_base[i], objects_base[j])
            objects_intersects[j, i, 0], objects_intersects[j, i, 1] = \
                objects_intersects[i, j, 0], objects_intersects[i, j, 1]

            if objects_dist[i, j] > 0:
                num_intersects += 1

    print("All admissible intersections: {0:d}".format(num_intersects))

    objects_connectivity = np.zeros((len(objects_base), len(objects_base)), dtype=np.uint8)
    objects_connect_viable_options = np.zeros(len(objects_base), dtype=np.uint8)
    for i in range(len(objects_base)):
        objects_connect_viable_options[i] = np.count_nonzero(objects_dist[i, :] > 0)

    #############################
    #           I C M           #
    #############################

    for test_obj in range(len(objects_base)):
        select_cnt = 0
        if objects_connect_viable_options[test_obj] == 0:  # no pairing possible (standalone - )
            continue
        # look at other viable connections to testObject
        for test_obj_pair in range(test_obj + 1, len(objects_base)):
            if objects_dist[test_obj, test_obj_pair] > 0:
                energy_old = compute_energy(objects_dist, objects_base, objects_connectivity, test_obj)
                energy_old += compute_energy(objects_dist, objects_base, objects_connectivity, test_obj_pair)
                objects_connectivity[test_obj, test_obj_pair] = 1 - objects_connectivity[test_obj, test_obj_pair]
                objects_connectivity[test_obj_pair, test_obj] = 1 - objects_connectivity[test_obj_pair, test_obj]
                energy_new = compute_energy(objects_dist, objects_base, objects_connectivity, test_obj)
                energy_new += compute_energy(objects_dist, objects_base, objects_connectivity, test_obj_pair)
                if energy_new <= energy_old:
                    # keep the connection between testObject and testObjectPair
                    select_cnt += 1
                    continue

                # revert to the old configuration
                objects_connectivity[test_obj, test_obj_pair] = 1 - objects_connectivity[test_obj, test_obj_pair]
                objects_connectivity[test_obj_pair, test_obj] = 1 - objects_connectivity[test_obj_pair, test_obj]

        print(f'accepted {select_cnt} changes in intersections to {test_obj}:')

    #############################
    #    C L U S T E R I N G    #
    #############################
    if not is_planar:
        max_dist_in_cluster = get_max_degree_dist_in_cluster_from_lat_lon((objects_base[0])[0], (objects_base[0])[1])
    else:
        mx, my = (objects_base[0])[0], (objects_base[0])[1]
        # cos(45) and sin(45) are all equal to 0.707, so d45 is the projected distance of MaxDisInCluster to x and y
        d45 = 0.707 * MAX_DIST_IN_CLUSTER
        ax, ay = mx + d45, my + d45
        ax1, ay1 = mx, my
        max_dist_in_cluster = ((ax - ax1) ** 2 + (ay - ay1) ** 2) ** 0.5

    intersect_list = []
    intersect_index_pairs = []
    print(f'objects_connectivity: {objects_connectivity}')
    print(f'objects_intersects: {objects_intersects}')
    for i in range(len(objects_base)):
        res, id_list = compute_avg_object(objects_intersects, objects_connectivity, i)
        print(f'res: {res}, id_list: {id_list}')
        if res[0]:
            intersect_list.append((res[0], res[1]))
            for oid in id_list:
                intersect_index_pairs.append((i, oid))
    print("ICM intersections: {0:d}".format(len(intersect_list)))
    intersect_clusters, ret_clusters = hierarchical_clustering(intersect_list, max_dist_in_cluster)

    num_clusters = intersect_clusters.shape[0]
    with open(output_filename, "w") as inter:
        inter.write("lat,lon,score\n")
        for i in range(num_clusters):
            inter.write("{0:f},{1:f},{2:d}\n".format(intersect_clusters[i, 0] / intersect_clusters[i, 2],
                                                     intersect_clusters[i, 1] / intersect_clusters[i, 2],
                                                     int(intersect_clusters[i, 2])))
    if output_intersect:
        with open(f'{os.path.splitext(output_filename)[0]}_intersect_base_images.txt', "w") as img_fp:
            for i, item in enumerate(intersect_index_pairs):
                img_fp.write(f"{item[0]}:{objects_base[item[0]][BASE_IMAGE_NAME]} "
                             f"{item[1]}:{objects_base[item[1]][BASE_IMAGE_NAME]} "
                             f"{ret_clusters[i]}\n")

    print("Number of output clusters: {0:d}".format(num_clusters))
    if not is_planar:
        # make further clustering of objects based on whether the objects detected in the sequence of consecutive
        # images can be treated as the same object. The decision rule is based on the fact that our images were
        # collected in sequence when the vehicle with cameras were driven toward the object from farther away to closer.
        cluster_dict = {}
        for idx_pair, cluster_idx in zip(intersect_index_pairs, ret_clusters):
            if cluster_idx not in cluster_dict:
                cluster_dict[cluster_idx] = list(idx_pair)
            else:
                cluster_dict[cluster_idx] += idx_pair
                # remove potential duplicates
                cluster_dict[cluster_idx] = list(set(cluster_dict[cluster_idx]))

        clusters = [[objects_base[idx][BASE_IMAGE_NAME], objects_base[idx][BEARING], objects_base[idx][DEPTH],
                     cluster_idx] for cluster_idx, idx_pairs in cluster_dict.items() for idx in idx_pairs]
        # sort clusters by base image name
        clusters.sort()
        # check whether further clustering can be performed
        image_idx = 0
        bearing_idx = 1
        depth_idx = 2
        cluster_idx = 3
        i, item_i = 0, clusters[0]
        j, item_j = 1, clusters[1]
        to_be_clustered = []
        while j < len(clusters) - 1:
            item_i, item_j = clusters[i], clusters[j]
            if item_j[cluster_idx] == item_i[cluster_idx]:
                # already clustered, no need to further cluster
                i += 1
                j += 1
                continue
            set_i, hour_i, minute_i, second_i, seq_num_i = \
                item_i[image_idx][:3], item_i[image_idx][3:5], item_i[image_idx][5:7], \
                int(item_i[image_idx][7:9]), item_i[image_idx][9:11]
            set_j, hour_j, minute_j, second_j, seq_num_j = \
                item_j[image_idx][:3], item_j[image_idx][3:5], item_j[image_idx][5:7], \
                int(item_j[image_idx][7:9]), item_j[image_idx][9:11]
            if set_j != set_i or hour_j != hour_i or minute_j != minute_i or abs(second_j - second_i) > 2 or \
                    item_i[depth_idx] < item_j[depth_idx]:
                # cannot be further clustered
                i += 1
                j += 1
                continue
            # see if the bearing change is consistent between cluster item i and j and between j and its next
            # in the same cluster
            k = j + 1
            # find the next cluster item which is in the same cluster as item j
            while k < len(clusters) and clusters[k][cluster_idx] != clusters[j][cluster_idx]:
                k += 1
            if k >= len(clusters):
                # item j is the last item in the cluster with no next item, so cannot be further clustered
                i += 1
                j += 1
                continue
            item_k = clusters[k]
            if (item_i[bearing_idx] < item_j[bearing_idx] < item_k[bearing_idx]) or \
                    (item_i[bearing_idx] > item_j[bearing_idx] > item_k[bearing_idx]):
                # item_i cluster and item_j cluster can be further clustered
                if len(to_be_clustered) < 1:
                    to_be_clustered.append([item_i[cluster_idx], item_j[cluster_idx]])
                else:
                    added = False
                    for idx, sub_cluster in enumerate(to_be_clustered):
                        if item_i[cluster_idx] in sub_cluster and item_j[cluster_idx] in sub_cluster:
                            # already in cluster
                            added = True
                            break
                        if item_i[cluster_idx] in sub_cluster:
                            to_be_clustered[idx].append(item_j[cluster_idx])
                            added = True
                            break
                        elif item_j[cluster_idx] in sub_cluster:
                            to_be_clustered[idx].append(item_i[cluster_idx])
                            added = True
                            break
                    if not added:
                        to_be_clustered.append([item_i[cluster_idx], item_j[cluster_idx]])
            i += 1
            j += 1
        if len(to_be_clustered) > 0:
            updated_cluster_cnt = 0
            with open(f'{os.path.splitext(output_filename)[0]}_further_clustering.csv', "w") as inter:
                inter.write("lat,lon,score\n")
                for i in range(num_clusters):
                    if i not in itertools.chain.from_iterable(to_be_clustered):
                        inter.write("{0:f},{1:f},{2:d}\n".format(intersect_clusters[i, 0] / intersect_clusters[i, 2],
                                                                 intersect_clusters[i, 1] / intersect_clusters[i, 2],
                                                                 int(intersect_clusters[i, 2])))
                        updated_cluster_cnt += 1
                for sub_cluster in to_be_clustered:
                    lat_sum = lon_sum = count_sum = 0
                    for idx in sub_cluster:
                        lat_sum += intersect_clusters[idx, 0]
                        lon_sum += intersect_clusters[idx, 1]
                        count_sum += int(intersect_clusters[idx, 2])
                    inter.write("{0:f},{1:f},{2:d}\n".format(lat_sum / count_sum,
                                                             lon_sum / count_sum,
                                                             count_sum))
                    updated_cluster_cnt += 1
            print(f"Number of output clusters after further clustering: {updated_cluster_cnt}")

    print("Elapsed total time: {0:.2f} seconds.".format(time.time() - start))


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Process arguments.')
    parser.add_argument('--input_file', type=str,
                        # default='../data_processing/data/d13_route_40001001011/oneformer/output/all_lidar_vertices/test_mapping_input.csv',
                        default='../data_processing/data/new_test_scene/lane_test/test_mapping_input.csv',
                        help='input file name with path')
    parser.add_argument('--output_file', type=str,
                        # default='../data_processing/data/d13_route_40001001011/oneformer/output/all_lidar_vertices/test_mapping_output.csv',
                        default='../data_processing/data/new_test_scene/lane_test/test_mapping_output.csv',
                        help='output file name with path')
    parser.add_argument('--output_intersect_base_images', action='store_true',
                        help='output list of intersection base images for categorization')
    parser.add_argument('--compute_planar', action='store_true',
                        help='computing object mapping assuming input objects are in planar coordinate system which '
                             'is useful to verify the accuracy of the approach and its sensitivity to the input '
                             'variations and hard coded parameters')

    args = parser.parse_args()
    input_file = args.input_file
    output_file = args.output_file
    output_intersect_base_images = args.output_intersect_base_images
    compute_planar = args.compute_planar
    main(input_file, output_file, output_intersect=output_intersect_base_images, is_planar=compute_planar)
    sys.exit(0)
