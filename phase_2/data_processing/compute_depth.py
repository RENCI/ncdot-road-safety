import os
import argparse
import pandas as pd
from PIL import Image
import numpy as np
from pypfm import PFMLoader
from utils import consecutive


ROAD = 1
POLE = 2
SCALING_FACTOR = 25
GAP_PIXEL_COUNT = 15


def compute_depth(mapped_image, path):
    # compute depth of segmented object taking the 10%-trimmed mean of the depths of its constituent pixels
    # to gain robustness with respect to segmentation errors, in particular along the object borders
    image_suffix_list = ('5.png', '1.png', '2.png')
    for suffix in image_suffix_list:
        input_image_name = os.path.join(path, f'{mapped_image}{suffix}')
        input_image = Image.open(input_image_name)
        image_width = input_image.width
        image_height = input_image.height
        input_data = np.array(input_image)
        levels = input_data[np.nonzero(input_data)]
        if np.size(levels) > 0:
            obj_level_indices = np.where(input_data == POLE)
            count = np.size(obj_level_indices)
            if count > 0:
                loader = PFMLoader((image_width, image_height), color=False, compress=False)
                input_image_base_name = os.path.basename(os.path.splitext(input_image_name)[0])
                image_pfm = loader.load_pfm(os.path.join(input_depth_image_path,
                                                         f'{input_image_base_name}.pfm'))
                image_pfm = np.flipud(image_pfm)
                # print(f'image_pfm shape: {image_pfm.shape}')
                min_depth = image_pfm.min()
                max_depth = image_pfm.max()
                # input_data[input_data == POLE] = 255
                # updated_image = Image.fromarray(input_data)
                # updated_image.save(os.path.join(path, f'updated_{mapped_image}{suffix}'))

                # pole are straight objects, so considering y axis for separating multiple poles since arrays are
                # stored in row/x order so y axis should be continuous
                centroid_xs = []
                split_indices, con_level_indices_y = consecutive(obj_level_indices[0], step_size=GAP_PIXEL_COUNT)
                # use the same splits to split corresponding x values for separated poles by y
                con_level_indices_x = np.split(obj_level_indices[1], split_indices + 1)
                for level_indices_x, level_indices_y in zip(con_level_indices_x, con_level_indices_y):
                    min_x = min(level_indices_x)
                    max_x = max(level_indices_x)
                    min_y = min(level_indices_y)
                    max_y = max(level_indices_y)
                    centroid_x = (min_x+max_x)/2
                    if not centroid_xs:
                        centroid_xs.append(centroid_x)
                    else:
                        is_separate_pole = False
                        for x in centroid_xs:
                            if abs(centroid_x - x) > GAP_PIXEL_COUNT:
                                is_separate_pole = True
                                break
                        if not is_separate_pole:
                            continue
                    trim_size_y = (max_y - min_y) * 0.01
                    trim_size_x = (max_x - min_x) * 0.01
                    if trim_size_y > 0:
                        filtered_level_indices = level_indices_y[((level_indices_y-min_y) > trim_size_y)
                                                                  & ((max_y-level_indices_y) > trim_size_y)]
                        if np.size(filtered_level_indices) > 0:
                            average_y = int(np.average(filtered_level_indices))
                        else:
                            continue
                    else:
                        average_y = int(np.average(level_indices_y))
                    if trim_size_x > 0:
                        filtered_level_indices = level_indices_x[((level_indices_x-min_x) > trim_size_x)
                                                                  & ((max_x-level_indices_x) > trim_size_x)]
                        if np.size(filtered_level_indices) > 0:
                            average_x = int(np.average(filtered_level_indices) + 0.5)
                        else:
                            continue
                    else:
                        average_x = int(np.average(level_indices_x)+0.5)
                    depth = (image_pfm[average_y, average_x] - min_depth) / (max_depth - min_depth)
                    img_depth_list.append([input_image_base_name, (1 - depth) * SCALING_FACTOR])


parser = argparse.ArgumentParser(description='Process arguments.')
parser.add_argument('--input_csv_file_with_path', type=str,
                    default='data/route_40001001011_segment_labels_with_poles.csv',
                    help='input csv file that includes input segmented image path and name for computing depth')
parser.add_argument('--input_depth_image_path', type=str,
                    default='../midas/output',
                    help='input path that includes depth prediction output images')
parser.add_argument('--output_file', type=str,
                    default='data/route_40001001011_segment_object_depths.csv',
                    help='output file that contains image base names and corresponding segmented object depths')


args = parser.parse_args()
input_csv_file_with_path = args.input_csv_file_with_path
input_depth_image_path = args.input_depth_image_path
output_file = args.output_file

df = pd.read_csv(input_csv_file_with_path, index_col=None, usecols=['MAPPED_IMAGE', 'LABEL_PATH'], dtype=str)
img_depth_list = []
df.apply(lambda row: compute_depth(row['MAPPED_IMAGE'], row['LABEL_PATH']), axis=1)
out_df = pd.DataFrame (img_depth_list, columns = ['ImageBaseName', 'Depth'])
out_df.to_csv(output_file, index=False)
