import numpy as np
import sys
import argparse
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import pandas as pd
from data_processing.utils import load_pickle_data, LIDARClass


def parse_colormap(value):
    try:
        return dict(item.split(':') for item in value.split(','))
    except ValueError:
        raise argparse.ArgumentTypeError("Colormap must be in the format 'key1:color1,key2:color2'")


parser = argparse.ArgumentParser(description='Process arguments.')
parser.add_argument('--input_2d', type=str,
                    default='../data/d13_route_40001001012/test/input_2d_88100043522.csv',
                    help='2d vertices')
parser.add_argument('--input_3d_proj', type=str,
                    default='../data/d13_route_40001001012/test/lidar_project_info_88100043522.csv',
                    help='3d projection vertices')
parser.add_argument('--overlay_bg_image_path', type=str,
                    default='../data/d13_route_40001001012/images/881000435221.jpg',
                    help='original background image for overlay with the scatter plots')
parser.add_argument('--use_lidar_proj_cols', nargs='+',
                    default=['PROJ_SCREEN_X', 'PROJ_SCREEN_Y', 'C', 'BOUND', 'SIDE'],
                    # default=['PROJ_SCREEN_X', 'PROJ_SCREEN_Y'],
                    help='list of columns to load when reading the input lidar projection data from input_3d_proj')
parser.add_argument('--colormap', type=parse_colormap,
                    default={6: 'purple', 2: 'cyan', 15: 'orange', 1: 'green', 11: 'blue', 12: 'yellow', 3: 'brown',
                             4: 'brown', 5: 'brown', 14: 'pink'},
                    help='colormap to map LIDAR point classification to color')
parser.add_argument('--show_lidar_road_only', action="store_true",
                    help='show LIDAR road only')
parser.add_argument('--show_bg_img', action="store_true",
                    help='show the background image')


args = parser.parse_args()
input_2d = args.input_2d
input_3d_proj = args.input_3d_proj
overlay_bg_image_path = args.overlay_bg_image_path
use_lidar_proj_cols = args.use_lidar_proj_cols
colormap = args.colormap
show_lidar_road_only = args.show_lidar_road_only
show_bg_img = args.show_bg_img

bg_img = mpimg.imread(overlay_bg_image_path)
image_height, image_width, _ = bg_img.shape

input_3d_proj_df = pd.read_csv(input_3d_proj, usecols=use_lidar_proj_cols, dtype=int)
if show_lidar_road_only:
    if 'C' in input_3d_proj_df.columns:
        input_3d_proj_df = input_3d_proj_df[(input_3d_proj_df.C == LIDARClass.ROAD.value) |
                                            (input_3d_proj_df.C == LIDARClass.BRIDGE.value)]
    if 'BOUND' in input_3d_proj_df.columns:
        input_3d_proj_df = input_3d_proj_df[input_3d_proj_df.BOUND == 1]
print(f'image_height: {image_height}, image_width: {image_width}, len: {len(input_3d_proj_df)}')

if overlay_bg_image_path.endswith('1.jpg'):
    xb_min = 0
    xb_max = image_width
elif overlay_bg_image_path.endswith('5.jpg'):
    # left image
    xb_min = -image_width
    xb_max = 0
else:
    # right view
    xb_min = image_width
    xb_max = image_width * 2

input_3d_proj_df = input_3d_proj_df[(input_3d_proj_df.PROJ_SCREEN_X > xb_min) &
                                    (input_3d_proj_df.PROJ_SCREEN_X < xb_max) &
                                    (input_3d_proj_df.PROJ_SCREEN_Y > 0) &
                                    (input_3d_proj_df.PROJ_SCREEN_Y < image_height)]

if not overlay_bg_image_path.endswith('1.jpg'):
    input_3d_proj_df['PROJ_SCREEN_X'] = input_3d_proj_df['PROJ_SCREEN_X'] - xb_min
else:
    if input_2d.endswith('.pkl'):
        input_2d_points = load_pickle_data(input_2d)
        plt.scatter(input_2d_points[:, 0], image_height - input_2d_points[:, 1], s=20)
    else:
        input_2d_df = pd.read_csv(input_2d)
        # colors = np.where(input_2d_df['SIDE'] > 0, 'blue', 'green')
        # plt.scatter(input_2d_df['X'], image_height - input_2d_df['Y'], s=20, c=colors)
        plt.scatter(input_2d_df['X'], image_height - input_2d_df['Y'], s=20)

if not show_lidar_road_only and 'BOUND' in use_lidar_proj_cols:
    bound_ldf = input_3d_proj_df[input_3d_proj_df['BOUND'] > 0]
    plt.scatter(bound_ldf['PROJ_SCREEN_X'], image_height - bound_ldf['PROJ_SCREEN_Y'], s=10, c='c')

if 'BOUND' in use_lidar_proj_cols:
    if show_lidar_road_only:
        remain_ldf = input_3d_proj_df
    else:
        remain_ldf = input_3d_proj_df[input_3d_proj_df['BOUND'] == 0]
else:
    remain_ldf = input_3d_proj_df

if colormap:
    # plt.scatter(remain_ldf['PROJ_SCREEN_X'], image_height - remain_ldf['PROJ_SCREEN_Y'], s=10,
    #             c=remain_ldf['C'].map(colormap), label=remain_ldf['C'])
    # colors_3d = np.where(remain_ldf['SIDE'] > 0, 'blue', 'green')
    # plt.scatter(remain_ldf['PROJ_SCREEN_X'], image_height - remain_ldf['PROJ_SCREEN_Y'], s=10, c=colors_3d)
    plt.scatter(remain_ldf['PROJ_SCREEN_X'], image_height - remain_ldf['PROJ_SCREEN_Y'], s=10, c='blue')
else:
    plt.scatter(remain_ldf['PROJ_SCREEN_X'], image_height - remain_ldf['PROJ_SCREEN_Y'], s=10)

if show_bg_img:
    plt.imshow(bg_img, extent=[0, image_width - 1, 0, image_height - 1])

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
