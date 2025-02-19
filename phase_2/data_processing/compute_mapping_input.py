import os
import sys
import argparse
import pandas as pd
import numpy as np
import multiprocessing as mp
from skimage.measure import label, regionprops, intersection_coeff
from skimage.morphology import binary_dilation, disk
from PIL import Image
from sklearn.linear_model import LinearRegression
import cv2
import itertools
from math import cos
from utils import SegmentationClass, get_data_from_image, \
    compute_match, bearing_between_two_latlon_points, LIDARClass, get_set_minute_sub_path
from common.utils import MAX_OBJ_DIST_FROM_CAM


POLE_X_SIZE_THRESHOLD = 10
POLE_Y_SIZE_THRESHOLD = 20
POLE_ASPECT_RATIO_THRESHOLD = 10  # 12
POLE_EROSION_DILATION_KERNEL_SIZE = 10


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


def process_image(row, input_depth_path, lidar_file_pattern):
    mapped_image = row['imageBaseName']
    cam_lon = float(row['LONGITUDE'])
    cam_lat = float(row['LATITUDE'])
    image_suffix_list = ('5.png', '1.png', '2.png')
    output_list = []

    # check if lidar project info is available for this image
    if lidar_file_pattern:
        lidar_file_name = lidar_file_pattern.format(f'{mapped_image}')
        if not os.path.exists(lidar_file_name):
            lidar_file_name = ''
    else:
        lidar_file_name = ''

    if lidar_file_name:
        lidar_df = pd.read_csv(lidar_file_name, usecols=['X', 'Y', 'PROJ_SCREEN_X', 'PROJ_SCREEN_Y', 'WORLD_Z',
                                                         'geometry_y', 'Z', 'C', 'BEARING', 'INITIAL_WORLD_X'])
        lidar_df[['lon', 'lat']] = lidar_df['geometry_y'].apply(lambda x: pd.Series(extract_lon_lat(x)))
    else:
        # no projected lidar file exist for this image, nothing to do
        return

    structuring_element = disk(1)
    for suffix in image_suffix_list:
        # get camera location for the mapped image
        input_image_name = os.path.join(row['SEG_PATH'], f'{mapped_image}{suffix}')
        try:
            image_width, image_height, input_data = get_data_from_image(input_image_name)
        except FileNotFoundError as e:
            print(e)
            continue

        # Depth-Height threshold, e.g., if D < 10, filter out those with H < 500; elif D<25,
        # filter out those with H < 350
        d_h_threshold = {
            MAX_OBJ_DIST_FROM_CAM / 2: image_height / 2,
            MAX_OBJ_DIST_FROM_CAM: image_height / 4  # 350
        }

        # check if the segmentation image includes traffic sign label
        unique_labels = np.unique(input_data)
        if SegmentationClass.POLE.value not in unique_labels:
            continue

        if SegmentationClass.SIGN.value in unique_labels:
            sign_seg_data = (input_data == SegmentationClass.SIGN.value).astype(int)
            dilated_sign_seg_data = binary_dilation(sign_seg_data, structuring_element)
        else:
            dilated_sign_seg_data = None

        pole_seg_data = (input_data == SegmentationClass.POLE.value).astype(int)
        # perform connected component analysis
        labeled_data, count = label(pole_seg_data, connectivity=2, return_num=True)
        labeled_data = labeled_data.astype('uint8')
        if count <= 0:
            continue

        object_features = regionprops(labeled_data)
        input_image_base_name = os.path.basename(os.path.splitext(input_image_name)[0])
        set_str, minute_str = get_set_minute_sub_path(input_image_base_name)
        if minute_str is None:
            # not a valid image
            continue

        depth_image_path = os.path.join(input_depth_path, set_str, minute_str,
                                        f'{input_image_base_name}_depth.png')
        with Image.open(depth_image_path) as depth_img:
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
        if len(sub_lidar_df.index) == 0:
            # the filtered dataframe is empty, nothing to match for
            continue
        sub_lidar_df['PROJ_SCREEN_X'] = sub_lidar_df['PROJ_SCREEN_X'] - xb_min

        front_lidar_fit_df = lidar_df[((lidar_df.C == LIDARClass.ROAD.value) | (lidar_df.C == LIDARClass.BRIDGE.value))
                                      & (lidar_df.CAM_DIST_M < MAX_OBJ_DIST_FROM_CAM)
                                      & (lidar_df.PROJ_SCREEN_X >= 0) & (lidar_df.PROJ_SCREEN_X < image_width)
                                      & (lidar_df.PROJ_SCREEN_Y >= 0) & (lidar_df.PROJ_SCREEN_Y < image_height)].copy()

        if suffix != '1.png':
            front_depth_image_path = os.path.join(input_depth_path, set_str, minute_str,
                                                  f'{input_image_base_name[:-1]}1_depth.png')
            with Image.open(front_depth_image_path) as fnt_dep_img:
                front_depth_data = np.asarray(fnt_dep_img, dtype=np.uint8)
                front_depth_data = front_depth_data[:, :, 0]
                front_depth_data = 255 - front_depth_data
        else:
            front_depth_data = depth_data

        # divide the depth values by 255 to normalize into (0, 1) range
        front_lidar_fit_df['DEPTH'] = front_lidar_fit_df.apply(lambda front_row:
                                                               front_depth_data[front_row['PROJ_SCREEN_Y'],
                                                               front_row['PROJ_SCREEN_X']] / 255, axis=1)
        near = min(front_lidar_fit_df['CAM_DIST_M'])
        far = max(front_lidar_fit_df['CAM_DIST_M'])
        c1_in = 2 * far * near / (near - far)
        c2_in = (far + near) / (far - near)
        # print(f'c1: {c1_in}, c2: {c2_in}, near: {near}, far: {far}')

        front_lidar_fit_df['MAPPED_DIST'] = front_lidar_fit_df.apply(lambda front_row: map_z(c1_in, c2_in,
                                                                                             front_row['CAM_DIST_M']),
                                                                     axis=1)

        x_in = front_lidar_fit_df['DEPTH'].values.reshape(-1, 1)  # Reshape X to a 2D array
        y_in = front_lidar_fit_df['MAPPED_DIST'].values
        model = LinearRegression(fit_intercept=False)
        model.fit(x_in, y_in)
        slope = model.coef_[0]
        # print(f"image: {input_image_base_name}, min_mapped_dist: {min(front_lidar_fit_df['MAPPED_DIST'])}, "
        #      f"max_mapped_dist: {max(front_lidar_fit_df['MAPPED_DIST'])}, fit slope: {slope}")

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
            yl = object_features[i].bbox[2] - 1
            obj_depth = reverse_map_z(c1_in, c2_in, depth_data[yl, x0] * slope / 255)
            # print(f'x0: {x0}, y0: {y0}, xdiff: {xdiff}, ydiff: {ydiff}, depth: {obj_depth}', flush=True)
            if ydiff / xdiff < POLE_ASPECT_RATIO_THRESHOLD:
                major_axis_len = object_features[i].major_axis_length
                minor_axis_len = object_features[i].minor_axis_length
                # print(f'major: {major_axis_len}, minor: {minor_axis_len}', flush=True)
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
                updated_object_features = regionprops(obj_only)
                y0, x0 = updated_object_features[0].centroid
                y0 = int(y0)
                x0 = int(x0)
                obj_depth = reverse_map_z(c1_in, c2_in, depth_data[yl, x0] * slope / 255)
                object_features[i] = updated_object_features[0]

            # apply depth-height filtering
            filtered_out = False
            for key, val in d_h_threshold.items():
                if obj_depth < key:
                    if ydiff < val:
                        filtered_out = True
                    break
            if filtered_out:
                # print(f'filtered out: {x0}, {y0}, {xdiff}, {ydiff}, {obj_depth}')
                continue

            # check if the pole intersects with any sign, if so, filter the pole out
            if dilated_sign_seg_data is not None:
                dilated_pole_seg_data = (labeled_data == i + 1).astype(int)
                if intersection_coeff(dilated_sign_seg_data, dilated_pole_seg_data) \
                        and ydiff < image_height / 3:
                    # only filter out FP sign when ydiff is small enough since there are cases with TP poles
                    # with posted sign on it
                    # print(f'filtered out: pole bbox {object_features[i].bbox} intersects with a sign')
                    continue

            sub_lidar_df['DEPTH'] = sub_lidar_df.apply(
                lambda sub_row: reverse_map_z(
                    c1_in, c2_in, depth_data[sub_row['PROJ_SCREEN_Y'], sub_row['PROJ_SCREEN_X']] * slope / 255),
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
                # print(f'object x, y: {x0}, {yl}, len(nearest_indices): {len(nearest_indices)}, '
                #       f'nearest_idx: {nearest_idx}, nearest_dist: {nearest_dist}, '
                #       f'ldf: {sub_lidar_df.iloc[nearest_idx]}')

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
                # print(f'nearest_fidx: {nearest_fidx}, nearest_fdist: {nearest_fdist}')
                if nearest_fdist < nearest_dist:
                    # use closest LIDAR data lying inside pole bounding box instead of closest LIDAR point
                    # to the lowest pole pixel
                    nearest_idx = nearest_fidx
                    # print(f'nearest filtered ldf: {sub_lidar_df.iloc[nearest_idx]}')

            # print(lidar_file_name, nearest_idx)
            if nearest_idx >= 0:
                ref_bearing = bearing_between_two_latlon_points(cam_lat, cam_lon,
                                                                sub_lidar_df.iloc[nearest_idx].lat,
                                                                sub_lidar_df.iloc[nearest_idx].lon,
                                                                is_degree=True)
                # convert camera line-of-sight obj_depth back to the distance between camera to object
                obj_depth = obj_depth / cos(sub_lidar_df.iloc[nearest_idx].BEARING)
                if obj_depth > MAX_OBJ_DIST_FROM_CAM:
                    # filter out the object if it is too far away from camera
                    continue
                # use ref_bearing only without accounting for any offset since the nearest LIDAR
                # point should be the point that is hit by the ray cast from camera to object if the
                # LIDAR raster grid has enough resolution
                # print(f'nearest_idx: {nearest_idx}, lat: {sub_lidar_df.iloc[nearest_idx].lat}, '
                #       f'lon: {sub_lidar_df.iloc[nearest_idx].lon}')
            else:
                print('nearest_idx is -1, returning')
                return []

            br_angle = (ref_bearing + 360) % 360
            output_list.append([input_image_base_name, cam_lat, cam_lon, int(x0), int(y0), br_angle, obj_depth])
            # if input_image_base_name == '926005420241':
            #    labeled_data[labeled_data == 1 ] = 255
            #    save_data_to_image(labeled_data, f'{input_image_base_name}_processed.png')

            # print(f'{input_image_base_name}, ori: {object_features[i].orientation}, '
            #       f'minx: {object_features[i].bbox[1]}, maxx: {object_features[i].bbox[3]}, '
            #       f'miny: {object_features[i].bbox[0]}, maxy: {yl}, '
            #       f'xdiff: {object_features[i].bbox[3] - object_features[i].bbox[1]}, '
            #       f'ydiff: {object_features[i].bbox[2] - object_features[i].bbox[0]}, '
            #       f'br_angle: {br_angle}, depth: {obj_depth}')
            obj_cnt += 1

    return output_list


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Process arguments.')
    parser.add_argument('--input_base_image_file', type=str,
                        default='/projects/ncdot/NC_2018_Secondary_2/d13_route_40001001012/'
                                'route_40001001012_input_corrected_updated.csv',
                        help='input csv file that includes input base images for computing mapping input')
    parser.add_argument('--segmentation_path', type=str,
                        default='/projects/ncdot/NC_2018_Secondary_2/segmentations/d13',
                        help='segmentation image route path')
    parser.add_argument('--input_depth_image_path', type=str,
                        default='/projects/ncdot/NC_2018_Secondary_2/depth_prediction/d13',
                        help='input path that includes depth prediction output images')
    parser.add_argument('--lidar_project_info_file_pattern', type=str,
                        default='/projects/ncdot/NC_2018_Secondary_2/d13_route_40001001012/'
                                'route_40001001012_geotagging_output/lidar_project_info_{}.csv',
                        help='input LIDAR projection info file pattern')
    parser.add_argument('--output_file', type=str,
                        default='/projects/ncdot/NC_2018_Secondary_2/d13_route_40001001012/'
                                'route_40001001012_mapping_input.csv',
                        help='output file that contains image base names and corresponding segmented object depths')

    args = parser.parse_args()
    input_base_image_file = args.input_base_image_file
    segmentation_path = args.segmentation_path
    input_depth_image_path = args.input_depth_image_path
    lidar_project_info_file_pattern = args.lidar_project_info_file_pattern
    output_file = args.output_file

    df = pd.read_csv(input_base_image_file, index_col=None,
                     usecols=['ROUTEID', 'imageBaseName', 'LATITUDE', 'LONGITUDE'], dtype=str)
    df['SEG_PATH'] = segmentation_path + '/' + df['imageBaseName'].str[:3]
    # Get all available CPU cores
    # forkserver method prevents child processes from inheriting the entire memory state of the parent
    mp.set_start_method("forkserver", force=True)

    # reduce numpy/OpenBLAS threads to 1 per process to prevent numpy/scipy from spawning extra
    # threads inside each worker
    os.environ["OMP_NUM_THREADS"] = "1"
    os.environ["OPENBLAS_NUM_THREADS"] = "1"
    os.environ["MKL_NUM_THREADS"] = "1"
    os.environ["VECLIB_MAXIMUM_THREADS"] = "1"
    os.environ["NUMEXPR_NUM_THREADS"] = "1"
    cv2.setNumThreads(0)  # disable OpenCV parallel threads since MP is used

    num_workers = mp.cpu_count()
    print(f'num_workers: {num_workers}')
    rows = zip(df.to_dict(orient='records'),
               [input_depth_image_path] * len(df),
               [lidar_project_info_file_pattern] * len(df))
    with mp.Pool(num_workers - 1, maxtasksperchild=10) as pool:
        results = pool.starmap(process_image, rows)

    print(f'results: {results}')
    valid_results = [r if r is not None else [] for r in results]
    img_input_list = list(itertools.chain.from_iterable(valid_results))
    out_df = pd.DataFrame(img_input_list, columns=["imageBaseName", "lat", "lon", "x", "y", "bearing", "depth"])
    out_df.to_csv(output_file, index=False)
    sys.exit(0)
