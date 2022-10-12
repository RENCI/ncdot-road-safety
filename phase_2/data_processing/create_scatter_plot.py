import argparse
import matplotlib.pyplot as plt
import numpy as np
from pypfm import PFMLoader
from PIL import Image


parser = argparse.ArgumentParser(description='Process arguments.')
parser.add_argument('--input_file_1', type=str,
                    default='../images/output/926005420241.pfm',
                    help='input file 1 with path to create scatter plot from')
parser.add_argument('--input_file_2', type=str,
                    default='../images/output/926005421055.pfm',
                    help='input file 2 with path to create scatter plot from')
parser.add_argument('--image_width', type=int, default=2748, help='image width')
parser.add_argument('--image_height', type=int, default=2198, help='image height')
parser.add_argument('--output_file', type=str,
                    default='../images/output/scatter_plot_pole_image_2_front_to_image_3_left.pdf',
                    help='output pdf file for the generated scatter plot')

args = parser.parse_args()
input_file_1 = args.input_file_1
input_file_2 = args.input_file_2
image_width = args.image_width
image_height = args.image_height
output_file = args.output_file


if input_file_1.endswith('.pfm'):
    loader = PFMLoader((image_width, image_height), color=False, compress=False)
    pfm_1 = loader.load_pfm(input_file_1)
    # flip columns since they are inverse depth maps
    pfm_1 = np.flipud(pfm_1)
    pfm_2 = loader.load_pfm(input_file_2)
    # flip columns since they are inverse depth maps
    pfm_2 = np.flipud(pfm_2)
    print(f'image 1 size: {pfm_1.shape}, image 2 size: {pfm_2.shape}')

    # first column of the first image
    X = pfm_1[:, 0]
    # last column of the second image
    Y = pfm_2[:, image_width-1]
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
