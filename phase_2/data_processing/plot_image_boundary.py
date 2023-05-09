import argparse
import matplotlib.pyplot as plt
from utils import get_data_from_image
from get_road_boundary_points import get_image_road_boundary_points


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Process arguments.')
    parser.add_argument('--image_file_name', type=str, default='data/d13_route_40001001011/oneformer/926005420241.png',
                        help='input image file name with path')

    args = parser.parse_args()
    image_file_name = args.image_file_name
    image_width, image_height, seg_img = get_data_from_image(image_file_name)
    _, _, road_contours = get_image_road_boundary_points(image_file_name)
    print(f'number of returned contours: {len(road_contours)}')
    # Plot the boundary on top of the original image
    plt.imshow(seg_img)
    plt.plot(road_contours[0][:, 0], road_contours[0][:, 1], 'r-', linewidth=2)

    plt.show()
