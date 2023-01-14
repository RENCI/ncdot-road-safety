#!/usr/bin/env python
import argparse
import pandas as pd
from utils import hierarchical_clustering, get_max_degree_dist_in_cluster_from_lat_lon

'''
This script combines multiple run results from the MRF-based object mapping algorithm of randomness nature and 
do the similar hierarchical clustering to the combined result to create the final result
'''

parser = argparse.ArgumentParser(description='Process arguments.')
parser.add_argument('--input_file_list', type=str,
                    default=[
                        'data/pole_detection.csv.1',
                        'data/pole_detection.csv.2',
                        'data/pole_detection.csv.3',
                        'data/pole_detection.csv.4',
                        'data/pole_detection.csv.5'
                    ],
                    help='list of input files to combine and cluster')
parser.add_argument('--output_file_name', type=str, default='data/pole_detection.csv',
                    help='output file name with path')


args = parser.parse_args()
input_file_list = args.input_file_list
output_file_name = args.output_file_name

dfs = [pd.read_csv(input_file, dtype=float, usecols=['lat', 'lon', 'score']) for input_file in input_file_list]
df = pd.concat(dfs, ignore_index=True).drop_duplicates()
print(df.shape)
print(df)
max_degree_dst_in_cluster = get_max_degree_dist_in_cluster_from_lat_lon(df.lat.iloc[0], df.lon.iloc[0])
intersect_clusters = hierarchical_clustering(list(zip(*map(df.get, ['lat', 'lon']))), max_degree_dst_in_cluster)
num_clusters = intersect_clusters.shape[0]
cluster_list = []
for i in range(num_clusters):
    lat_str = format(intersect_clusters[i, 0]/intersect_clusters[i, 2], '.6f')
    lat = float(lat_str)
    lon_str = format(intersect_clusters[i, 1]/intersect_clusters[i, 2], '.6f')
    lon = float(lon_str)
    ori_score_df = df.loc[(df.lat == lat) & (df.lon == lon)].reset_index()
    if not ori_score_df.empty:
        score = int(ori_score_df.loc[0, 'score']) + int(intersect_clusters[i, 2]) - 1
    else:
        print(f'cannot find {lat}/{lon} in original data')
        score = int(intersect_clusters[i, 2])
    cluster_list.append((lat_str, lon_str, score))
out_df = pd.DataFrame(cluster_list, columns=['lat', 'lon', 'score'])
out_df.to_csv(output_file_name, index=False)
print("Number of output ICM clusters: {0:d}".format(num_clusters))
