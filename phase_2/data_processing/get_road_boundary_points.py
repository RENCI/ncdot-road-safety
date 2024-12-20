import argparse
import os
import sys
import matplotlib.pyplot as plt
import cv2
import numpy as np
import pandas as pd
from PIL import Image
from skimage import morphology, measure
from sklearn.cluster import DBSCAN
from scipy.spatial import cKDTree
from scipy.ndimage import binary_dilation
from itertools import combinations

from data_processing.utils import get_data_from_image, SegmentationClass, ROADSIDE, classify_points_base_on_centerline


def _get_road_intersections_by_y(contours, y):
    # Find intersections of the scanline of y with the road boundary contours
    # y_range is a list of indices of the vertices that intersect the scanline
    y_range = np.where((contours[:, 1] <= y) & (np.roll(contours, 1, axis=0)[:, 1] > y))[0]
    # contours[y_range, 0] are the x-coordinates of those intersecting vertices
    # contours[y_range, 1] are the y-coordinates of those intersecting vertices
    # intersections = x1 + (x2-x1) * (y-y1)/(y2-y1)
    intersects = contours[y_range, 0] + (y - contours[y_range, 1]) * \
                    (np.roll(contours, 1, axis=0)[y_range, 0] - contours[y_range, 0]) / \
                    (np.roll(contours, 1, axis=0)[y_range, 1] - contours[y_range, 1])
    # Sort intersection points
    intersects.sort()
    return intersects


def process_boundary_in_image(in_img, vehicle_mask=None):
    cleaned_mask = morphology.remove_small_objects(in_img, min_size=1000)
    labeled_data, count = measure.label(cleaned_mask, connectivity=2, return_num=True)
    labeled_data = labeled_data.astype('uint8')
    binary_data = np.copy(labeled_data)
    binary_data[binary_data > 0] = 255

    # Apply Gaussian blur to reduce noise
    blurred_image = cv2.GaussianBlur(binary_data, (5, 5), 0)
    # Apply Canny edge detection
    edges = cv2.Canny(blurred_image, 100, 200)
    if vehicle_mask is not None:
        edges[vehicle_mask] = 0
    # Find all connected components in the edge image
    num_labels, labels, stats, centroids = cv2.connectedComponentsWithStats(edges, connectivity=8)
    # The first label is the background, skip it
    for i in range(1, num_labels):
        area = stats[i, cv2.CC_STAT_AREA]
        if area < 360:
            # Set the pixel values of this small component to 0 to remove it
            labels[labels == i] = 0

    # Convert the filtered labels back to a binary image
    filtered_edges = np.where(labels > 0, 255, 0).astype('uint8')
    y_coords, x_coords = np.where(filtered_edges > 0)
    edge_points = np.column_stack((x_coords, y_coords))
    return filtered_edges, [edge_points]


def _cluster_points(points, eps=80, min_samples=1):
    """Clusters points in a row using DBSCAN to identify lanes."""
    if len(points) < min_samples:
        return [points]
    clustering = DBSCAN(eps=eps, min_samples=min_samples).fit(points)
    clusters = []
    for cluster_id in np.unique(clustering.labels_):
        if cluster_id == -1:
            # Noise points, ignore
            continue
        clusters.append(points[clustering.labels_ == cluster_id])
    return clusters


def _cluster_row(contours, row_no):
    row_data = contours[contours[:, 1] == row_no]
    # sort x-coordinates of the first row
    sorted_row = row_data[row_data[:, 1].argsort()]
    return _cluster_points(sorted_row)


def _filter_out_small_noisy_clusters(input_img):
    # filter out small noisy clusters
    num_labels, labels, stats, _ = cv2.connectedComponentsWithStats(input_img, connectivity=8)
    for i in range(num_labels):
        if stats[i, cv2.CC_STAT_AREA] < 30 or (stats[i, cv2.CC_STAT_AREA] == stats[i, cv2.CC_STAT_WIDTH]
                                               and stats[i, cv2.CC_STAT_AREA] < 210):
            input_img[labels == i] = 0
    # extract lane contour points
    obj_indices = np.where(input_img == 255)
    # obj_indices[1] contains x coordinate of lane pixel while obj_indices[0] contains y coordinate
    # of lane pixel lane_contour contains array of lane pixel [x y]
    contour = np.column_stack((obj_indices[1], obj_indices[0]))
    return input_img, contour


