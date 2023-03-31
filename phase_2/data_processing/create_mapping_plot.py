import argparse
import matplotlib.pyplot as plt
import pickle
import numpy as np


parser = argparse.ArgumentParser(description='Process arguments.')
parser.add_argument('--input_match_2d_3d', type=str,
                    default='data/d13_route_40001001011/oneformer/output/matches_2d_3d.csv',
                    help='2d-3d matched vertices')
parser.add_argument('--input_match_2d_3d_indices', type=str,
                    default='data/d13_route_40001001011/oneformer/output/matches_2d_3d_indices.csv',
                    help='2d-3d matched vertex indices')
parser.add_argument('--input_2d', type=str,
                    default='data/d13_route_40001001011/oneformer/output/input_2d.pkl',
                    help='2d vertices')
parser.add_argument('--input_3d', type=str,
                    default='data/d13_route_40001001011/oneformer/output/input_3d.pkl',
                    help='3d vertices')

args = parser.parse_args()
input_match_2d_3d = args.input_match_2d_3d
input_match_2d_3d_indices = args.input_match_2d_3d_indices
input_2d = args.input_2d
input_3d = args.input_3d
aspect_ratio = 2748/2198

with open(input_2d, 'rb') as f:
    input_2d_points = pickle.load(f)[0]
with open(input_3d, 'rb') as f:
    input_3d_points = pickle.load(f)[0]
print(f'input 2d numpy array shape: {input_2d_points.shape}, input 3d numpy array shape: {input_3d_points.shape}')
max_2d = np.amax(input_2d_points, axis=0)
min_2d = np.amin(input_2d_points, axis=0)
norm_2d_points = (input_2d_points - min_2d) * np.array([200*aspect_ratio, 200]) // (max_2d-min_2d)
plt.scatter(norm_2d_points[:, 0], 200 - norm_2d_points[:, 1], s=10)

max_3d = np.amax(input_3d_points, axis=0)
min_3d = np.amin(input_3d_points, axis=0)
norm_3d_points = (input_3d_points - min_3d) * 200 // (max_3d-min_3d)
plt.scatter(norm_3d_points[:, 0] + 500, 200 - norm_3d_points[:, 1], s=10)

plt.title('Scatter plot of 2D and 3D vertices')
plt.ylabel('Y')
plt.xlabel('X')
plt.grid(True)
# plt.legend(loc='lower left')
plt.show()
#plt.savefig(output_file)
