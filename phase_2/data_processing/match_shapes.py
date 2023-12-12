import sys
import argparse
import matplotlib.pyplot as plt
from PIL import Image
import cv2
import numpy as np
import pandas as pd
from utils import load_pickle_data
from get_road_boundary_points import process_boundary_in_image


def process_defects(defects):
    processed_defs = []
    for defect in defects:
        _, _, _, far_dist = defect[0]
        # if 40000 > far_dist > 2000:
        processed_defs.append(defect)
    return processed_defs


def match_shapes(contour1, contour2, threshold_dist=1000, threshold_depth=1000):
    # Calculate convex hull and convexity defects for both contours
    hull1 = cv2.convexHull(contour1, returnPoints=False)
    hull1[::-1].sort(axis=0)
    defects1 = process_defects(cv2.convexityDefects(contour1, hull1))

    hull2 = cv2.convexHull(contour2, returnPoints=False)
    hull2[::-1].sort(axis=0)
    defects2 = process_defects(cv2.convexityDefects(contour2, hull2))
    print(f'len(defects1): {len(defects1)}, len(defects2): {len(defects2)}')
    image1 = np.zeros((image_height, image_width), dtype=np.uint8)
    cv2.drawContours(image1, [contour1], -1, (127, 127, 127), 1)
    cv2.drawContours(image1, [cv2.convexHull(contour1)], -1, (100, 100, 100), 1)
    for defect in defects1:
        _, _, fp, fdist = defect[0]
        print(f'defects1: {fdist}')
        far = tuple(contour1[fp])
        cv2.circle(image1, far, 5, (255, 255, 255), -1)
    Image.fromarray(image1, 'L').save('image1.png')
    image2 = np.zeros((image_height, image_width), dtype=np.uint8)
    cv2.drawContours(image2, [contour2], -1, (127, 127, 127), 1)
    cv2.drawContours(image2, [cv2.convexHull(contour2)], -1, (100, 100, 100), 1)
    for defect in defects2:
        _, _, fp, fdist = defect[0]
        print(f'defects2: {fdist}')
        far = tuple(contour2[fp])
        cv2.circle(image2, far, 5, (255, 255, 255), -1)
    Image.fromarray(image2, 'L').save('image2.png')
    # Check if the number of convexity defects is the same
    if len(defects1) != len(defects2):
        return False
    # Compare convexity defects
    for i in range(len(defects1)):
        print(defects1[i])
        print(defects2[i])
        d1 = defects1[i][0]
        d2 = defects2[i][0]

        # Check if start points of defects are close
        if np.linalg.norm(contour1[d1[0]] - contour2[d2[0]]) > threshold_dist:
            return False

        # Check if end points of defects are close
        if np.linalg.norm(contour1[d1[1]] - contour2[d2[1]]) > threshold_dist:
            return False

        # Check if depth (depth point of the defect) is close
        if np.abs(d1[3] - d2[3]) > threshold_depth:
            return False

    return True


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Process arguments.')
    parser.add_argument('--input_2d', type=str,
                        default='data/new_test_scene/output/input_2d_88100095218.pkl',
                        help='2d vertices')
    parser.add_argument('--input_3d_proj', type=str,
                        default='data/new_test_scene/output/lidar_project_info_881000952181.csv',
                        help='3d projection vertices')
    parser.add_argument('--use_lidar_proj_cols', type=list,
                        default=['PROJ_SCREEN_X', 'PROJ_SCREEN_Y', 'I', 'BOUND'],
                        help='list of columns to load when reading the input lidar projection data from input_3d_proj')
    parser.add_argument('--image_width', type=int, default=2356,
                        help='image width for lidar projections in input_3d_proj')
    parser.add_argument('--image_height', type=int, default=1200,
                        help='image height for lidar projections in input_3d_proj')

    args = parser.parse_args()
    input_2d = args.input_2d
    input_3d_proj = args.input_3d_proj
    use_lidar_proj_cols = args.use_lidar_proj_cols
    image_width = args.image_width
    image_height = args.image_height

    input_2d_points = load_pickle_data(input_2d)

    input_3d_proj_df = pd.read_csv(input_3d_proj, usecols=use_lidar_proj_cols, dtype=int)

    input_3d_proj_df = input_3d_proj_df[(input_3d_proj_df.PROJ_SCREEN_X > 0) &
                                        (input_3d_proj_df.PROJ_SCREEN_X < image_width) &
                                        (input_3d_proj_df.PROJ_SCREEN_Y > 0) &
                                        (input_3d_proj_df.PROJ_SCREEN_Y < image_height)]

    input_lidar_bounds = input_3d_proj_df[input_3d_proj_df['BOUND'] == 1]
    print(input_3d_proj_df.shape, input_lidar_bounds.shape)
    lidar_proj_df = input_lidar_bounds[['PROJ_SCREEN_X', 'PROJ_SCREEN_Y']]
    lidar_img = np.zeros((image_height, image_width), dtype=np.uint8)
    lidar_img[lidar_proj_df['PROJ_SCREEN_Y'], lidar_proj_df['PROJ_SCREEN_X']] = 255
    cv2.fillPoly(lidar_img, pts=[lidar_proj_df.to_numpy()], color=(127, 127, 127))

    process_img, process_contour = process_boundary_in_image(lidar_img)
    process_img[process_img != 0] = 0
    cv2.drawContours(process_img, process_contour, -1, (127, 127, 127), 1)
    match_deg = match_shapes(input_2d_points, process_contour[0])
    print(match_deg)

    sys.exit()
