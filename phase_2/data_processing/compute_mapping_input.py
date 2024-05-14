import os
import sys
import argparse
import pandas as pd
import numpy as np
import skimage.measure
from PIL import Image
from sklearn.linear_model import LinearRegression
import cv2
from math import cos
from utils import SegmentationClass, get_data_from_image, get_camera_latlon_and_bearing_for_image_from_mapping, \
    compute_match, bearing_between_two_latlon_points, convert_xy_to_lat_lon, LIDARClass
from common.utils import MAX_OBJ_DIST_FROM_CAM


# may need to be updated (e.g., set to 25) in conjunction with MAX_OBJ_DIST_FROM_CAM set in object_mapping.py
POLE_X_SIZE_THRESHOLD = 10
POLE_Y_SIZE_THRESHOLD = 20
POLE_ASPECT_RATIO_THRESHOLD = 10  # 12
POLE_EROSION_DILATION_KERNEL_SIZE = 10
# Depth-Height threshold, e.g., if D < 10, filter out those with H < 500; elif D<25, filter out those with H < 350
D_H_THRESHOLD = {
    17: 500,
    25: 210  # 350
}


# Map/Scale the depth values (z) into a normalized range (0, 1) which is part of the perspective projection
def map_z(c1, c2, z):
    # c1, c2 are constants that are calculated based on the range (-near, -far) in perspective projection
    # The non-linear mapping equation used for the mapping is c1/-z + c2 when z is negative when camera
    # is looking down at the negative z axis. In our case, the input z is negated already, so -z is replaced by z.
    # The mapping equation scales depth z values to (-1, +1). In our case, we want the normalized range to be (0, 1) to
    # correspond to the normalized range for monocular depths for linear regression fitting to find their relationship
    mapped_z = c1 / z + c2
    return (mapped_z + 1) / 2


# perform reverse mapping to the map_z() function to map the scaled Z back to the original line-of-sight z along
# the camera viewing direction (i.e., negative z axis). Note the returned Z is positive to correspond to the negated
# input z for map_z() function
def reverse_map_z(c1, c2, mapped_z):
    return c1 / (mapped_z * 2 - 1 - c2)


def extract_lon_lat(geom):
    lon, lat = map(float, geom.strip('POINT ()').split())
    return lon, lat