def _get_cluster_info(contour, contour_idx):
    clustered_row = _cluster_row(contour, contour_idx)
    row_center = None
    row_filter_dist = -1
    if len(clustered_row) >= 3:
        # Check if the clusters satisfy the central positioning condition
        best_score = float('inf')
        for left_cluster, middle_cluster, right_cluster in combinations(clustered_row, 3):
            left_centroid_x = np.mean(left_cluster[:, 0])
            right_centroid_x = np.mean(right_cluster[:, 0])
            middle_centroid = np.mean(middle_cluster, axis=0)
            dist_to_left = middle_centroid[0] - left_centroid_x
            dist_to_right = right_centroid_x - middle_centroid[0]
            score = abs(dist_to_left - dist_to_right)
            if score < 300 and score < best_score:
                # the middle cluster is approximately centered between left and right clusters.
                best_score = score
                row_center = middle_centroid
                row_filter_dist = (np.max(right_cluster[:, 0]) - np.min(left_cluster[:, 0])) / 4
    return row_center, row_filter_dist


def get_axis_from_points(start_point, end_point):
    # return axis pointing from start_point to end_point
    axis = end_point - start_point
    return axis / np.linalg.norm(axis)  # Normalize the axis


def get_image_lane_points(image_file_name, save_processed_image=False):
    image_width, image_height, lane_img = get_data_from_image(image_file_name)
    # remove unwanted pixels
    kernel = np.ones((1, 3), np.uint8)
    eroded = cv2.erode(lane_img, kernel, iterations=1)
    lane_img = cv2.dilate(eroded, kernel, iterations=1)
    mask = morphology.skeletonize(lane_img)

    lane_img[lane_img != 0] = 0
    lane_img[mask == 1] = 255
    lane_img, lane_contour = _filter_out_small_noisy_clusters(lane_img)

    # Sort lane_points based on y-coordinates
    sorted_lane_contour = lane_contour[lane_contour[:, 1].argsort()]
    # Find rows (represented by y) with more than 2 points
    unique_rows, counts = np.unique(sorted_lane_contour[:, 1], return_counts=True)
    rows_with_potential_lanes = unique_rows[counts >= 3]  # Use rows with 2 or more points
    first_row_idx = last_row_idx = -1
    # determine the first and last row containing the middle lane
    filter_threshold = 30
    for i in range(len(rows_with_potential_lanes)):
        if first_row_idx == -1:
            first_row_center, filter_dist = _get_cluster_info(lane_contour, rows_with_potential_lanes[i])
            if first_row_center is not None:
                first_row_idx = i
                if 200 > filter_dist > filter_threshold:
                    filter_threshold = filter_dist
        if last_row_idx == -1:
            last_row_center, _ = _get_cluster_info(lane_contour, rows_with_potential_lanes[-(i+1)])
            if last_row_center is not None:
                last_row_idx = len(rows_with_potential_lanes) - (i + 1)

        if first_row_idx > -1 and last_row_idx > -1:
            break

    if first_row_idx == -1 or last_row_idx == -1:
        print(f'cannot find start and end middle lane points to create a centralline axis for filtering: '
              f'first_row_idx: {first_row_idx}, last_row_idx: {last_row_idx}, {image_file_name}, returning')
        return image_width, image_height, lane_img, [lane_contour], None

    # compute axes and centroids composed of multiple segments from the middle lane
    middle_points = []
    middle_axes = []
    # Loop through the selected rows to create multiple line segments
    step_size = 30
    last_valid_end = None
    for idx in range(first_row_idx, last_row_idx, step_size):
        idx2 = idx + step_size
        if idx2 >= last_row_idx:
            idx2 = last_row_idx
        if last_valid_end is not None:
            row_center_start = last_valid_end
        else:
            row_center_start, _ = _get_cluster_info(lane_contour, rows_with_potential_lanes[idx])
        row_center_end, _ = _get_cluster_info(lane_contour, rows_with_potential_lanes[idx2])
        if (row_center_start is not None and row_center_end is not None
                and abs(row_center_start[0] - row_center_end[0]) <= 300):
            # Calculate axis for this segment
            axis = get_axis_from_points(row_center_end, row_center_start)
            # Append axis and centroid point to lists
            middle_axes.append(axis)
            middle_points.append(row_center_start)
            last_valid_end = row_center_end
    if last_valid_end is not None and not np.any(np.all(middle_points == last_valid_end, axis=1)):
        start_point = middle_points[-1]
        axis = get_axis_from_points(last_valid_end, start_point)
        middle_axes.append(axis)
        middle_points.append(last_valid_end)
    if len(middle_axes) <= 0:
        return image_width, image_height, lane_img, [lane_contour], None

    # Convert lists to NumPy arrays
    middle_axes = np.array(middle_axes)
    middle_points = np.array(middle_points[:-1])

    if save_processed_image:
        # Draw the central axis line for visual debugging
        binary_data = np.uint8(lane_img)
        color_image = cv2.cvtColor(binary_data, cv2.COLOR_GRAY2BGR)
        for idx in range(len(middle_points) - 1):
            point1 = (int(middle_points[idx][0]), int(middle_points[idx][1]))
            point2 = (int(middle_points[idx + 1][0]), int(middle_points[idx + 1][1]))
            cv2.line(color_image, point1, point2, (0, 0, 255), 2)  # Blue line for visibility
        # cv2.line(color_image, (0, rows_with_potential_lanes[first_row_idx]),
        #           (2000, rows_with_potential_lanes[first_row_idx]), (0, 0, 255), 2)
        # cv2.line(color_image, (0, rows_with_potential_lanes[last_row_idx]),
        #           (2000, rows_with_potential_lanes[last_row_idx]), (0, 0, 255), 2)
        Image.fromarray(color_image, 'RGB').save(f'{os.path.splitext(image_file_name)[0]}_axis.png')

    # compute the perpendicular distance of each point to the central axes
    # Build a cKDTree for fast nearest neighbor search
    middle_line_kdtree = cKDTree(middle_points)
    dists, indices = middle_line_kdtree.query(lane_contour)
    # Get the corresponding closest middle_points and axis directions
    closest_middle_points = middle_points[indices]  # Shape: (M, 2)
    closest_axes = middle_axes[indices]  # Shape: (M, 2)
    vector_to_middle = lane_contour - closest_middle_points
    # Project the vector to the axis via dot product
    dot_products = np.sum(vector_to_middle * closest_axes, axis=1)  # Shape: (M,)
    projections = dot_products[:, np.newaxis] * closest_axes  # Shape: (M, 2)

    # Compute the perpendicular vectors (difference between vectors and their projections)
    perpendicular_vectors = vector_to_middle - projections  # Shape: (M, 2)
    # The perpendicular distances are the magnitudes of the perpendicular vectors
    perpendicular_dists = np.linalg.norm(perpendicular_vectors, axis=1)  # Shape: (M,)

    # Filter out points based on the threshold distance
    filtered_lane_contour = lane_contour[perpendicular_dists > filter_threshold]
    lane_img[lane_img != 0] = 0
    lane_img[filtered_lane_contour[:, 1], filtered_lane_contour[:, 0]] = 255
    lane_img, filtered_lane_contour = _filter_out_small_noisy_clusters(lane_img)

    if save_processed_image:
        binary_data = np.uint8(lane_img)
        Image.fromarray(binary_data, 'L').save(f'{os.path.splitext(image_file_name)[0]}_processed_filtered.png')

    return image_width, image_height, lane_img, [filtered_lane_contour], middle_points


