import sys
import cv2
import os
import numpy as np
from skimage import morphology, measure
from PIL import Image
import argparse
from utils import get_data_from_image, SegmentationClass
import pickle


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
    print(f'length of contours found: {len(contours)}, length of filtered/processed contours: {len(updated_contours)}')
    if len(updated_contours) > 1:
        if updated_contours[-2].shape[0] > 800:
            return binary_data, [np.concatenate(updated_contours[-2:], axis=0)]
        else:
            return binary_data, [updated_contours[-1]]
    else:
        return binary_data, updated_contours


def get_image_road_points(image_file_name, boundary_only=True):
    image_width, image_height, seg_img = get_data_from_image(image_file_name)
    # assign road with 255 and the rest with 0
    seg_img[seg_img == SegmentationClass.ROAD.value] = 255
    seg_img[seg_img != 255] = 0

    process_img, process_contour = process_boundary_in_image(seg_img)

    if boundary_only:
        # find convexHull of the road contours
        hull = cv2.convexHull(process_contour[0], returnPoints=False)
        # find convexity defects to identify concave regions (potential intersections)
        defects = cv2.convexityDefects(process_contour[0], hull)

        process_img[process_img != 0] = 0
        binary_data = np.uint8(process_img)
        if defects is not None:
            left_intersect_list = []
            right_intersect_list = []
            for defect in defects:
                sp, ep, fp, fdist = defect[0]

                start = tuple(process_contour[0][sp])
                end = tuple(process_contour[0][ep])
                far = tuple(process_contour[0][fp])
                if 40000 > fdist > 2000:
                    # print(f'fdist: {fdist}, x: {far[0]}, y: {far[1]}')
                    cv2.line(binary_data, start, far, (255, 255, 255), 2)
                    cv2.line(binary_data, far, end, (255, 255, 255), 2)
                    cv2.circle(binary_data, far, 5, (255, 255, 255), -1)
                    # Find intersections of the scanline of y with road boundary
                    intersections = get_road_intersections_by_y(process_contour[0], far[1])
                    x_start = int(intersections[0])
                    x_end = int(intersections[-1]) + 1
                    center_pt_x = x_start + (x_end - x_start) // 2
                    if far[0] <= center_pt_x:
                        left_intersect_list.append(far)
                    else:
                        right_intersect_list.append(far)
            # sort intersect_list by the second element (y coordinate) of each tuple (x, y) pair in descending order
            # since y origin is on the top of the image in the image coordinate system and we want to sort points
            # in the distance from camera from closest to farthest
            sorted_intersects = [sorted(left_intersect_list, key=lambda point: point[1], reverse=True),
                                 sorted(right_intersect_list, key=lambda point: point[1], reverse=True)]
        else:
            sorted_intersects = []
        cv2.drawContours(binary_data, process_contour, -1, (127, 127, 127), 1)
        Image.fromarray(binary_data, 'L').save(f'{os.path.splitext(image_file_name)[0]}_intersections.png')
        print(sorted_intersects)
        return image_width, image_height, process_contour, sorted_intersects
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
        return image_width, image_height, [np.array(filled_points)], []


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Process arguments.')
    parser.add_argument('--input_data_path', type=str,
                        # default='data/d13_route_40001001011/oneformer/input',
                        default='data/new_test_scene/seg_test',
                        help='input data path')
    parser.add_argument('--output_file', type=str,
                        # default='data/d13_route_40001001011/oneformer/output/input_2d.pkl',
                        default='data/new_test_scene/output/input_2d.pkl',
                        help='output pickle 2D point file name with path')

    args = parser.parse_args()
    input_data_path = args.input_data_path
    output_file = args.output_file

    all_road_contours = []
    for image in os.listdir(input_data_path):
        if not image.endswith('1.png'):
            continue
        _, _, road_contours, _ = get_image_road_points(os.path.join(input_data_path, image))
        print(f"Number of updated contours found = {len(road_contours)} for {image}")
        print(f"the first contour shape: {road_contours[0].shape} for {image}")
        # binary_data[binary_data != 0] = 0
        # binary_data = np.uint8(binary_data)
        # cv2.drawContours(binary_data, updated_contours, -1, (255, 255, 255), 3)
        # Image.fromarray(binary_data, 'L').save('926005420241_road_boundary.png')
        all_road_contours.extend(road_contours)
    # output to pickle file for blindPnP correspondence prediction
    with open(output_file, 'wb') as f:
        pickle.dump(all_road_contours, f)
    sys.exit()
