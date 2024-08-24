import argparse
import os
import sys

import cv2
import numpy as np
from PIL import Image
from skimage import morphology, measure
from sklearn.cluster import DBSCAN
from data_processing.utils import get_data_from_image, SegmentationClass


def get_road_intersections_by_y(contours, y):
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


def process_boundary_in_image(img):
    cleaned_mask = morphology.remove_small_objects(img, min_size=1000)
    labeled_data, count = measure.label(cleaned_mask, connectivity=2, return_num=True)
    labeled_data = labeled_data.astype('uint8')
    binary_data = np.copy(labeled_data)
    binary_data[binary_data > 0] = 255
    # Apply Canny edge detection
    edges = cv2.Canny(binary_data, 100, 200)
    # Dilate edges to connect any broken lines
    dilated_edges = cv2.dilate(edges, None, iterations=1)

    # Find contours of the dilated edges
    contours, _ = cv2.findContours(dilated_edges, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    contours = sorted(contours, key=lambda x: cv2.contourArea(x), reverse=True)
    updated_contours = []
    for i in range(len(contours)):
        min_xy = np.min(contours[i], axis=0)
        max_xy = np.max(contours[i], axis=0)
        miny = min_xy[0][1]
        maxy = max_xy[0][1]
        if maxy - miny > 15:
            cshape = contours[i].shape
            cont_len = len(updated_contours)
            if cont_len < 1:
                updated_contours.append(np.reshape(contours[i], (cshape[0], cshape[2])))
            elif cshape[0] < updated_contours[-1].shape[0]:
                updated_contours.insert(cont_len - 1, np.reshape(contours[i], (cshape[0], cshape[2])))
            else:
                updated_contours.append(np.reshape(contours[i], (cshape[0], cshape[2])))
    if len(updated_contours) > 1:
        if updated_contours[-2].shape[0] > 800:
            return binary_data, [np.concatenate(updated_contours[-2:], axis=0)]
        else:
            return binary_data, [updated_contours[-1]]
    else:
        return binary_data, updated_contours

    # Clustering to group points on the same lane


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


def _is_cluster_centered(left_cluster, middle_cluster, right_cluster):
    """Checks if the middle cluster is approximately centered between left and right clusters."""
    left_centroid_x = np.mean(left_cluster[:, 0])
    right_centroid_x = np.mean(right_cluster[:, 0])
    middle_centroid_x = np.mean(middle_cluster[:, 0])

    return abs((middle_centroid_x - left_centroid_x) - (right_centroid_x - middle_centroid_x)) < 100


def get_image_lane_points(image_file_name):
    image_width, image_height, img = get_data_from_image(image_file_name)
    # remove unwanted pixels
    kernel = np.ones((1, 3), np.uint8)
    eroded = cv2.erode(img, kernel, iterations=1)
    img = cv2.dilate(eroded, kernel, iterations=1)
    mask = morphology.skeletonize(img)

    img[img != 0] = 0
    img[mask == 1] = 255
    # binary_data = np.uint8(img)
    # Image.fromarray(binary_data, 'L').save(f'{os.path.splitext(image_file_name)[0]}_contour.png')

    # extract lane contour points
    lane_indices = np.where(img == 255)
    # lane_indices[1] contains x coordinate of lane pixel while lane_indices[0] contains y coordinate of lane pixel
    # lane_contour contains array of lane pixel [x y]
    lane_contour = np.column_stack((lane_indices[1], lane_indices[0]))
    # Sort lane_points based on y-coordinates
    sorted_lane_contour = lane_contour[lane_contour[:, 1].argsort()]
    # Find rows (represented by y) with more than 2 points
    unique_rows, counts = np.unique(sorted_lane_contour[:, 1], return_counts=True)
    rows_with_potential_lanes = unique_rows[counts >= 3]  # Use rows with 2 or more points
    first_row_idx = last_row_idx = -1

    # determine the first and last row containing the central lane
    for i in range(len(rows_with_potential_lanes)):
        if first_row_idx == -1:
            first_row = lane_contour[lane_contour[:, 1] == rows_with_potential_lanes[i]]
            # sort x-coordinates of the first row
            first_row = first_row[first_row[:, 1].argsort()]
            clustered_first_row = _cluster_points(first_row)
            if len(clustered_first_row) >= 3:
                # Check if the clusters satisfy the central positioning condition
                left_cluster, middle_cluster, right_cluster = clustered_first_row[:3]
                if _is_cluster_centered(left_cluster, middle_cluster, right_cluster):
                    first_row_idx = i
                    first_row_center = np.mean(middle_cluster, axis=0)  # Use the centroid of the middle cluster
        if last_row_idx == -1:
            last_row = lane_contour[lane_contour[:, 1] == rows_with_potential_lanes[-(i+1)]]
            # sort x-coordinates of the last row
            last_row = last_row[last_row[:, 1].argsort()]
            clustered_last_row = _cluster_points(last_row)
            # find the row where the middle point is part of the middle lane
            if len(clustered_last_row) >= 3:
                left_cluster, middle_cluster, right_cluster = clustered_last_row[:3]
                if _is_cluster_centered(left_cluster, middle_cluster, right_cluster):
                    last_row_idx = len(rows_with_potential_lanes) - (i + 1)
                    last_row_center = np.mean(middle_cluster, axis=0)

        if first_row_idx > -1 and last_row_idx > -1:
            break
    if first_row_idx == -1 or last_row_idx == -1:
        print(f'cannot find start and end middle lane points to create a central axis for filtering: '
              f'first_row_idx: {first_row_idx}, last_row_idx: {last_row_idx}, returning')
        return image_width, image_height, [], []

    # calculate the central axis and centroid
    # find the central axis from the last row middle lane pixel (lower) to the first row middle lane pixel (upper)
    axis = first_row_center - last_row_center
    # centroid is the middle point of the axis
    centroid = last_row_center + axis / 2.0
    # normalize the axis
    axis = axis / np.linalg.norm(axis)
    # Draw the central axis line for visual debugging
    # point1 = (int(first_row_center[0]), int(first_row_center[1]))
    # point2 = (int(last_row_center[0]), int(last_row_center[1]))
    # color_image = cv2.cvtColor(binary_data, cv2.COLOR_GRAY2BGR)
    # cv2.line(color_image, point1, point2, (0, 0, 255), 2)  # Blue line for visibility
    # Image.fromarray(color_image, 'RGB').save(f'{os.path.splitext(image_file_name)[0]}_axis.png')
    # compute the perpendicular distance of each point to the central axis
    vector_to_centroid = lane_contour - centroid
    # Project the vector to the axis via dot product
    projection_on_axis = np.dot(vector_to_centroid, axis)
    # Calculate the perpendicular vector (error vector)
    perpendicular_vector = vector_to_centroid - np.outer(projection_on_axis, axis)
    # Calculate the distance of each point to the axis
    distance_to_axis = np.linalg.norm(perpendicular_vector, axis=1)

    # Filter out points based on the threshold distance
    filtered_lane_contour = lane_contour[distance_to_axis > 25]
    img[img != 0] = 0
    img[filtered_lane_contour[:, 1], filtered_lane_contour[:, 0]] = 255
    binary_data = np.uint8(img)
    # cv2.line(binary_data, first_row[1], last_row[1], (255, 255, 255), 2)
    Image.fromarray(binary_data, 'L').save(f'{os.path.splitext(image_file_name)[0]}_processed_filtered.png')

    return image_width, image_height, [filtered_lane_contour]


def get_image_road_points(image_file_name, boundary_only=True):
    image_width, image_height, seg_img = get_data_from_image(image_file_name)
    # assign road with 255 and the rest with 0
    seg_img[seg_img == SegmentationClass.ROAD.value] = 255
    seg_img[seg_img != 255] = 0

    process_img, process_contour = process_boundary_in_image(seg_img)

    if boundary_only:
        return image_width, image_height, process_contour
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
            intersections = get_road_intersections_by_y(boundary_contours, y)

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
        return image_width, image_height, [np.array(filled_points)]


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Process arguments.')
    parser.add_argument('--input_data_path', type=str,
                        default='data/d13_route_40001001012/seg_test',
                        help='input data path')

    args = parser.parse_args()
    input_data_path = args.input_data_path

    for image in os.listdir(input_data_path):
        if not image.endswith('1_lanes.png'):
            continue
        _, _, input_list = get_image_lane_points(os.path.join(input_data_path, image))
        print(f"Number of updated contours found = {len(input_list[0])} for {image}")
        print(f"the first contour shape: {input_list[0].shape} for {image}")

    sys.exit()
