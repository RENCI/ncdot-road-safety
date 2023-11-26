import sys
import argparse
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import pandas as pd
from utils import load_pickle_data


parser = argparse.ArgumentParser(description='Process arguments.')
parser.add_argument('--input_2d', type=str,
                    # default='data/d13_route_40001001011/oneformer/output/aerial_lidar_test/input_2d_92600542024.pkl',
                    default='data/new_test_scene/output/input_2d_88100095218.pkl',
                    help='2d vertices')
parser.add_argument('--input_3d_proj', type=str,
                    # default='data/d13_route_40001001011/oneformer/output/aerial_lidar_test/'
                    #         'lidar_project_info_926005420241.csv',
                    default='data/new_test_scene/output/lidar_project_info_881000952181.csv',
                    help='3d projection vertices')
parser.add_argument('--overlay_bg_image_path', type=str,
                    # default='data/d13_route_40001001011/other/926005420241.jpg',
                    default='data/new_test_scene/images/881000952181.jpg',
                    help='original background image for overlay with the scatter plots')
parser.add_argument('--show_intersect_only', action="store_true",
                    help='show the intersection alignment only')
parser.add_argument('--show_bg_img', action="store_true",
                    help='show the background image')


args = parser.parse_args()
input_2d = args.input_2d
input_3d_proj = args.input_3d_proj
overlay_bg_image_path = args.overlay_bg_image_path
show_intersect_only = args.show_intersect_only
show_bg_img = args.show_bg_img

input_2d_points = load_pickle_data(input_2d)

bg_img = mpimg.imread(overlay_bg_image_path)
image_height, image_width, _ = bg_img.shape

if show_intersect_only:
    input_3d_proj_df = pd.read_csv(input_3d_proj, usecols=['PROJ_SCREEN_X', 'PROJ_SCREEN_Y', 'I'], dtype=int)
    input_3d_proj_df = input_3d_proj_df[input_3d_proj_df['I'] > 0]
else:
    input_3d_proj_df = pd.read_csv(input_3d_proj, usecols=['PROJ_SCREEN_X', 'PROJ_SCREEN_Y'], dtype=int)

print(input_3d_proj_df.shape, min(input_3d_proj_df.PROJ_SCREEN_X), max(input_3d_proj_df.PROJ_SCREEN_X))
print(min(input_3d_proj_df.PROJ_SCREEN_Y), max(input_3d_proj_df.PROJ_SCREEN_Y))
print(image_width, image_height)
input_3d_proj_df = input_3d_proj_df[(input_3d_proj_df.PROJ_SCREEN_X > 0) &
                                    (input_3d_proj_df.PROJ_SCREEN_X < image_width) &
                                    (input_3d_proj_df.PROJ_SCREEN_Y > 0) &
                                    (input_3d_proj_df.PROJ_SCREEN_Y < image_height)]
print(input_3d_proj_df.shape)
plt.scatter(input_2d_points[:, 0], image_height - input_2d_points[:, 1], s=20)
plt.scatter(input_3d_proj_df['PROJ_SCREEN_X'], image_height - input_3d_proj_df['PROJ_SCREEN_Y'], s=20)
if show_bg_img:
    plt.imshow(bg_img, extent=[0, image_width-1, 0, image_height-1])
plt.title('Road alignment in screen coordinate system')
plt.ylabel('Y')
plt.xlabel('X')
if show_bg_img:
    plt.grid(False)
else:
    plt.grid(True)
# plt.legend(loc='lower left')
plt.show()
sys.exit()
