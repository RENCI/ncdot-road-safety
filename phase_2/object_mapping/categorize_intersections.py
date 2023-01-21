#!/usr/bin/env python
import argparse
import pandas as pd
import ast

'''
This script categorizes intersections created by the MRF-based object mapping approach into whether intersections 
come from image segmentation FPs
'''


parser = argparse.ArgumentParser(description='Process arguments.')
parser.add_argument('--intersection_filename', type=str,
                    default='data/pole_detection_intersect_base_images.txt',
                    help='filename that contains list of base image intersections created by mapping')
parser.add_argument('--seg_fps_filename', type=str,
                    default='data/route_40001001011_segment_object_input_fps.csv',
                    help='filename that contains list of image fps')
parser.add_argument('--output_file_name', type=str, default='data/route_40001001011_pole_detect_intersect_cat.csv',
                    help='output file name that contains categorization of intersection input')


args = parser.parse_args()
intersection_filename = args.intersection_filename
seg_fps_filename = args.seg_fps_filename
output_file_name = args.output_file_name

fps_df = pd.read_csv(seg_fps_filename, index_col='ImageBaseName', dtype=str)
fps_df.fillna('', inplace=True)
intersects_1 = []
intersects_2 = []
category = []
with open(intersection_filename, 'r') as f:
    for line in f:
        inter_pts = ast.literal_eval(line)
        intersects_1.append(int(inter_pts[0]))
        intersects_2.append(int(inter_pts[1]))
        intersect_cats = [fps_df.loc[intersects_1[-1]]['Category'],
                          fps_df.loc[intersects_2[-1]]['Category']]
        fp_added = False
        for inter_cat in intersect_cats:
            if isinstance(inter_cat, str):
                if inter_cat == 'FP':
                    category.append('FP')
                    fp_added = True
                    break
            elif isinstance(inter_cat, pd.Series):
                if inter_cat.str.contains('FP').any():
                    category.append('FP')
                    fp_added = True
                    break
        if not fp_added:
            category.append('Valid')
out_df = pd.DataFrame({'Intersect_1': intersects_1,
                       'Intersect_2': intersects_2,
                       'Category': category})
out_df.to_csv(output_file_name, index=False)
