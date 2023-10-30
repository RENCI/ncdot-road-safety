import argparse
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import pandas as pd
from utils import load_pickle_data, IMAGE_HEIGHT, IMAGE_WIDTH


parser = argparse.ArgumentParser(description='Process arguments.')
parser.add_argument('--input_2d', type=str,
                    default='data/d13_route_40001001011/oneformer/output/aerial_lidar_test/input_2d_92600542014.pkl',
                    help='2d vertices')
parser.add_argument('--input_3d_proj', type=str,
                    default='data/d13_route_40001001011/oneformer/output/aerial_lidar_test/'
                            'lidar_project_info_926005420141.csv',
                    help='3d projection vertices')
parser.add_argument('--overlay_bg_image_path', type=str,
                    default='data/d13_route_40001001011/other/926005420141.jpg',
                    help='original background image for overlay with the scatter plots')
parser.add_argument('--show_bg_img', action="store_false",
                    help='show the background image')


args = parser.parse_args()
input_2d = args.input_2d
input_3d_proj = args.input_3d_proj
overlay_bg_image_path = args.overlay_bg_image_path
show_bg_img = args.show_bg_img

input_2d_points = load_pickle_data(input_2d)

input_3d_proj_df = pd.read_csv(input_3d_proj, usecols=['PROJ_SCREEN_X', 'PROJ_SCREEN_Y'], dtype=int)

if show_bg_img:
    bg_img = mpimg.imread(overlay_bg_image_path)

plt.scatter(input_2d_points[:, 0], IMAGE_HEIGHT - input_2d_points[:, 1], s=20)
plt.scatter(input_3d_proj_df['PROJ_SCREEN_X'], IMAGE_HEIGHT - input_3d_proj_df['PROJ_SCREEN_Y'], s=20)
if show_bg_img:
    plt.imshow(bg_img, extent=[0, IMAGE_WIDTH-1, 0, IMAGE_HEIGHT-1])
plt.title('2D road vertices & 3D projected road vertices in screen coordinate system')
plt.ylabel('Y')
plt.xlabel('X')
if show_bg_img:
    plt.grid(False)
else:
    plt.grid(True)
# plt.legend(loc='lower left')
plt.show()
