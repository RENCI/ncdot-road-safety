import argparse
import matplotlib.pyplot as plt
import pandas as pd
from utils import load_pickle_data, IMAGE_HEIGHT


parser = argparse.ArgumentParser(description='Process arguments.')
parser.add_argument('--input_2d', type=str,
                    default='data/d13_route_40001001011/oneformer/output/route_batch/input_2d_92600555627.pkl',
                    help='2d vertices')
parser.add_argument('--input_3d_proj', type=str,
                    default='data/d13_route_40001001011/oneformer/output/route_batch/lidar_project_info_926005556271.csv',
                    help='3d projection vertices')

args = parser.parse_args()
input_2d = args.input_2d
input_3d_proj = args.input_3d_proj

input_2d_points = load_pickle_data(input_2d)

input_3d_proj_df = pd.read_csv(input_3d_proj, usecols=['PROJ_SCREEN_X', 'PROJ_SCREEN_Y'], dtype=int)
plt.scatter(input_2d_points[:, 0], IMAGE_HEIGHT - input_2d_points[:, 1], s=20)
plt.scatter(input_3d_proj_df['PROJ_SCREEN_X'], IMAGE_HEIGHT - input_3d_proj_df['PROJ_SCREEN_Y'], s=20)

plt.title('2D road vertices & 3D projected road vertices in screen coordinate system')
plt.ylabel('Y')
plt.xlabel('X')
plt.grid(True)
# plt.legend(loc='lower left')
plt.show()
