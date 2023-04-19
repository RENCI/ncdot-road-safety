import argparse
import matplotlib.pyplot as plt
from mpl_toolkits import mplot3d
import pandas as pd
import numpy as np
from utils import load_pickle_data


parser = argparse.ArgumentParser(description='Process arguments.')
parser.add_argument('--input_2d', type=str,
                    default='data/d13_route_40001001011/oneformer/output/input_2d.pkl',
                    help='2d vertices')
parser.add_argument('--input_3d_proj', type=str,
                    default='data/d13_route_40001001011/oneformer/output/lidar_project_info.csv',
                    help='3d projection vertices')

args = parser.parse_args()
input_2d = args.input_2d
input_3d_proj = args.input_3d_proj

input_2d_points = load_pickle_data(input_2d)
max_2d = np.amax(input_2d_points, axis=0)
min_2d = np.amin(input_2d_points, axis=0)

input_3d_proj_df = pd.read_csv(input_3d_proj, usecols=['PROJ_SCREEN_X', 'PROJ_SCREEN_Y'], dtype=int)

plt.scatter(input_2d_points[:, 0], max_2d[1] - input_2d_points[:, 1], s=20)
plt.scatter(input_3d_proj_df['PROJ_SCREEN_X'], max_2d[1] - input_3d_proj_df['PROJ_SCREEN_Y'], s=20)

plt.title('2D road vertices & 3D projected road vertices in screen coordinate system')
plt.ylabel('Y')
plt.xlabel('X')
plt.grid(True)
# plt.legend(loc='lower left')
plt.show()
