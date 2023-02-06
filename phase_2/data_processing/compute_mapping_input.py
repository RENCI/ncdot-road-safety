import os
import argparse
import pandas as pd
import numpy as np
from pypfm import PFMLoader
from utils import consecutive, get_object_data_from_image, POLE, bearing_between_two_latlon_points


ROAD = 1
SCALING_FACTOR = 25
GAP_PIXEL_COUNT = 15
width_to_hfov = {
    2748: 71.43
}


def compute_mapping_input(mapped_image, path):
    # compute depth of segmented object taking the 10%-trimmed mean of the depths of its constituent pixels
    # to gain robustness with respect to segmentation errors, in particular along the object borders
    image_suffix_list = ('5.png', '1.png', '2.png')
    for suffix in image_suffix_list:
        input_image_name = os.path.join(path, f'{mapped_image}{suffix}')
        image_width, image_height, obj_level_indices = get_object_data_from_image(input_image_name, POLE)
        if image_width not in width_to_hfov:
            print(f'no HFOV can be found for image width {image_width} of the image {input_image_name}')
            continue
        count = np.size(obj_level_indices)
        if count > 0:
            # get camera location for the mapped image
            mapped_image_df = mapping_df[mapping_df['MAPPED_IMAGE'] == mapped_image]
            if len(mapped_image_df) != 1:
                # no camera location
                print(f'no camera location found for {mapped_image}')
                continue
            cam_lat = float(mapped_image_df.iloc[0]['LATITUDE'])
            cam_lon = float(mapped_image_df.iloc[0]['LONGITUDE'])
            # find the next camera lat/lon for computing bearing
            cam_lat2 = float(mapping_df.iloc[mapped_image_df.index+1]['LATITUDE'])
            cam_lon2 = float(mapping_df.iloc[mapped_image_df.index+1]['LONGITUDE'])
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
                # compute bearing
                cam_br = bearing_between_two_latlon_points(cam_lat, cam_lon, cam_lat2, cam_lon2)
                if suffix == '1.png':
                    # front view image
                    image_center_x = image_width/2
                    if average_x < image_center_x:
                        minus_bearing = True
                    else:
                        minus_bearing = False
                    hangle = (abs(average_x - image_center_x)/image_width) * width_to_hfov[image_width]

                elif suffix == '5.png':
                    # left view image
                    minus_bearing = True
                    # addition of 0.5 is needed to account for the front view image
                    hangle = ((image_width - average_x)/image_width + 0.5) * width_to_hfov[image_width]
                else:
                    # right view image
                    minus_bearing = False
                    # addition of 0.5 is needed to account for the front view image
                    hangle = (average_x / image_width + 0.5) * width_to_hfov[image_width]

                br_angle = (cam_br - hangle) if minus_bearing else (cam_br + hangle)
                br_angle = (br_angle + 360) % 360
                img_input_list.append([input_image_base_name, cam_lat, cam_lon, br_angle, (1 - depth) * SCALING_FACTOR])


parser = argparse.ArgumentParser(description='Process arguments.')
parser.add_argument('--input_seg_map_info_with_path', type=str,
                    default='/projects/ncdot/test_route_segmentation/test_route_road_pole_labels.csv',
                    help='input csv file that includes input segmented image path and name for computing depth')
parser.add_argument('--route_id', type=str, default='40001001011',
                    help='route id to filter input_seg_map_info_with_path data with')
parser.add_argument('--model_col_header', type=str, default='ONEFORMER',
                    help='input model column header in the input_seg_map_info_with_path to get segmentation path')
parser.add_argument('--input_sensor_mapping_file_with_path', type=str,
                    default='/projects/ncdot/secondary_road/output/d13/mapped_2lane_sr_images_d13.csv',
                    help='input csv file that includes mapped image lat/lon info')
parser.add_argument('--input_depth_image_path', type=str,
                    default='/projects/ncdot/geotagging/midas_output/d13_route_40001001011/oneformer',
                    help='input path that includes depth prediction output images')
parser.add_argument('--output_file', type=str, default='/projects/ncdot/geotagging/input/oneformer/'
                                                       'route_40001001011_segment_object_mapping_input.csv',
                    help='output file that contains image base names and corresponding segmented object depths')


args = parser.parse_args()
input_seg_map_info_with_path = args.input_seg_map_info_with_path
route_id = args.route_id
model_col_header = args.model_col_header
input_sensor_mapping_file_with_path = args.input_sensor_mapping_file_with_path
input_depth_image_path = args.input_depth_image_path
output_file = args.output_file

df = pd.read_csv(input_seg_map_info_with_path, index_col=None,
                 usecols=['ROUTEID', 'MAPPED_IMAGE', model_col_header], dtype=str)
if route_id:
    df = df[df.ROUTEID == route_id]

mapping_df = pd.read_csv(input_sensor_mapping_file_with_path,
                         usecols=['ROUTEID', 'MAPPED_IMAGE', 'LATITUDE','LONGITUDE'], dtype=str)
mapping_df.sort_values(by=['ROUTEID', 'MAPPED_IMAGE'], inplace=True, ignore_index=True)
img_input_list = []
df.apply(lambda row: compute_mapping_input(row['MAPPED_IMAGE'], row[model_col_header]), axis=1)
out_df = pd.DataFrame(img_input_list, columns=["ImageBaseName", "lat", "lon", "bearing", "Depth"])
out_df.to_csv(output_file, index=False)
