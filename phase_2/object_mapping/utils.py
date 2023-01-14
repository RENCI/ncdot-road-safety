#!/usr/bin/env python

import numpy as np
from math import pi, tan, atan, exp, log
from scipy.cluster.hierarchy import linkage, fcluster


# conversion from (lat,lon) to meters
def lat_lon_to_meters(lat, lon):
    # Converts given lat/lon in WGS84 Datum to XY in Spherical Mercator EPSG:4326
    origin_shift = 2 * pi * 6378137 / 2.0
    mx = lon * origin_shift / 180.0
    my = log(tan((90+lat) * pi/360.0))/(pi/180.0)
    my = my * origin_shift / 180.0
    return mx, my


# conversion from meters to (lat,lon)
def meters_to_lat_lon(mx, my):
    # Converts XY point from Spherical Mercator EPSG:4326 to lat/lon in WGS84 Datum
    origin_shift = 2 * pi * 6378137 / 2.0
    lon = (mx / origin_shift) * 180.0
    lat = (my / origin_shift) * 180.0
    lat = 180 / pi * (2 * atan(exp(lat * pi / 180.0)) - pi / 2.0)
    return lat, lon


# hierarchical clustering
def hierarchical_clustering(intersects, max_intra_degree_dst):
    # Z returned is the hierarchical clustering encoded as a linkage matrix.
    Z = linkage(np.asarray(intersects))
    clusters = fcluster(Z, max_intra_degree_dst, criterion='distance') - 1
    num_clusters = max(clusters) + 1
    intersect_clusters = np.zeros((num_clusters, 3))
    for i in range(len(intersects)):
        intersect_clusters[clusters[i], 0] += (intersects[i])[0]
        intersect_clusters[clusters[i], 1] += (intersects[i])[1]
        intersect_clusters[clusters[i], 2] += 1
    return intersect_clusters


def get_max_degree_dist_in_cluster_from_lat_lon(lat, lon, max_dist_in_cluster=1, scaling_factor=640.0/256):
    mx, my = lat_lon_to_meters(lat, lon)
    # cos(45) and sin(45) are all equal to 0.707, so d45 is the projected distance of MaxDisInCluster to x and y
    d45 = 0.707 * max_dist_in_cluster * scaling_factor
    ax, ay = meters_to_lat_lon(mx + d45, my + d45)
    ax1, ay1 = meters_to_lat_lon(mx, my)
    return ((ax - ax1) ** 2 + (ay - ay1) ** 2) ** 0.5
