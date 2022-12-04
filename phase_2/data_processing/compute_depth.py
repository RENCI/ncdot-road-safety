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
            print(obj_level_indices)
            count = np.size(obj_level_indices)
            if count > 0:
                min_yx = max_yx = []
                for idx in range(2):
                    con_level_indices = consecutive(obj_level_indices[idx], step_size=1)
                    for level_indices in con_level_indices:
                        print(level_indices)
                        min_yx.append(min(level_indices))
                        max_yx.append(max(level_indices))
                        print(min_yx, min(level_indices))
                        print(max_yx, max(level_indices))
                print(input_image_name, min_yx[0], max_yx[0], min_yx[1], max_yx[1])
                trim_size_y = (max_yx[0] - min_yx[0]) * 0.05
                trim_size_x = (max_yx[1] - min_yx[1]) * 0.05
                if trim_size_y > 0:
                    filtered_level_indices = level_indices[0][((level_indices[0]-min_yx[0]) > trim_size_y)
                                                              & ((max_yx[0]-level_indices[0]) > trim_size_y)]
                    average_y = int(np.average(filtered_level_indices))
                else:
                    average_y = int(np.average(level_indices[0]))
                if trim_size_x > 0:
                    filtered_level_indices = level_indices[1][((level_indices[1]-min_yx[1]) > trim_size_x)
                                                              & ((max_yx[1]-level_indices[1]) > trim_size_x)]
                    average_x = int(np.average(filtered_level_indices) + 0.5)
                else:
                    average_x = int(np.average(level_indices[1])+0.5)

                # input_data[input_data == POLE] = 255
                # updated_image = Image.fromarray(input_data)
                # updated_image.save(os.path.join(path, f'updated_{mapped_image}{suffix}'))

                loader = PFMLoader((image_width, image_height), color=False, compress=False)
                input_image_base_name = os.path.basename(os.path.splitext(input_image_name)[0])
                image_pfm = loader.load_pfm(os.path.join(input_depth_image_path,
                                                         f'{input_image_base_name}.pfm'))
                image_pfm = np.flipud(image_pfm)
                print(f'image_pfm shape: {image_pfm.shape}')
                min_depth = image_pfm.min()
                max_depth = image_pfm.max()
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
