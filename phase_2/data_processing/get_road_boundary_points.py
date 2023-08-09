import cv2
import os
import numpy as np
from skimage import morphology, measure
import argparse
from utils import get_data_from_image
import pickle


def get_image_road_points(image_file_name, boundary_only=True):
    image_width, image_height, seg_img = get_data_from_image(image_file_name)
    # seg_img is labeled segmented image data with road labeled as 1 and object labeled as 2
    seg_img[seg_img == 2] = 0
    seg_img[seg_img == 1] = 255
    cleaned_mask = morphology.remove_small_objects(seg_img, min_size=1000)
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
            return_contours = [np.concatenate(updated_contours[-2:], axis=0)]
        else:
            return_contours = [updated_contours[-1]]
    else:
        return_contours = updated_contours

    if boundary_only:
        return image_width, image_height, return_contours
    else:
        boundary_contours = return_contours[0]
        # Determine the minimum and maximum y coordinates of the polygon
        y_min = int(np.min(boundary_contours[:, 1]))
        y_max = int(np.max(boundary_contours[:, 1]))

        # Create an empty list to store the points within the boundary contour
        filled_points = []
        prev_line_x_intersect_first = prev_line_x_intersect_last = None
        for y in range(y_min, y_max + 1):
            # Find intersections of the scanline with each edge, y_range is a list of indices of the vertices that
            # intersect the scanline
            y_range = np.where((boundary_contours[:, 1] <= y) & (np.roll(boundary_contours, 1, axis=0)[:, 1] > y))[0]
            # boundary_contours[y_range, 0] are the x-coordinates of those intersecting vertices
            # boundary_contours[y_range, 1] are the y-coordinates of those intersecting vertices
            # intersections = x1 + (x2-x1) * (y-y1)/(y2-y1)
            intersections = boundary_contours[y_range, 0] + (y - boundary_contours[y_range, 1]) * \
                (np.roll(boundary_contours, 1, axis=0)[y_range, 0] - boundary_contours[y_range, 0]) / \
                (np.roll(boundary_contours, 1, axis=0)[y_range, 1] - boundary_contours[y_range, 1])
            # Sort intersection points
            intersections.sort()

            if y > 1900 and len(intersections) >= 1:
                if intersections[0] > 2000 and prev_line_x_intersect_first is not None:
                    intersections = np.insert(intersections, 0, prev_line_x_intersect_first)
                elif intersections[-1] < 100 and prev_line_x_intersect_last is not None:
                    intersections = np.append(intersections, prev_line_x_intersect_last)

            # Fill points between pairs of intersections
            for i in range(0, len(intersections) - 1, 2):
                x_start = int(intersections[i])
                x_end = int(intersections[i + 1]) + 1
                filled_points.extend([[x, y] for x in range(x_start, x_end)])
            if len(intersections) > 0:
                prev_line_x_intersect_first = intersections[0]
                prev_line_x_intersect_last = intersections[-1]
        return image_width, image_height, [filled_points]


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Process arguments.')
    parser.add_argument('--input_data_path', type=str, default='data/d13_route_40001001011/oneformer/input',
                        help='input data path')
    parser.add_argument('--output_file', type=str, default='data/d13_route_40001001011/oneformer/output/input_2d.pkl',
                        help='output pickle 2D point file name with path')

    args = parser.parse_args()
    input_data_path = args.input_data_path
    output_file = args.output_file

    all_road_contours = []
    for image in os.listdir(input_data_path):
        if not image.endswith('1.png'):
            continue
        _, _, road_contours = get_image_road_points(os.path.join(input_data_path, image))
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