def get_image_road_points(image_file_name, boundary_only=True):
    image_width, image_height, seg_img = get_data_from_image(image_file_name)
    # Create a mask for ROAD and vehicle classes
    road_mask = seg_img == SegmentationClass.ROAD.value

    # Filter out ROAD boundary pixels that overlap with vehicle pixels
    # Expand the vehicle mask to touch potentially shared road boundary pixels
    vehicle_mask = ((seg_img == SegmentationClass.CAR.value) |
                    (seg_img == SegmentationClass.TRUCK.value) |
                    (seg_img == SegmentationClass.BUS.value) |
                    (seg_img == SegmentationClass.BICYCLE.value) |
                    (seg_img == SegmentationClass.MOTORCYCLE.value) |
                    (seg_img == SegmentationClass.TRAIN.value))
    structuring_element = np.array([[0, 1, 0],
                                    [1, 1, 1],
                                    [0, 1, 0]])
    adjusted_vehicle_mask = binary_dilation(vehicle_mask, structure=structuring_element)

    # Assign values: 255 for filtered ROAD pixels, 0 otherwise
    seg_img[:] = 0
    seg_img[road_mask] = 255
    process_img, process_contour = process_boundary_in_image(seg_img, vehicle_mask = adjusted_vehicle_mask)

    if boundary_only:
        return image_width, image_height, process_img, process_contour
    else:
        boundary_contours = process_contour[0]
        # Determine the minimum and maximum y coordinates of the polygon
        y_min = int(np.min(boundary_contours[:, 1]))
        y_max = int(np.max(boundary_contours[:, 1]))

        # Create an empty list to store the points within the boundary contour
        filled_points = []
        prev_line_x_intersect_first = prev_line_x_intersect_last = None
        for y in range(y_min, y_max + 1):
            # Find intersections of the scanline of y with road boundary
            intersections = _get_road_intersections_by_y(boundary_contours, y)

            if y > 1900 and len(intersections) >= 1:
                if intersections[0] > 2000 and prev_line_x_intersect_first is not None:
                    intersections = np.insert(intersections, 0, prev_line_x_intersect_first)
                elif intersections[-1] < 100 and prev_line_x_intersect_last is not None:
                    intersections = np.append(intersections, prev_line_x_intersect_last)

            # Fill points between pairs of intersections
            for i in range(0, len(intersections) - 1, 2):
                x_start = int(intersections[i])
                x_end = int(intersections[i + 1]) + 1
                # Fill all points between pairs of intersections
                # filled_points.extend([[x, y] for x in range(x_start, x_end)])
                step = (x_end - x_start) // 2
                filled_points.extend([[x_start, y, 1],
                                      # only set Z to be 0 to indicate the middle point for the first intersection pair
                                      [x_start + step, y, 0 if i == 0 else 1],
                                      [x_end, y, 1]])
                # filled_points.extend([[x, y] for x in range(x_start, x_end, step)])
            if len(intersections) > 0:
                prev_line_x_intersect_first = intersections[0]
                prev_line_x_intersect_last = intersections[-1]

        return image_width, image_height, process_img, [np.array(filled_points)]


