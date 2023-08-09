import argparse
import matplotlib.pyplot as plt
from utils import get_data_from_image
import numpy as np
from get_road_boundary_points import get_image_road_points


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Process arguments.')
    parser.add_argument('--image_file_name', type=str, default='data/d13_route_40001001011/oneformer/926005420241.png',
                        help='input image file name with path')
    parser.add_argument('--boundary_only', action="store_true",
                        help='whether to plot boundary only or all road pixels')

    args = parser.parse_args()
    image_file_name = args.image_file_name
    boundary_only = args.boundary_only
    image_width, image_height, seg_img = get_data_from_image(image_file_name)
    _, _, road_contours = get_image_road_points(image_file_name, boundary_only=boundary_only)
    # Plot the boundary on top of the original image
    plt.imshow(seg_img)
    if boundary_only:
        plt.plot(road_contours[0][:, 0], road_contours[0][:, 1], 'r-', linewidth=2)
    else:
        road_data = np.array(road_contours[0])
        plt.scatter(road_data[:, 0], road_data[:, 1], s=1, c='r')
    plt.show()
