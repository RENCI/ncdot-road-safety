import os
import argparse
import pandas as pd
import numpy as np
from pypfm import PFMLoader
import skimage.measure
import cv2
from utils import ROAD, get_data_from_image, get_camera_latlon_and_bearing_for_image_from_mapping, \
    get_depth_data, get_depth_of_pixel, compute_match, bearing_between_two_latlon_points


SCALING_FACTOR = 25
POLE_X_SIZE_THRESHOLD = 10
POLE_Y_SIZE_THRESHOLD = 20
POLE_ASPECT_RATIO_THRESHOLD = 12
POLE_EROSION_DILATION_KERNEL_SIZE = 10
# Depth-Height threshold, e.g., if D < 10, filter out those with H < 500; elif D<25, filter out those with H < 350
D_H_THRESHOLD = {
    17: 500,
    25: 350
}
width_to_hfov = {
    # 2748: 38.92
    2748: 31
}


def extract_lon_lat(geom):
    lon, lat = map(float, geom.strip('POINT ()').split())
    return lon, lat


def compute_mapping_input(mapping_df, input_depth_image_path, depth_image_postfix, mapped_image, path,
                          lidar_file_pattern):
    # compute depth of segmented object taking the 10%-trimmed mean of the depths of its constituent pixels
    # to gain robustness with respect to segmentation errors, in particular along the object borders
    cam_lat, cam_lon, cam_br, _, _, _ = get_camera_latlon_and_bearing_for_image_from_mapping(mapping_df, mapped_image)
    if cam_lat is None:
        # no camera location
        print(f'no camera location found for {mapped_image}')
        return

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
        labeled_data = labeled_data.astype('uint8')
        if count > 0:
            object_features = skimage.measure.regionprops(labeled_data)
            loader = PFMLoader((image_width, image_height), color=False, compress=False)
            input_image_base_name = os.path.basename(os.path.splitext(input_image_name)[0])
            image_pfm = get_depth_data(loader, os.path.join(input_depth_image_path,
                                                            f'{input_image_base_name}{depth_image_postfix}.pfm'))
            # print(f'image_pfm shape: {image_pfm.shape}')
            min_depth = image_pfm.min()
            max_depth = image_pfm.max()
            # input_data[input_data == POLE] = 255
            # updated_image = Image.fromarray(input_data)
            # updated_image.save(os.path.join(path, f'updated_{mapped_image}{suffix}'))

            obj_cnt = 0
            for i in range(count):
                xdiff = object_features[i].bbox[3] - object_features[i].bbox[1]
                ydiff = object_features[i].bbox[2] - object_features[i].bbox[0]

                if xdiff <= POLE_X_SIZE_THRESHOLD or ydiff <= POLE_Y_SIZE_THRESHOLD:
                    # filter out noises or non-straight pole-like objects
                    continue

                y0, x0 = object_features[i].centroid
                depth = get_depth_of_pixel(y0, x0, image_pfm, min_depth, max_depth, scaling=SCALING_FACTOR)

                if ydiff / xdiff < POLE_ASPECT_RATIO_THRESHOLD:
                    major_axis_len = object_features[i].major_axis_length
                    minor_axis_len = object_features[i].minor_axis_length
                    if major_axis_len / minor_axis_len < POLE_ASPECT_RATIO_THRESHOLD:
                        # filter out detected short sticks
                        continue
                    # connected wires from detected pole make xdiff much bigger than it should,
                    # remove connected wires in order to make accurate centroid computations to get depth info
                    binary_labeled_data = np.copy(labeled_data)
                    binary_labeled_data[binary_labeled_data == i + 1] = 255
                    binary_labeled_data[binary_labeled_data != 255] = 0
                    # Define the structuring element for erosion and dilation
                    kernel = np.ones((POLE_EROSION_DILATION_KERNEL_SIZE, POLE_EROSION_DILATION_KERNEL_SIZE), np.uint8)
                    # apply erosion
                    img_erosion = cv2.erode(binary_labeled_data, kernel, iterations=1)
                    # apply dilation to restore the regions
                    img_dilation = cv2.dilate(img_erosion, kernel, iterations=1)
                    # use the resulting image with erosion followed by dilation as a mask to
                    obj_only = cv2.bitwise_and(labeled_data, img_dilation)

                    if len(np.unique(obj_only)) <= 1:
                        # The object gets filtered out, so discard it
                        continue
                    # need to recompute properties of the object
                    updated_object_features = skimage.measure.regionprops(obj_only)
                    y0, x0 = updated_object_features[0].centroid
                    depth = get_depth_of_pixel(y0, x0, image_pfm, min_depth, max_depth, scaling=SCALING_FACTOR)
                    object_features[i] = updated_object_features[0]

                # apply depth-height filtering
                filtered_out = False
                for key, val in D_H_THRESHOLD.items():
                    if depth < key:
                        if ydiff < val:
                            filtered_out = True
                        break
                if filtered_out:
                    continue

                ref_bearing = cam_br
                if suffix == '1.png':
                    # front view image
                    # check if lidar project info is available for this image
                    lidar_file_name = lidar_file_pattern.format(f'{mapped_image}{suffix[0]}')
                    if os.path.exists(lidar_file_name):
                        lidar_df = pd.read_csv(lidar_file_name, usecols=['ROAD_X', 'ROAD_Y', 'BEARING',
                                                                         'geometry_y'])
                        lidar_df[['lon', 'lat']] = lidar_df['geometry_y'].apply(lambda x: pd.Series(extract_lon_lat(x)))

                        # find the nearest LIDAR projected point from the pole ground location
                        # (x0, object_features[i].bbox[2])
                        obj_depth = get_depth_of_pixel(object_features[i].bbox[2], x0,
                                                       image_pfm, min_depth, max_depth, scaling=SCALING_FACTOR)
                        print(f'obj_depth: {obj_depth}, depth: {depth}')
                        lidar_df['ROAD_Z'] = lidar_df.apply(lambda row: get_depth_of_pixel(
                            row['ROAD_Y'], row['ROAD_X'], image_pfm, min_depth, max_depth, scaling=SCALING_FACTOR),
                                                            axis=1)
                        lidar_df['DIFF_ROAD_Z'] = lidar_df.apply(lambda row: abs(depth - row['ROAD_Z']),
                                                                 axis=1)
                        sub_lidar_df = lidar_df[lidar_df['DIFF_ROAD_Z'] <= 1].reset_index(drop=True)
                        nearest_idx = compute_match(x0, object_features[i].bbox[2],
                                                    sub_lidar_df['ROAD_X'], sub_lidar_df['ROAD_Y'])[0]
                        print(sub_lidar_df.iloc[nearest_idx])
                        ref_bearing = bearing_between_two_latlon_points(cam_lat, cam_lon,
                                                                        sub_lidar_df.iloc[nearest_idx].lat,
                                                                        sub_lidar_df.iloc[nearest_idx].lon,
                                                                        is_degree=True)
                        ref_x = sub_lidar_df.iloc[nearest_idx].ROAD_X
                        print(f'input_image_base_name: {input_image_base_name}, x0: {x0}, ref_x: {ref_x}, '
                              f'closet lidar lat: {sub_lidar_df.iloc[nearest_idx].lat}, '
                              f'lon: {sub_lidar_df.iloc[nearest_idx].lon}')
                        hangle = (abs(x0 - ref_x)/image_width) * width_to_hfov[image_width]
                    else:
                        ref_x = image_width/2
                        hangle = (abs(x0 - ref_x)/image_width) * width_to_hfov[image_width]
                    minus_bearing = True if x0 < ref_x else False
                    print(f'ref_bearing: {ref_bearing}, ref_x: {ref_x}, hangle: {hangle}, minus_bearing: {minus_bearing}')
                elif suffix == '5.png':
                    # left view image
                    minus_bearing = True
                    # addition of 0.5 is needed to account for the front view image
                    hangle = ((image_width - x0)/image_width + 0.5) * width_to_hfov[image_width]
                else:
                    # right view image
                    minus_bearing = False
                    # addition of 0.5 is needed to account for the front view image
                    hangle = (x0 / image_width + 0.5) * width_to_hfov[image_width]

                br_angle = (ref_bearing - hangle) if minus_bearing else (ref_bearing + hangle)
                br_angle = (br_angle + 360) % 360
                img_input_list.append([input_image_base_name, cam_lat, cam_lon, x0, y0, br_angle, depth])
                # if input_image_base_name == '926005420241':
                #    labeled_data[labeled_data == 1 ] = 255
                #    save_data_to_image(labeled_data, f'{input_image_base_name}_processed.png')
                print(f'{input_image_base_name}, ori: {object_features[i].orientation}, '
                      f'minx: {object_features[i].bbox[1]}, maxx: {object_features[i].bbox[3]}, '
                      f'miny: {object_features[i].bbox[0]}, maxy: {object_features[i].bbox[2]}, '
                      f'xdiff: {object_features[i].bbox[3] - object_features[i].bbox[1]}, '
                      f'ydiff: {object_features[i].bbox[2] - object_features[i].bbox[0]}, cam_br:{cam_br}, '
                      f'br_angle: {br_angle}, depth: {depth}')
                obj_cnt += 1
            if obj_cnt > 0:
                print(f'pole count: {obj_cnt}, mapped_image: {mapped_image}')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Process arguments.')
    parser.add_argument('--input_seg_map_info_with_path', type=str,
                        # default='/projects/ncdot/test_route_segmentation/test_route_road_pole_labels.csv',
                        default='data/d13_route_40001001011/other/test_route_road_pole_labels_test_image.csv',
                        help='input csv file that includes input segmented image path and name for computing depth')
    parser.add_argument('--route_id', type=str, default='40001001011',
                        help='route id to filter input_seg_map_info_with_path data with')
    parser.add_argument('--model_col_header', type=str, default='ONEFORMER',
                        help='input model column header in the input_seg_map_info_with_path to get segmentation path')
    parser.add_argument('--input_sensor_mapping_file_with_path', type=str,
                        # default='/projects/ncdot/secondary_road/output/d13/mapped_2lane_sr_images_d13.csv',
                        default='data/d13_route_40001001011/other/mapped_2lane_sr_images_d13.csv',
                        help='input csv file that includes mapped image lat/lon info')
    parser.add_argument('--input_depth_image_path', type=str,
                        default='../midas/images/output',
                        help='input path that includes depth prediction output images')
    parser.add_argument('--input_depth_image_postfix', type=str,
                        default='-dpt_beit_large_512',
                        help='input depth prediction output image postfix to concatenate with image basename')
    parser.add_argument('--lidar_project_info_file_pattern', type=str,
                        default='data/d13_route_40001001011/oneformer/output/aerial_lidar_test/'
                                'lidar_project_info_{}.csv',
                        help='input LIDAR projection info file pattern')
    parser.add_argument('--output_file', type=str,
                        # default='/projects/ncdot/geotagging/input/oneformer/route_40001001011_segment_object_mapping_input.csv',
                        default='data/d13_route_40001001011/oneformer/output/aerial_lidar_test/'
                                'test_mapping_input.csv',
                        help='output file that contains image base names and corresponding segmented object depths')


    args = parser.parse_args()
    input_seg_map_info_with_path = args.input_seg_map_info_with_path
    route_id = args.route_id
    model_col_header = args.model_col_header
    input_sensor_mapping_file_with_path = args.input_sensor_mapping_file_with_path
    input_depth_image_path = args.input_depth_image_path
    input_depth_image_postfix = args.input_depth_image_postfix
    lidar_project_info_file_pattern = args.lidar_project_info_file_pattern
    output_file = args.output_file

    df = pd.read_csv(input_seg_map_info_with_path, index_col=None,
                     usecols=['ROUTEID', 'MAPPED_IMAGE', model_col_header], dtype=str)
    if route_id:
        df = df[df.ROUTEID == route_id]

    mapping_df = pd.read_csv(input_sensor_mapping_file_with_path,
                             usecols=['ROUTEID', 'MAPPED_IMAGE', 'LATITUDE','LONGITUDE'], dtype=str)
    mapping_df.sort_values(by=['ROUTEID', 'MAPPED_IMAGE'], inplace=True, ignore_index=True)
    img_input_list = []
    df.apply(lambda row: compute_mapping_input(mapping_df, input_depth_image_path, input_depth_image_postfix,
                                               row['MAPPED_IMAGE'], row[model_col_header],
                                               lidar_project_info_file_pattern), axis=1)
    out_df = pd.DataFrame(img_input_list, columns=["imageBaseName", "lat", "lon", "x", "y", "bearing", "depth"])
    out_df.to_csv(output_file, index=False)