def combine_lane_and_road_boundary(lane_points, lane_img, road_img, image_file_name, save_processed_image=False,
                                   image_height=1200):
    # get mask created from two lanes for masking out road boundaries
    clust_points = _cluster_points(lane_points, eps=30, min_samples=5)

    if len(clust_points) > 2:
        clust_points = _cluster_points(lane_points, eps=60, min_samples=5)

    # only use the top two clusters which should represent the left and right lanes
    if len(clust_points) >= 3:
        clust_points.sort(key=len, reverse=True)
        clust_points = clust_points[:2]

    if len(clust_points) >= 2:
        # extend the top point of both lanes vertically to the image top so that everything
        # between two lanes will be masked out
        # clust_points[0] = np.vstack((np.array([clust_points[0][0][0], 0]), clust_points[0]))
        # clust_points[1] = np.vstack((np.array([clust_points[1][0][0], 0]), clust_points[1]))
        # move left lane certain pixels to the left and right lane to the right to mask out
        # corresponding road boundary lanes since lane lines will be used in the combined image
        if clust_points[0][0][0] < clust_points[1][0][0]:
            # clust_points[0] is left lane and clust_points[1] is right lane
            clust_points[0][:, 0] -= (clust_points[0][:, 1] * 100 / image_height).astype(int)
            clust_points[1][:, 0] += (clust_points[1][:, 1] * 100 / image_height).astype(int)
        else:
            # clust_points[0] is right lane and clust_points[1] is left lane
            clust_points[0][:, 0] += (clust_points[0][:, 1] * 100 / image_height).astype(int)
            clust_points[1][:, 0] -= (clust_points[1][:, 1] * 100 / image_height).astype(int)
        # clustered points are sorted from top to bottom, i.e., by y in increasing order, so need to
        # flip the sorting order for the second cluster so that bottom of the first cluster can connect
        # to bottom of the second cluster when vstack them
        clust_points[1] = np.flip(clust_points[1], 0)
    clust_points = np.vstack(clust_points)
    # plt.plot(clust_points[:, 0], img_hgt - clust_points[:, 1], 'b--', lw=2)
    # plt.show()
    # create mask from sorted clustered points
    lane_mask = np.zeros_like(lane_img)

    cv2.fillPoly(lane_mask, [clust_points], 255)
    filtered_road_boundaries = cv2.bitwise_and(road_img, road_img, mask=cv2.bitwise_not(lane_mask))

    road_indices = np.where(filtered_road_boundaries == 255)
    road_contour = np.column_stack((road_indices[1], road_indices[0]))

    # filter out smaller road boundary clusters
    clust_road_points = _cluster_points(road_contour, eps=30, min_samples=5)
    road_boundaries = [clust for clust in clust_road_points if len(clust) > 10]
    if len(road_boundaries) > 0:
        road_boundaries_points = np.vstack(road_boundaries)
        road_boundary_img = np.zeros_like(road_img)
        road_boundary_img[road_boundaries_points[:, 1], road_boundaries_points[:, 0]] = 255
        combined_img = cv2.bitwise_or(lane_img, road_boundary_img)
        if save_processed_image:
            cv2.imwrite(f'{os.path.splitext(image_file_name)[0]}_processed_combined.png', combined_img)
        road_indices = np.where(combined_img == 255)
        return np.column_stack((road_indices[1], road_indices[0]))
    else:
        # return lane contours since there are no important road boundary components to merge in
        return lane_points



