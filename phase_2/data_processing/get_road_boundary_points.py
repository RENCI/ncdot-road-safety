import cv2
import os
import numpy as np
import skimage.measure
import argparse
from utils import get_data_from_image
import pickle

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Process arguments.')
    parser.add_argument('--input_data_path', type=str, default='data/d13_route_40001001011/oneformer/input',
                        help='input data path')
    parser.add_argument('--output_file', type=str, default='data/d13_route_40001001011/oneformer/output/input_2d.pkl',
                        help='output pickle 2D point file name with path')

    args = parser.parse_args()
    input_data_path = args.input_data_path
    output_file = args.output_file

    updated_contours = []
    for image in os.listdir(input_data_path):
        if not image.endswith('1.png'):
            continue
        image_width, image_height, input_data = get_data_from_image(os.path.join(input_data_path, image))
        input_data[input_data == 2] = 0
        labeled_data, count = skimage.measure.label(input_data, connectivity=2, return_num=True)
        labeled_data = labeled_data.astype('uint8')

        binary_data = np.copy(labeled_data)
        binary_data[binary_data == 1] = 255
        binary_data[binary_data != 255] = 0

        # Apply Canny edge detection
        edges = cv2.Canny(binary_data, 100, 200)

        # Dilate edges to connect any broken lines
        dilated_edges = cv2.dilate(edges, None, iterations=1)

        # Find contours of the dilated edges
        contours, _ = cv2.findContours(dilated_edges, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        print(f"Number of Contours found = {len(contours)} for image {image}")

        for i in range(len(contours)):
            min_xy = np.min(contours[i], axis=0)
            max_xy = np.max(contours[i], axis=0)
            minx = min_xy[0][0]
            miny = min_xy[0][1]
            maxx = max_xy[0][0]
            maxy = max_xy[0][1]
            if maxy - miny > 15:
                cshape = contours[i].shape
                updated_contours.append(np.reshape(contours[i], (cshape[0], cshape[2])))
        print(f"Number of updated contours found = {len(updated_contours)}")
        print(f"the first contour shape: {updated_contours[0].shape}")
        print(updated_contours[0])
        # binary_data[binary_data != 0] = 0
        # binary_data = np.uint8(binary_data)
        # cv2.drawContours(binary_data, updated_contours, -1, (255, 255, 255), 3)
        # Image.fromarray(binary_data, 'L').save('926005420241_road_boundary.png')

    # output to pickle file for blindPnP correspondence prediction
    with open(output_file, 'wb') as f:
        pickle.dump(updated_contours, f)
