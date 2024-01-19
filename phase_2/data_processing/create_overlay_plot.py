import sys
import argparse
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import pandas as pd
from utils import load_pickle_data, LIDARClass


parser = argparse.ArgumentParser(description='Process arguments.')
parser.add_argument('--input_2d', type=str,
                    # default='data/d13_route_40001001011/oneformer/output/all_lidar_vertices/input_2d_92600542024.pkl',
                    default='data/new_test_scene/lane_test/input_2d_88100095218.pkl',
                    help='2d vertices')
parser.add_argument('--input_3d_proj', type=str,
                    # default='data/d13_route_40001001011/oneformer/output/all_lidar_vertices/'
                    #         'lidar_project_info_926005420241.csv',
                    default='data/new_test_scene/lane_test/lidar_project_info_881000952181.csv',
                    help='3d projection vertices')
parser.add_argument('--overlay_bg_image_path', type=str,
                    # default='data/d13_route_40001001011/other/926005420241.jpg',
                    default='data/new_test_scene/images/881000952181.jpg',
                    help='original background image for overlay with the scatter plots')
parser.add_argument('--image_crossroad_intersect_file', type=str,
                    default='data/new_test_scene/output/image_881000952181_crossroad_intersects.csv',
                    # default='',
                    help='csv file that includes interpolated crossroad intersection points to overlay on the display')
parser.add_argument('--landmark_file', type=str,
                    default='data/new_test_scene/new_test_scene_landmarks_881000952181.csv',
                    # default='',
                    help='input csv file that includes landmark mapping info')
parser.add_argument('--use_lidar_proj_cols', type=list,
                    default=['PROJ_SCREEN_X', 'PROJ_SCREEN_Y', 'C'],
                    help='list of columns to load when reading the input lidar projection data from input_3d_proj')
parser.add_argument('--colormap', type=dict,
                    default={6: 'purple', 2: 'red', 15: 'orange', 1: 'green', 11: 'blue'},
                    # default={3: 'purple', 5: 'blue', 2: 'green', 4: 'orange', 14: 'pink', 1: 'yellow', 11: 'red'},
                    # default='',
                    help='colormap to map LIDAR point classification to color')
parser.add_argument('--show_intersect_only', action="store_true",
                    help='show the intersection alignment only')
parser.add_argument('--show_lidar_road_only', action="store_true",
                    help='show LIDAR road only')
parser.add_argument('--show_bg_img', action="store_true",
                    help='show the background image')


args = parser.parse_args()
input_2d = args.input_2d
input_3d_proj = args.input_3d_proj
overlay_bg_image_path = args.overlay_bg_image_path
image_crossroad_intersect_file = args.image_crossroad_intersect_file
landmark_file = args.landmark_file
use_lidar_proj_cols = args.use_lidar_proj_cols
colormap = args.colormap
show_intersect_only = args.show_intersect_only
show_lidar_road_only = args.show_lidar_road_only
show_bg_img = args.show_bg_img

input_2d_points = load_pickle_data(input_2d)

bg_img = mpimg.imread(overlay_bg_image_path)
image_height, image_width, _ = bg_img.shape

input_3d_proj_df = pd.read_csv(input_3d_proj, usecols=use_lidar_proj_cols, dtype=int)

if landmark_file:
    landmark_df = pd.read_csv(landmark_file, usecols=['LANDMARK_SCREEN_X', 'LANDMARK_SCREEN_Y', 'C'])
    landmark_size = len(landmark_df)
    input_3d_proj_lm_df = input_3d_proj_df[len(input_3d_proj_df)-landmark_size:]
    input_3d_proj_df = input_3d_proj_df[:len(input_3d_proj_df)-landmark_size]

if show_intersect_only:
    input_3d_proj_df = input_3d_proj_df[input_3d_proj_df['I'] > 0]
elif show_lidar_road_only:
    input_3d_proj_df = input_3d_proj_df[input_3d_proj_df.C == LIDARClass.ROAD.value]


input_3d_proj_df = input_3d_proj_df[(input_3d_proj_df.PROJ_SCREEN_X > 0) &
                                    (input_3d_proj_df.PROJ_SCREEN_X < image_width) &
                                    (input_3d_proj_df.PROJ_SCREEN_Y > 0) &
                                    (input_3d_proj_df.PROJ_SCREEN_Y < image_height)]

plt.scatter(input_2d_points[:, 0], image_height - input_2d_points[:, 1], s=20)
if 'BOUND' in use_lidar_proj_cols:
    bound_ldf = input_3d_proj_df[input_3d_proj_df['BOUND'] > 0]
    plt.scatter(bound_ldf['PROJ_SCREEN_X'], image_height - bound_ldf['PROJ_SCREEN_Y'], s=10, c='c')
if 'I' in use_lidar_proj_cols and 'BOUND' in use_lidar_proj_cols:
    remain_ldf = input_3d_proj_df[(input_3d_proj_df['I'] == 0) & (input_3d_proj_df['BOUND'] == 0)]
elif 'I' in use_lidar_proj_cols:
    remain_ldf = input_3d_proj_df[input_3d_proj_df['I'] == 0]
elif 'BOUND' in use_lidar_proj_cols:
    remain_ldf = input_3d_proj_df[input_3d_proj_df['BOUND'] == 0]
else:
    remain_ldf = input_3d_proj_df

if colormap:
    plt.scatter(remain_ldf['PROJ_SCREEN_X'], image_height - remain_ldf['PROJ_SCREEN_Y'], s=10,
                c=remain_ldf['C'].map(colormap), label=remain_ldf['C'])
else:
    plt.scatter(remain_ldf['PROJ_SCREEN_X'], image_height - remain_ldf['PROJ_SCREEN_Y'], s=10)

if show_bg_img:
    plt.imshow(bg_img, extent=[0, image_width-1, 0, image_height-1])
if image_crossroad_intersect_file:
    cr_inter_df = pd.read_csv(image_crossroad_intersect_file)
    plt.scatter(cr_inter_df['X'], image_height - cr_inter_df['Y'], s=20, c='g')

if 'I' in use_lidar_proj_cols:
    intersect_ldf =input_3d_proj_df[input_3d_proj_df['I'] > 0]
    plt.scatter(intersect_ldf['PROJ_SCREEN_X'], image_height - intersect_ldf['PROJ_SCREEN_Y'], s=10, c='#001100')

if landmark_file:
    plt.scatter(landmark_df['LANDMARK_SCREEN_X'], image_height - landmark_df['LANDMARK_SCREEN_Y'], s=10, c='#880000')
    plt.scatter(input_3d_proj_lm_df['PROJ_SCREEN_X'], image_height - input_3d_proj_lm_df['PROJ_SCREEN_Y'], s=10,
                c='#ff0000')
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