if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Process arguments.')
    parser.add_argument('--input_data_path', type=str,
                        default='data/d13_route_40001001012/seg_test',
                        help='input data path')

    args = parser.parse_args()
    input_data_path = args.input_data_path
    input_lane_points = input_road_points = None
    images = [image[:-4] for image in os.listdir(input_data_path) if image.endswith('1.png')]
    print(f'images: {images}')
    for img in images:
        lane_image_with_path = os.path.join(input_data_path, f'{img}_lanes.png')
        _, img_hgt, input_lane_img, input_list, m_points = get_image_lane_points(lane_image_with_path, save_processed_image=True)
        input_lane_points = input_list[0]
        road_image_with_path = os.path.join(input_data_path, f'{img}.png')
        _, _, input_road_img, input_list = get_image_road_points(road_image_with_path)
        input_road_points = input_list[0]

        if len(input_lane_points) > 0 and len(input_road_points) > 0:
            filtered_contour = combine_lane_and_road_boundary(input_lane_points, input_lane_img, input_road_img,
                                                              road_image_with_path, save_processed_image=True)
        elif len(input_road_points) > 0:
            filtered_contour = input_road_points
        else: # len(input_lane_points) > 0
            filtered_contour = input_lane_points

        # classify each point as left or right side
        if m_points is not None:
            # insert the top point in filtered_contour to m_points to account of the far end
            # curved segment that is not part of the segmented lane but part of the road segmentation boundary
            min_y_index = np.argmin(filtered_contour[:, 1])
            if m_points[0, 1] - filtered_contour[min_y_index, 1] > 10:
                m_points = np.vstack((filtered_contour[min_y_index, :], m_points))

            m_points_df = pd.DataFrame({'x': m_points[:, 0], 'y': m_points[:, 1]})
            classified_sides = classify_points_base_on_centerline(
                filtered_contour, m_points_df)
            left_mask = classified_sides == ROADSIDE.LEFT.value  # Mask for left side points
            right_mask = classified_sides == ROADSIDE.RIGHT.value  # Mask for right side points

            input_lane_img[input_lane_img != 0] = 0
            input_lane_img[filtered_contour[left_mask][:, 1], filtered_contour[left_mask][:, 0]] = 100
            input_lane_img[filtered_contour[right_mask][:, 1], filtered_contour[right_mask][:, 0]] = 255
            binary_data = np.uint8(input_lane_img)
            Image.fromarray(binary_data, 'L').save(f'{os.path.splitext(lane_image_with_path)[0]}_with_sides.png')

    sys.exit()
