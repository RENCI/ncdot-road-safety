import os
import sys
import argparse
import pandas as pd
import numpy as np
from pypfm import PFMLoader
import skimage.measure
import cv2
from math import sqrt, atan2, degrees
from utils import SegmentationClass, get_data_from_image, get_camera_latlon_and_bearing_for_image_from_mapping, \
    get_depth_data, get_depth_of_pixel, compute_match, bearing_between_two_latlon_points, \
    add_lidar_x_y_from_lat_lon, LIDARClass
from align_segmented_road_with_lidar import transform_to_world_coordinate_system, INIT_CAMERA_PARAMS, \
    CAMERA_LIDAR_X_OFFSET, CAMERA_LIDAR_Y_OFFSET, CAMERA_LIDAR_Z_OFFSET, CAMERA_YAW, CAMERA_PITCH, CAMERA_ROLL


# may need to be updated (e.g., set to 25) in conjunction with MAX_OBJ_DIST_FROM_CAM set in object_mapping.py
SCALING_FACTOR = 55
POLE_X_SIZE_THRESHOLD = 10
POLE_Y_SIZE_THRESHOLD = 20
POLE_ASPECT_RATIO_THRESHOLD = 10  # 12
POLE_EROSION_DILATION_KERNEL_SIZE = 10
# Depth-Height threshold, e.g., if D < 10, filter out those with H < 500; elif D<25, filter out those with H < 350
D_H_THRESHOLD = {
    17: 500,
    25: 210  # 350
}
width_to_hfov = {
    2748: 24.86,
    2356: 38.19
}


def extract_lon_lat(geom):
    lon, lat = map(float, geom.strip('POINT ()').split())
    return lon, lat