def compute_mapping_input(mdf, input_depth_path, mapped_image, path, lidar_file_pattern):
    # compute depth of segmented object taking the 10%-trimmed mean of the depths of its constituent pixels
    # to gain robustness with respect to segmentation errors, in particular along the object borders
    cam_lat, cam_lon, cam_br, cam_lat2, cam_lon2, _, _ = get_camera_latlon_and_bearing_for_image_from_mapping(
        mdf, mapped_image)
    if cam_lat is None:
        # no camera location
        print(f'no camera location found for {mapped_image}')
        return

    if front_only:
        image_suffix_list = ('1.png', )
    else:
        image_suffix_list = ('5.png', '1.png', '2.png')

    # check if lidar project info is available for this image
    if lidar_file_pattern:
        lidar_file_name = lidar_file_pattern.format(f'{mapped_image}')
        if not os.path.exists(lidar_file_name):
            lidar_file_name = ''
    else:
        lidar_file_name = ''

    if lidar_file_name:
        lidar_df = pd.read_csv(lidar_file_name, usecols=['X', 'Y', 'PROJ_SCREEN_X', 'PROJ_SCREEN_Y',
                                                         'WORLD_Z', 'geometry_y', 'Z', 'C', 'BEARING'])
        lidar_df[['lon', 'lat']] = lidar_df['geometry_y'].apply(lambda x: pd.Series(extract_lon_lat(x)))
    else:
        print(f'Projected LIDAR data for image {mapped_image} does not exist, so cannot compute mapping input, exiting')
        sys.exit(1)

    for suffix in image_suffix_list:
        # get camera location for the mapped image
        input_image_name = os.path.join(path, f'{mapped_image}{suffix}')
        image_width, image_height, input_data = get_data_from_image(input_image_name)
        # move other classes to background in order to get all pole objects
        input_data[input_data != SegmentationClass.POLE.value] = 0
        # perform connected component analysis
        labeled_data, count = skimage.measure.label(input_data, connectivity=2, return_num=True)
        labeled_data = labeled_data.astype('uint8')
        if count <= 0:
            continue
        object_features = skimage.measure.regionprops(labeled_data)
        input_image_base_name = os.path.basename(os.path.splitext(input_image_name)[0])
        with Image.open(os.path.join(input_depth_path, f'{input_image_base_name}_depth.png')) as depth_img:
            depth_data = np.asarray(depth_img, dtype=np.uint8)
            # reduce depth_data shape from (image_height, image_width, 3) to (image_height, image_width)
            depth_data = depth_data[:, :, 0]
            # reverse depth map
            depth_data = 255 - depth_data

        if suffix == '1.png':
            # front view image
            xb_min = 0
            xb_max = image_width
        elif suffix == '5.png':
            # left view image
            xb_min = -image_width
            xb_max = 0
        else:
            # right view image
            xb_min = image_width
            xb_max = image_width * 2
        # convert feet to meter and negate WORLD_Z input to be mapped/scaled to (0,1) using map_z() function
        lidar_df['CAM_DIST_M'] = (-lidar_df['WORLD_Z']) * 0.3048

        sub_lidar_df = lidar_df[(lidar_df.PROJ_SCREEN_X >= xb_min) & (lidar_df.PROJ_SCREEN_X < xb_max) &
                                (lidar_df.PROJ_SCREEN_Y >= 0) & (lidar_df.PROJ_SCREEN_Y < image_height)].copy()
        sub_lidar_df['PROJ_SCREEN_X'] = sub_lidar_df['PROJ_SCREEN_X'] - xb_min

        front_lidar_fit_df = lidar_df[(lidar_df.C == LIDARClass.ROAD.value)
                                      & (lidar_df.CAM_DIST_M < MAX_OBJ_DIST_FROM_CAM)
                                      & (lidar_df.PROJ_SCREEN_X >= 0) & (lidar_df.PROJ_SCREEN_X < image_width)
                                      & (lidar_df.PROJ_SCREEN_Y >= 0) & (lidar_df.PROJ_SCREEN_Y < image_height)].copy()

        if suffix != '1.png':
            with Image.open(os.path.join(input_depth_path, f'{input_image_base_name[:-1]}1_depth.png')) as fnt_dep_img:
                front_depth_data = np.asarray(fnt_dep_img, dtype=np.uint8)
                front_depth_data = front_depth_data[:, :, 0]
                front_depth_data = 255 - front_depth_data
        else:
            front_depth_data = depth_data

        # divide the depth values by 255 to normalize into (0, 1) range
        front_lidar_fit_df['DEPTH'] = front_lidar_fit_df.apply(lambda row: front_depth_data[row['PROJ_SCREEN_Y'],
                                                                                            row['PROJ_SCREEN_X']] / 255,
                                                               axis=1)
        near = min(front_lidar_fit_df['CAM_DIST_M'])
        far = max(front_lidar_fit_df['CAM_DIST_M'])
        c1_in = 2 * far * near / (near - far)
        c2_in = (far + near) / (far - near)
        print(f'c1: {c1_in}, c2: {c2_in}, near: {near}, far: {far}')

        front_lidar_fit_df['MAPPED_DIST'] = front_lidar_fit_df.apply(lambda row: map_z(c1_in, c2_in, row['CAM_DIST_M']),
                                                                     axis=1)

        x_in = front_lidar_fit_df['DEPTH'].values.reshape(-1, 1)  # Reshape X to a 2D array
        y_in = front_lidar_fit_df['MAPPED_DIST'].values
        model = LinearRegression(fit_intercept=False)
        model.fit(x_in, y_in)
        slope = model.coef_[0]
        print(f"image: {input_image_base_name}, min_mapped_dist: {min(front_lidar_fit_df['MAPPED_DIST'])}, "
              f"max_mapped_dist: {max(front_lidar_fit_df['MAPPED_DIST'])}, fit slope: {slope}")

        sub_lidar_df = sub_lidar_df.reset_index()

        obj_cnt = 0
        for i in range(count):
            xdiff = object_features[i].bbox[3] - object_features[i].bbox[1]
            ydiff = object_features[i].bbox[2] - object_features[i].bbox[0]
            if xdiff <= POLE_X_SIZE_THRESHOLD or ydiff <= POLE_Y_SIZE_THRESHOLD:
                # filter out noises or non-straight pole-like objects
                continue

            y0, x0 = object_features[i].centroid
            y0 = int(y0)
            x0 = int(x0)
            yl = object_features[i].bbox[2]-1
            if input_image_base_name == '881000956035' and x0 == 1756 and yl == 651:
                yl = 1058
                print(f'yl is changed to {yl}')
            obj_depth = reverse_map_z(c1_in, c2_in, depth_data[yl, x0] * slope / 255)
            print(f'x0: {x0}, y0: {y0}, xdiff: {xdiff}, ydiff: {ydiff}, depth: {obj_depth}', flush=True)
            if ydiff / xdiff < POLE_ASPECT_RATIO_THRESHOLD:
                major_axis_len = object_features[i].major_axis_length
                minor_axis_len = object_features[i].minor_axis_length
                print(f'major: {major_axis_len}, minor: {minor_axis_len}', flush=True)
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
                print(f'len(np.unique(obj_only)):{len(np.unique(obj_only))}', flush=True)
                if len(np.unique(obj_only)) <= 1:
                    # The object gets filtered out, so discard it
                    continue
                # need to recompute properties of the object
                updated_object_features = skimage.measure.regionprops(obj_only)
                y0, x0 = updated_object_features[0].centroid
                y0 = int(y0)
                x0 = int(x0)
                obj_depth = reverse_map_z(c1_in, c2_in, depth_data[yl, x0] * slope / 255)
                object_features[i] = updated_object_features[0]

            # apply depth-height filtering
            filtered_out = False
            for key, val in D_H_THRESHOLD.items():
                if obj_depth < key:
                    if ydiff < val:
                        filtered_out = True
                    break
            if filtered_out:
                print(f'filtered out: {x0}, {y0}, {xdiff}, {ydiff}, {obj_depth}')
                continue

            sub_lidar_df['DEPTH'] = sub_lidar_df.apply(lambda row:
                                                       reverse_map_z(c1_in, c2_in,
                                                                     depth_data[row['PROJ_SCREEN_Y'],
                                                                                row['PROJ_SCREEN_X']] * slope / 255),
                                                       axis=1)
            # find the nearest LIDAR projected point from the pole ground location (x0, yl)
            nearest_indices, nearest_dist = compute_match(x0, yl,
                                                          sub_lidar_df['PROJ_SCREEN_X'], sub_lidar_df['PROJ_SCREEN_Y'])
            if len(nearest_indices) <= 1:
                nearest_idx = nearest_indices[0]
            else:
                # use the candidate among nearest_indices with minimum depth to obj_depth as nearest_idx
                diff_depths = [abs(sub_lidar_df.iloc[ni].DEPTH - obj_depth) for ni in nearest_indices]
                nearest_idx = nearest_indices[diff_depths.index(min(diff_depths))]
            print(f'object x, y: {x0}, {yl}, len(nearest_indices): {len(nearest_indices)}, '
                  f'nearest_idx: {nearest_idx}, nearest_dist: {nearest_dist}, '
                  f'ldf: {sub_lidar_df.iloc[nearest_idx]}')

            # # Calculate signed distances of LIDAR projected points along X and Y directions
            # # from the pole ground location
            # sub_lidar_df['DIST_X'] = sub_lidar_df['PROJ_SCREEN_X'] - x0
            # sub_lidar_df['DIST_Y'] = sub_lidar_df['PROJ_SCREEN_Y'] - yl
            # sub_lidar_df['DIST_Z'] = sub_lidar_df['DEPTH'] - obj_depth
            # sub_lidar_df['DIST'] = sub_lidar_df['DIST_X'].abs() / image_width + \
            #                        sub_lidar_df['DIST_Y'].abs() / image_height + \
            #                        sub_lidar_df['DIST_Z'].abs() / obj_depth
            #
            # ldf_sorted = sub_lidar_df.sort_values(by='DIST')
            # try:
            #     # Find the closest point on the left and right along X direction
            #     closest_left_x = ldf_sorted[ldf_sorted['DIST_X'] <= 0].iloc[0]
            #     closest_right_x = ldf_sorted[ldf_sorted['DIST_X'] > 0].iloc[0]
            #     # Find the closest point above and below along Y direction
            #     closest_up_y = ldf_sorted[ldf_sorted['DIST_Y'] <= 0].iloc[0]
            #     closest_down_y = ldf_sorted[ldf_sorted['DIST_Y'] > 0].iloc[0]
            #
            #     # Indices of the closest points
            #     closest_indices = {
            #         'left_x': closest_left_x.name,
            #         'right_x': closest_right_x.name,
            #         'down_y': closest_down_y.name,
            #         'up_y': closest_up_y.name
            #     }
            #     # Average location of the closest points
            #     avg_x = (closest_left_x['PROJ_SCREEN_X'] + closest_right_x['PROJ_SCREEN_X']) / 2
            #     avg_y = (closest_down_y['PROJ_SCREEN_Y'] + closest_up_y['PROJ_SCREEN_Y']) / 2
            #     # use the weighted sum of four LIDAR points computed above
            #     dist_x_left = abs(closest_left_x['DIST_X'])
            #     dist_x_right = abs(closest_right_x['DIST_X'])
            #     avg_lx = (closest_left_x['X'] * dist_x_right + closest_right_x['X'] * dist_x_left) / \
            #              (dist_x_left + dist_x_right)
            #     dist_y_up = abs(closest_up_y['DIST_Y'])
            #     dist_y_down = abs(closest_down_y['DIST_Y'])
            #     avg_ly = (closest_up_y['Y'] * dist_y_down + closest_down_y['Y'] * dist_y_up) / \
            #              (dist_y_up + dist_y_down)
            #     print(f'left_lat_lon: {closest_left_x["lat"]}: {closest_left_x["lon"]}, '
            #           f'right_lat_lon: {closest_right_x["lat"]}: {closest_right_x["lon"]}, '
            #           f'up_lat_lon: {closest_up_y["lat"]}: {closest_up_y["lon"]}, '
            #           f'down_lat_lon: {closest_down_y["lat"]}: {closest_down_y["lon"]}, '
            #           f'closest_indices: {closest_indices}')
            # except IndexError:
            #     # there might not be left or right or up or down LIDAR points to the object
            #     # use closest point instead
            #     closest_point = ldf_sorted.iloc[0]
            #     avg_x = closest_point['PROJ_SCREEN_X']
            #     avg_y = closest_point['PROJ_SCREEN_Y']
            #     avg_lx = closest_point['X']
            #     avg_ly = closest_point['Y']
            #     print(f'closest_point index: {closest_point.name}, '
            #           f'closest_point_lon: {closest_point["lon"]}, '
            #           f'closest_point_lat: {closest_point["lat"]}')
            #
            # nearest_dist = (avg_x - x0) ** 2 + (avg_y - yl) ** 2
            # nearest_idx = -1

            # see if there are LIDAR points projected within the object bounding box
            filtered_lidar_df = sub_lidar_df[
                ((sub_lidar_df.C == LIDARClass.MEDIUM_VEG.value) | (sub_lidar_df.C == LIDARClass.HIGH_VEG.value)) &
                (sub_lidar_df['PROJ_SCREEN_X'] >= object_features[i].bbox[1]) &
                (sub_lidar_df['PROJ_SCREEN_X'] <= object_features[i].bbox[3]) &
                (sub_lidar_df['PROJ_SCREEN_Y'] >= object_features[i].bbox[0]) &
                (sub_lidar_df['PROJ_SCREEN_Y'] <= yl)]
            if len(filtered_lidar_df) > 0:
                nearest_findices, nearest_fdist = compute_match(x0, y0,
                                                                filtered_lidar_df['PROJ_SCREEN_X'],
                                                                filtered_lidar_df['PROJ_SCREEN_Y'])
                nearest_fidx = nearest_findices[0]
                # compare the distance between nearest_fidx to all pole pixels with nearest_dist
                # to determine whether to use nearest_fidx or nearest_idx
                obj_feat_df = pd.DataFrame(data=object_features[i].coords, columns=['Y', 'X'])

                _, nearest_fdist = compute_match(sub_lidar_df.iloc[nearest_fidx].PROJ_SCREEN_X,
                                                 sub_lidar_df.iloc[nearest_fidx].PROJ_SCREEN_Y,
                                                 obj_feat_df['X'], obj_feat_df['Y'])
                print(f'nearest_fidx: {nearest_fidx}, nearest_fdist: {nearest_fdist}')
                if nearest_fdist < nearest_dist:
                    # use closest LIDAR data lying inside pole bounding box instead of closest LIDAR point
                    # to the lowest pole pixel
                    nearest_idx = nearest_fidx
                    print(f'nearest filtered ldf: {sub_lidar_df.iloc[nearest_idx]}')

            print(lidar_file_name, nearest_idx)
            if nearest_idx >= 0:
                ref_bearing = bearing_between_two_latlon_points(cam_lat, cam_lon,
                                                                sub_lidar_df.iloc[nearest_idx].lat,
                                                                sub_lidar_df.iloc[nearest_idx].lon,
                                                                is_degree=True)
                # convert camera line-of-sight obj_depth back to the distance between camera to object
                obj_depth = obj_depth / cos(sub_lidar_df.iloc[nearest_idx].BEARING)
                # use ref_bearing only without accounting for any offset since the nearest LIDAR
                # point should be the point that is hit by the ray cast from camera to object if the
                # LIDAR raster grid has enough resolution
                print(f'nearest_idx: {nearest_idx}, lat: {sub_lidar_df.iloc[nearest_idx].lat}, '
                      f'lon: {sub_lidar_df.iloc[nearest_idx].lon}')
            else:
                # avg_lat, avg_lon = convert_xy_to_lat_lon(avg_lx, avg_ly)
                # ref_bearing = bearing_between_two_latlon_points(cam_lat, cam_lon,
                #                                                 avg_lat,
                #                                                 avg_lon,
                #                                                 is_degree=True)
                # print(f'ref_bearing: {ref_bearing}, avg_lat: {avg_lat}, avg_lon: {avg_lon}, '
                #       f'depth: {obj_depth},'
                #       f'image: {mapped_image}{suffix}, x0: {x0}, y0: {yl}')
                print('nearest_idx is -1, exiting')
                exit(1)

            br_angle = (ref_bearing + 360) % 360
            img_input_list.append([input_image_base_name, cam_lat, cam_lon, int(x0), int(y0),
                                   br_angle, obj_depth])
            # if input_image_base_name == '926005420241':
            #    labeled_data[labeled_data == 1 ] = 255
            #    save_data_to_image(labeled_data, f'{input_image_base_name}_processed.png')
            print(f'{input_image_base_name}, ori: {object_features[i].orientation}, '
                  f'minx: {object_features[i].bbox[1]}, maxx: {object_features[i].bbox[3]}, '
                  f'miny: {object_features[i].bbox[0]}, maxy: {yl}, '
                  f'xdiff: {object_features[i].bbox[3] - object_features[i].bbox[1]}, '
                  f'ydiff: {object_features[i].bbox[2] - object_features[i].bbox[0]}, cam_br:{cam_br}, '
                  f'br_angle: {br_angle}, depth: {obj_depth}')
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
                        default='../depth_anything/output/new_test_scene',
                        help='input path that includes depth prediction output images')
    parser.add_argument('--lidar_project_info_file_pattern', type=str,
                        default='data/new_test_scene/lane_test/lidar_project_info_{}.csv',
                        # default='data/d13_route_40001001011/oneformer/output/all_lidar_vertices/lidar_project_info_{}.csv',
                        help='input LIDAR projection info file pattern')
    parser.add_argument('--output_file', type=str,
                        # default='data/d13_route_40001001011/oneformer/output/all_lidar_vertices/test_mapping_input.csv',
                        default='data/new_test_scene/lane_test/test_mapping_input.csv',
                        help='output file that contains image base names and corresponding segmented object depths')
    parser.add_argument('--front_only', action="store_true",
                        help='whether to compute mapping inputs for front view images only')


    args = parser.parse_args()
    input_seg_map_info_with_path = args.input_seg_map_info_with_path
    route_id = args.route_id
    model_col_header = args.model_col_header
    input_sensor_mapping_file_with_path = args.input_sensor_mapping_file_with_path
    input_depth_image_path = args.input_depth_image_path
    lidar_project_info_file_pattern = args.lidar_project_info_file_pattern
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
    df.apply(lambda row: compute_mapping_input(mapping_df, input_depth_image_path,
                                               row['MAPPED_IMAGE'], row[model_col_header],
                                               lidar_project_info_file_pattern), axis=1)
    out_df = pd.DataFrame(img_input_list, columns=["imageBaseName", "lat", "lon", "x", "y", "bearing", "depth"])
    out_df.to_csv(output_file, index=False)
    sys.exit(0)
