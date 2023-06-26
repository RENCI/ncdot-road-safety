import argparse
import matplotlib.pyplot as plt
import numpy as np
from pypfm import PFMLoader
from PIL import Image
from utils import get_depth_data


parser = argparse.ArgumentParser(description='Process arguments.')
parser.add_argument('--input_file_1', type=str,
                    default='../midas/images/output/grayscale_926005420241.pfm',
                    help='input file 1 with path to create scatter plot from')
parser.add_argument('--input_file_2', type=str,
                    default='../midas/images/output/grayscale_926005421055.pfm',
                    help='input file 2 with path to create scatter plot from')
parser.add_argument('--image_width', type=int, default=2748, help='image width')
parser.add_argument('--image_height', type=int, default=2198, help='image height')
parser.add_argument('--point_1_yx', type=tuple, default=(752, 270), help='(y, x) coordinate of point for computing '
                                                                         'depth of object of interest in '
                                                                         'input_file_1 image')
parser.add_argument('--point_2_yx', type=tuple, default=(1030, 2639), help='(y, x) coordinate of point for '
                                                                               'computing depth of object of interest '
                                                                               'in input_file_2 image')
parser.add_argument('--output_file', type=str,
                    default='../midas/images/output/scatter_plot_pole_image_2_front_to_image_3_left.pdf',
                    help='output pdf file for the generated scatter plot')

args = parser.parse_args()
input_file_1 = args.input_file_1
input_file_2 = args.input_file_2
image_width = args.image_width
image_height = args.image_height
point_1_yx = args.point_1_yx
point_2_yx = args.point_2_yx
output_file = args.output_file


if input_file_1.endswith('.pfm'):
    loader = PFMLoader((image_width, image_height), color=False, compress=False)
    pfm_1 = get_depth_data(loader, input_file_1)
    pfm_2 = get_depth_data(loader, input_file_2)
    print(f'image 1 size: {pfm_1.shape}, image 2 size: {pfm_2.shape}')

    # first column (x=0) of the first image
    X = pfm_1[:, 0]
    # last column (x=image_width-1) of the second image
    Y = pfm_2[:, image_width-1]
    min_1 = pfm_1.min()
    max_1 = pfm_1.max()
    min_2 = pfm_2.min()
    max_2 = pfm_2.max()
    depth_1 = (pfm_1[point_1_yx[0], point_1_yx[1]]-min_1)/(max_1-min_1)
    depth_2 = (pfm_2[point_2_yx[0], point_2_yx[1]] - min_2) / (max_2 - min_2)
    print(f'depth of point_1 of the first image on X, depth: {pfm_1[point_1_yx[0], point_1_yx[1]]}, '
          f'normalized depth: {depth_1}, inversed normalized depth: {1-depth_1}, min: {min_1}, max: {max_1}')
    print(f'depth of point_2 of the second image on Y, depth: {pfm_2[point_2_yx[0], point_2_yx[1]]}, '
          f'normalized depth: {depth_2}, inversed normalized depth: {1 - depth_2}, min: {min_2}, max: {max_2}')
elif input_file_1.endswith('.png'):
    data_1 = np.asarray(Image.open(input_file_1))
    data_2 = np.asarray(Image.open(input_file_2))
    X = data_1[:, 0]
    Y = data_2[:, image_width-1]

plt.scatter(X, Y, s=20)
plt.title('Scatter plot of predicted depths for 2 images')
plt.ylabel('Depth of last column of the left image')
plt.xlabel('Depth of first column of the front image')
plt.grid(True)
# plt.legend(loc='lower left')
plt.show()
#plt.savefig(output_file)
