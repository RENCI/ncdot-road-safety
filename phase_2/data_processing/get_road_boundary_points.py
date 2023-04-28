import cv2
import os
import numpy as np
import skimage.measure
import argparse
from utils import get_data_from_image
import pickle


def get_image_road_boundary_points(image_file_name):
    image_width, image_height, seg_img = get_data_from_image(image_file_name)
    # seg_img is labeled segmented image data with road labeled as 1 and object labeled as 2
    seg_img[seg_img == 2] = 0
    labeled_data, count = skimage.measure.label(seg_img, connectivity=2, return_num=True)
    labeled_data = labeled_data.astype('uint8')

    # segmented road could have many disconnected road segments, only use the largest one
    max_len = 0
    max_lbl = 0
    for i in range(1, len(np.unique(labeled_data))):
        seg_len = len(labeled_data[labeled_data == i])
        if seg_len > max_len:
            max_len = seg_len
            max_lbl = i

    binary_data = np.copy(labeled_data)
    # label road boundary pixels as 255 and other pixels as 0
    binary_data[binary_data == max_lbl] = 255
    binary_data[binary_data != 255] = 0

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
            contour_shape = contours[i].shape
            updated_contours.append(np.reshape(contours[i], (contour_shape[0], contour_shape[2])))
    return image_width, image_height, updated_contours


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
        _, _, road_contours = get_image_road_boundary_points(os.path.join(input_data_path, image))
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
