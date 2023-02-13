import os
import argparse
import pandas as pd
import numpy as np
from pypfm import PFMLoader
import skimage.measure

from utils import ROAD, get_data_from_image, bearing_between_two_latlon_points, split_into_lines, consecutive


SCALING_FACTOR = 25
POLE_WIDTH_THRESHOLD = 10
POLE_ASPECT_RATIO_THRESHOLD = 12
# Depth-Height threshold, e.g., if D < 10, filter out those with H < 500; elif D<25, filter out those with H < 350
D_H_THRESHOLD = {
    10: 500,
    25: 350
}
width_to_hfov = {
    2748: 71.43
}


def compute_mapping_input(mapping_df, input_depth_image_path, mapped_image, path):
    # compute depth of segmented object taking the 10%-trimmed mean of the depths of its constituent pixels
    # to gain robustness with respect to segmentation errors, in particular along the object borders
    mapped_image_df = mapping_df[mapping_df['MAPPED_IMAGE'] == mapped_image]
    if len(mapped_image_df) != 1:
        # no camera location
        print(f'no camera location found for {mapped_image}')
        return
    cam_lat = float(mapped_image_df.iloc[0]['LATITUDE'])
    cam_lon = float(mapped_image_df.iloc[0]['LONGITUDE'])
    # find the next camera lat/lon for computing bearing
    cam_lat2 = float(mapping_df.iloc[mapped_image_df.index + 1]['LATITUDE'])
    cam_lon2 = float(mapping_df.iloc[mapped_image_df.index + 1]['LONGITUDE'])
    image_suffix_list = ('5.png', '1.png', '2.png')
    for suffix in image_suffix_list:
        # get camera location for the mapped image
        input_image_name = os.path.join(path, f'{mapped_image}{suffix}')
        image_width, image_height, input_data = get_data_from_image(input_image_name)
        if image_width not in width_to_hfov:
            print(f'no HFOV can be found for image width {image_width} of the image {input_image_name}')
            continue
        # move ROAD to background in order to get all pole objects
        input_data[input_data == ROAD] = 0
        # perform connected component analysis
        labeled_data, count = skimage.measure.label(input_data, connectivity=2, return_num=True)
        if count > 0:
            object_features = skimage.measure.regionprops(labeled_data)
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
            for i in range(count):
                min_y = object_features[i].bbox[0]
                max_y = object_features[i].bbox[2]
                min_x = object_features[i].bbox[1]
                max_x = object_features[i].bbox[3]
                xdiff = max_x - min_x
                ydiff = max_y - min_y
                if xdiff < POLE_WIDTH_THRESHOLD:
                    # filter out noises
                    continue
                level_indices = np.where(labeled_data == i + 1)
                level_indices_y = level_indices[0]
                level_indices_x = level_indices[1]
                if ydiff / xdiff < POLE_ASPECT_RATIO_THRESHOLD:
                    major_axis_len = object_features[i].major_axis_length
                    minor_axis_len = object_features[i].minor_axis_length
                    if major_axis_len / minor_axis_len < POLE_ASPECT_RATIO_THRESHOLD:
                        # filter out detected short sticks
                        continue
                    else:
                        # connected wires from detected pole make xdiff much bigger than it should,
                        # remove connected wires in order to make accurate centroid computations to get depth info
                        line_indices_y, line_indices_x = split_into_lines(level_indices_y, level_indices_x)
                        # use number of pixels and the first pixel x coordinate for two consecutive lines to determine
                        # whether there are connected wires on the line that need to be removed
                        is_first_line = True
                        for i in range(len(line_indices_x)):
                            split_indices, con_level_indices_x = consecutive(line_indices_x[i])
                            if any(split_indices):
                                # the line is not consecutive, so use the line segment that is closet to the last line
                                # for continuity
                                if is_first_line:
                                    # if the first line is not consecutive, remove this line from the detected object
                                    line_indices_x[i][line_indices_x[i] != 0] = 0
                                    continue

                                # only keep the closest segment while cleaning up other segments with zeros
                                x_dist_to_last_line = 10000
                                closest_seg = None
                                for segment in con_level_indices_x:
                                    x_dist = abs(segment[0] - line_indices_x[i-1][0])
                                    if x_dist < x_dist_to_last_line:
                                        x_dist_to_last_line = x_dist
                                        if closest_seg is not None:
                                            closest_seg[closest_seg != 0] = 0
                                        closest_seg = segment
                                    else:
                                        segment[segment != 0] = 0

                            if is_first_line:
                                is_first_line = False
                                continue
                            # find the first object pixel (with non-zero intensity) in last line
                            last_obj_indices = np.where(line_indices_x[i-1] != 0)[0]
                            last_start_idx = last_obj_indices[0]
                            last_end_idx = last_obj_indices[-1]
                            x_dist = abs(line_indices_x[i][0] - line_indices_x[i-1][last_start_idx])
                            if x_dist > POLE_WIDTH_THRESHOLD:
                                # connected wired are included in the line, remove those added pixels compared to
                                # its previous line
                                if line_indices_x[i][0] < line_indices_x[i-1][last_start_idx]:
                                    line_indices_x[i][line_indices_x[i] < line_indices_x[i-1][last_start_idx]] = 0
                                    # update min_x and xdiff as needed
                                    if line_indices_x[i][0] - min_x <= 1:
                                        obj_indices = np.where(line_indices_x[i] != 0)[0]
                                        if abs(line_indices_x[i][0] - min_x) <= 1:
                                            min_x = obj_indices[0]
                                        elif obj_indices[0] < min_x:
                                            min_x = obj_indices[0]
                                        xdiff = max_x - min_x
                                else:
                                    line_indices_x[i][line_indices_x[i] > line_indices_x[i-1][last_end_idx]] = 0
                                    if max_x - line_indices_x[i][-1] <= 1:
                                        obj_indices = np.where(line_indices_x[i] != 0)[0]
                                        if abs(max_x - line_indices_x[i][-1]) <= 1:
                                            max_x = obj_indices[-1]
                                        elif obj_indices[-1] > max_x:
                                            max_x = obj_indices[-1]
                                        xdiff = max_x - min_x

                trim_size_y = ydiff * 0.01
                trim_size_x = xdiff * 0.01

                if trim_size_y > 0:
                    filtered_level_indices = level_indices_y[((level_indices_y-min_y) > trim_size_y)
                                                              & ((max_y-level_indices_y) > trim_size_y)]
                    if np.size(filtered_level_indices) > 0:
                        average_y = int(np.average(filtered_level_indices))
                    else:
                        continue
                else:
                    # detected pole is too short and treated as FP
                    continue
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
                depth = (1 - depth) * SCALING_FACTOR
                # apply depth-height filtering
                filtered_out = False
                for key, val in D_H_THRESHOLD.items():
                    if depth < key:
                        if ydiff < val:
                            filtered_out = True
                        break
                if filtered_out:
                    continue

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
                img_input_list.append([input_image_base_name, cam_lat, cam_lon, br_angle, depth])


if __name__ == '__main__':
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
    df.apply(lambda row: compute_mapping_input(mapping_df, input_depth_image_path, row['MAPPED_IMAGE'],
                                               row[model_col_header]), axis=1)
    out_df = pd.DataFrame(img_input_list, columns=["ImageBaseName", "lat", "lon", "bearing", "Depth"])
    out_df.to_csv(output_file, index=False)
