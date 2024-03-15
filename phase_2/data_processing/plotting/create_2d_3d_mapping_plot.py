import argparse
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from collections import OrderedDict
from utils import load_pickle_data


SCALING_FACTOR = 400
X_OFFSET_3D = 500
ASPECT_RATIO = 2748/2198

parser = argparse.ArgumentParser(description='Process arguments.')
parser.add_argument('--input_match_2d_3d_indices', type=str,
                    default='data/d13_route_40001001011/oneformer/output/road_alignment_with_lidar.csv',
                    help='2d-3d matched vertex indices')
parser.add_argument('--input_2d', type=str,
                    default='data/d13_route_40001001011/oneformer/output/input_2d.pkl',
                    help='2d vertices')
parser.add_argument('--input_3d', type=str,
                    default='data/d13_route_40001001011/oneformer/output/input_3d.pkl',
                    help='3d vertices')

args = parser.parse_args()
input_match_2d_3d_indices = args.input_match_2d_3d_indices
input_2d = args.input_2d
input_3d = args.input_3d

input_2d_points = load_pickle_data(input_2d)
input_3d_points = load_pickle_data(input_3d)
print(f'input 2d numpy array shape: {input_2d_points.shape}, input 3d numpy array shape: {input_3d_points.shape}')
max_2d = np.amax(input_2d_points, axis=0)
min_2d = np.amin(input_2d_points, axis=0)
norm_2d_points = (input_2d_points - min_2d) * np.array([SCALING_FACTOR*ASPECT_RATIO, SCALING_FACTOR]) // (max_2d-min_2d)

max_3d = np.amax(input_3d_points, axis=0)
min_3d = np.amin(input_3d_points, axis=0)
norm_3d_points = (input_3d_points - min_3d) * SCALING_FACTOR // (max_3d-min_3d)

match_2d_3d_indices = pd.read_csv(input_match_2d_3d_indices, header=None, names=['2d', '3d'], dtype=int)
print(f'match_2d_3d_indices shape: {match_2d_3d_indices.shape}')
match_dict = OrderedDict()
for val_2d, val_3d in match_2d_3d_indices.groupby('2d'):
    match_dict[val_2d] = val_3d['3d'].tolist()[0]
print(f'match_dict size: {len(match_dict)}')
count = 0
for key, val in match_dict.items():
    # curved segment: count < 100
    # left side of the road: 100 < count < 1500
    # right side of the road: count > 2100
    # if count % 20 == 0:
    plt.plot([norm_2d_points[key, 0], norm_3d_points[val, 0] + X_OFFSET_3D],
             [SCALING_FACTOR-norm_2d_points[key, 1], norm_3d_points[val, 1]], linewidth=1,
             color='gray')
    count += 1

plt.scatter(norm_2d_points[:, 0], SCALING_FACTOR-norm_2d_points[:, 1], s=20)
plt.scatter(norm_3d_points[:, 0] + X_OFFSET_3D, norm_3d_points[:, 1], s=10)

plt.title('2D road vertices and 3D road vertices mapping')
plt.ylabel('Y')
plt.xlabel('X')
plt.grid(True)
# plt.legend(loc='lower left')
plt.show()
#plt.savefig(output_file)