def compute_mapping_input(mdf, input_depth_image, depth_image_postfix, mapped_image, path,
                          lidar_file_pattern, cam_paras_file_pattern):
    # compute depth of segmented object taking the 10%-trimmed mean of the depths of its constituent pixels
    # to gain robustness with respect to segmentation errors, in particular along the object borders
    cam_lat, cam_lon, cam_br, cam_lat2, cam_lon2, _ = get_camera_latlon_and_bearing_for_image_from_mapping(mdf,
                                                                                                           mapped_image)
    if cam_lat is None:
        # no camera location
        print(f'no camera location found for {mapped_image}')
        return

    if front_only:
        image_suffix_list = ('1.png', )
    else:
        image_suffix_list = ('5.png', '1.png', '2.png')

    for suffix in image_suffix_list:
        # get camera location for the mapped image
        input_image_name = os.path.join(path, f'{mapped_image}{suffix}')
        image_width, image_height, input_data = get_data_from_image(input_image_name)
        if image_width not in width_to_hfov:
            print(f'no HFOV can be found for image width {image_width} of the image {input_image_name}')
            continue
        # move other classes to background in order to get all pole objects
        input_data[input_data != SegmentationClass.POLE.value] = 0
        # perform connected component analysis
        labeled_data, count = skimage.measure.label(input_data, connectivity=2, return_num=True)
        labeled_data = labeled_data.astype('uint8')
        if count > 0:
            object_features = skimage.measure.regionprops(labeled_data)
            loader = PFMLoader((image_width, image_height), color=False, compress=False)
            input_image_base_name = os.path.basename(os.path.splitext(input_image_name)[0])
            image_pfm = get_depth_data(loader, os.path.join(input_depth_image,
                                                            f'{input_image_base_name}{depth_image_postfix}.pfm'))
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
                    if lidar_file_pattern:
                        lidar_file_name = lidar_file_pattern.format(f'{mapped_image}{suffix[0]}')
                    else:
                        lidar_file_name = ''
                    if cam_paras_file_pattern:
                        cam_paras_file = cam_paras_file_pattern.format(f'{mapped_image}{suffix[0]}')
                    else:
                        cam_paras_file = ''
                    if cam_paras_file and os.path.exists(cam_paras_file):
                        cam_para_df = pd.read_csv(cam_paras_file)
                        # transform cam_lat2, cam_lon2 using specified camera pose parameters
                        cam_df = pd.DataFrame(data={'LATITUDE': [cam_lat, cam_lat2], 'LONGITUDE': [cam_lon, cam_lon2]})
                        cam_gdf = add_lidar_x_y_from_lat_lon(cam_df)
                        proj_cam_x = cam_gdf.iloc[0].x
                        proj_cam_y = cam_gdf.iloc[0].y
                        proj_cam_x2 = cam_gdf.iloc[1].x
                        proj_cam_y2 = cam_gdf.iloc[1].y
                        point_z = -sqrt((proj_cam_x2 - proj_cam_x) ** 2 + (proj_cam_y2 - proj_cam_y) ** 2)
                        cam_bearing_df = pd.DataFrame(data={'INITIAL_WORLD_X': [0],
                                                            'INITIAL_WORLD_Y': [cam_para_df.iloc[0]['diff_z']],
                                                            'INITIAL_WORLD_Z': [point_z]})
                        cam_para_list = INIT_CAMERA_PARAMS.copy()
                        cam_para_list[CAMERA_LIDAR_X_OFFSET] = cam_para_df.iloc[0]['translation_x']
                        cam_para_list[CAMERA_LIDAR_Y_OFFSET] = cam_para_df.iloc[0]['translation_y']
                        cam_para_list[CAMERA_LIDAR_Z_OFFSET] = cam_para_df.iloc[0]['translation_z']
                        cam_para_list[CAMERA_YAW] = cam_para_df.iloc[0]['rotation_x']
                        cam_para_list[CAMERA_PITCH] = cam_para_df.iloc[0]['rotation_y']
                        cam_para_list[CAMERA_ROLL] = cam_para_df.iloc[0]['rotation_z']
                        cam_bearing_df = transform_to_world_coordinate_system(cam_bearing_df, cam_para_list)
                        delta_bearing = degrees(atan2(cam_bearing_df.iloc[0]['WORLD_X'],
                                                      -cam_bearing_df.iloc[0]['WORLD_Z']))
                        ref_bearing += delta_bearing

                    if lidar_file_name and os.path.exists(lidar_file_name):
                        lidar_df = pd.read_csv(lidar_file_name, usecols=['PROJ_SCREEN_X', 'PROJ_SCREEN_Y',
                                                                         'ROAD_X', 'ROAD_Y', 'BEARING',
                                                                         'geometry_y', 'Z', 'C'])
                        lidar_df[['lon', 'lat']] = lidar_df['geometry_y'].apply(lambda x: pd.Series(extract_lon_lat(x)))

                        # find the nearest LIDAR projected point from the pole ground location
                        # (x0, object_features[i].bbox[2])
                        nearest_idx, nearest_dist = compute_match(x0, object_features[i].bbox[2],
                                                                  lidar_df['PROJ_SCREEN_X'], lidar_df['PROJ_SCREEN_Y'])
                        print(f'nearest_idx: {nearest_idx}, nearest_dist: {nearest_dist}, ldf: {lidar_df.iloc[nearest_idx]}')
                        # see if there are LIDAR points projected within the object bounding box
                        filtered_lidar_df = lidar_df[
                            ((lidar_df.C == LIDARClass.MEDIUM_VEG.value) | (lidar_df.C == LIDARClass.HIGH_VEG.value)) &
                            (lidar_df['PROJ_SCREEN_X'] >= object_features[i].bbox[1]) &
                            (lidar_df['PROJ_SCREEN_X'] <= object_features[i].bbox[3]) &
                            (lidar_df['PROJ_SCREEN_Y'] >= object_features[i].bbox[0]) &
                            (lidar_df['PROJ_SCREEN_Y'] <= object_features[i].bbox[2])]
                        if len(filtered_lidar_df) > 0:
                            nearest_fidx, nearest_fdist = compute_match(x0, y0,
                                                                        filtered_lidar_df['PROJ_SCREEN_X'],
                                                                        filtered_lidar_df['PROJ_SCREEN_Y'])
                            # compare the distance between nearest_fidx to all pole pixels with nearest_dist
                            # to determine whether to use nearest_fidx or nearest_idx
                            obj_feat_df = pd.DataFrame(data=object_features[i].coords, columns=['Y', 'X'])
                            _, nearest_fdist = compute_match(lidar_df.iloc[nearest_fidx].PROJ_SCREEN_X,
                                                             lidar_df.iloc[nearest_fidx].PROJ_SCREEN_Y,
                                                             obj_feat_df['X'], obj_feat_df['Y'])
                            print(f'nearest_fidx: {nearest_fidx}, nearest_fdist: {nearest_fdist}')
                            if nearest_fdist < nearest_dist:
                                # use closest LIDAR data lying inside pole bounding box instead of closest LIDAR point
                                # to the lowest pole pixel
                                nearest_idx = nearest_fidx
                                print(f'nearest filtered ldf: {lidar_df.iloc[nearest_idx]}')

                        print(lidar_file_name, nearest_idx)
                        ref_bearing = bearing_between_two_latlon_points(cam_lat, cam_lon,
                                                                        lidar_df.iloc[nearest_idx].lat,
                                                                        lidar_df.iloc[nearest_idx].lon,
                                                                        is_degree=True)
                        # use ref_bearing only without accounting for any offset since the nearest LIDAR
                        # point should be the point that is hit by the ray cast from camera to object if the
                        # LIDAR raster grid has enough resolution
                        ref_x = lidar_df.iloc[nearest_idx].PROJ_SCREEN_X
                        hangle = 0
                    else:
                        ref_x = image_width / 2
                        hangle = (abs(x0 - ref_x)/image_width) * width_to_hfov[image_width]
                    minus_bearing = True if x0 < ref_x else False
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
                img_input_list.append([input_image_base_name, cam_lat, cam_lon, int(x0 + 0.5), int(y0 + 0.5),
                                       br_angle, depth])
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
                        # default='data/d13_route_40001001011/other/test_route_road_pole_labels_test_image.csv',
                        default='data/new_test_scene/test_route_road_pole_labels_test_images.csv',
                        help='input csv file that includes input segmented image path and name for computing depth')
    parser.add_argument('--route_id', type=str,
                        # default='40001001011',
                        default='40001001012',
                        help='route id to filter input_seg_map_info_with_path data with')
    parser.add_argument('--model_col_header', type=str, default='ONEFORMER',
                        help='input model column header in the input_seg_map_info_with_path to get segmentation path')
    parser.add_argument('--input_sensor_mapping_file_with_path', type=str,
                        # default='/projects/ncdot/secondary_road/output/d13/mapped_2lane_sr_images_d13.csv',
                        default='data/d13_route_40001001011/other/mapped_2lane_sr_images_d13.csv',
                        help='input csv file that includes mapped image lat/lon info')
    parser.add_argument('--input_depth_image_path', type=str,
                        default='../midas/images/output/new_test_scene',
                        # default='../midas/images/output/d13_route_40001001011',
                        help='input path that includes depth prediction output images')
    parser.add_argument('--input_depth_image_postfix', type=str,
                        default='-dpt_beit_large_512',
                        help='input depth prediction output image postfix to concatenate with image basename')
    parser.add_argument('--lidar_project_info_file_pattern', type=str,
                        default='data/new_test_scene/output/lidar_project_info_{}.csv',
                        # default='data/d13_route_40001001011/oneformer/output/all_lidar_vertices/lidar_project_info_{}.csv',
                        help='input LIDAR projection info file pattern')
    parser.add_argument('--lidar_project_cam_params_pattern', type=str,
                        # default='data/new_test_scene/output/lidar_project_info_{}_cam_paras.csv',
                        default='',
                        help='input LIDAR projection info file pattern')
    parser.add_argument('--output_file', type=str,
                        # default='data/d13_route_40001001011/oneformer/output/all_lidar_vertices/test_mapping_input.csv',
                        default='data/new_test_scene/output/test_mapping_input.csv',
                        help='output file that contains image base names and corresponding segmented object depths')
    parser.add_argument('--front_only', action="store_true",
                        help='whether to compute mapping inputs for front view images only')


    args = parser.parse_args()
    input_seg_map_info_with_path = args.input_seg_map_info_with_path
    route_id = args.route_id
    model_col_header = args.model_col_header
    input_sensor_mapping_file_with_path = args.input_sensor_mapping_file_with_path
    input_depth_image_path = args.input_depth_image_path
    input_depth_image_postfix = args.input_depth_image_postfix
    lidar_project_info_file_pattern = args.lidar_project_info_file_pattern
    lidar_project_cam_params_pattern = args.lidar_project_cam_params_pattern
    output_file = args.output_file
    front_only = args.front_only

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
                                               lidar_project_info_file_pattern,
                                               lidar_project_cam_params_pattern), axis=1)
    out_df = pd.DataFrame(img_input_list, columns=["imageBaseName", "lat", "lon", "x", "y", "bearing", "depth"])
    out_df.to_csv(output_file, index=False)
    sys.exit(0)
