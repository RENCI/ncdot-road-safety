import os
import argparse
import pandas as pd
import numpy as np
from utils import get_data_from_image, POLE


def get_image_resolution(mapped_image, path):
    image_suffix_list = ('5.png', '1.png', '2.png')
    for suffix in image_suffix_list:
        image_name = f'{mapped_image}{suffix}'
        image_width, image_height, input_data = get_data_from_image(os.path.join(path, image_name))
        obj_level_indices = np.where(input_data == POLE)
        count = np.size(obj_level_indices)
        if count > 0:
            if image_width not in image_width_list:
                image_width_list.append(image_width)
                image_name_list.append(image_name)



parser = argparse.ArgumentParser(description='Process arguments.')
parser.add_argument('--input_csv_file_with_path', type=str,
                    default='/projects/ncdot/ade20k_annotations/route_40001001011_segment_labels_with_poles.csv',
                    help='input csv file that includes input image path and name for MiDAS depth prediction')
parser.add_argument('--output_file', type=str,
                    default='/projects/ncdot/geotagging/other/image_width.csv',
                    help='output file with image name and corresponding image width for HFOV computation')


args = parser.parse_args()
input_csv_file_with_path = args.input_csv_file_with_path
output_file = args.output_file

image_width_list = []
image_name_list = []
df = pd.read_csv(input_csv_file_with_path, index_col=None, usecols=['MAPPED_IMAGE', 'LABEL_PATH'], dtype=str)
df.apply(lambda row: get_image_resolution(row['MAPPED_IMAGE'], row['LABEL_PATH']), axis=1)
out_df = pd.DataFrame(list(zip(image_width_list, image_name_list)), columns=['ImageWidth', 'ImageName'])
out_df.to_csv(output_file, index=False)
