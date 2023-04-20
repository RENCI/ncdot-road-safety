import argparse
import matplotlib.pyplot as plt
import pandas as pd

X_SCALING_FACTOR = 2748
Y_SCALING_FACTOR = 2198

parser = argparse.ArgumentParser(description='Process arguments.')
parser.add_argument('--input_3d_proj', type=str,
                    default='data/d13_route_40001001011/oneformer/output/lidar_project_info.csv',
                    help='3d projection vertices')

args = parser.parse_args()
input_3d_proj = args.input_3d_proj

input_3d_proj_df = pd.read_csv(input_3d_proj, usecols=['PROJ_X', 'PROJ_Y', 'WORLD_X', 'WORLD_Y', 'WORLD_Z'],
                               dtype=float)

fig = plt.figure()
fig.tight_layout(pad=10.0)
ax3 = fig.add_subplot(211, projection='3d')
# Data for three-dimensional points
ax3.scatter3D(input_3d_proj_df['WORLD_X'], input_3d_proj_df['WORLD_Y'], input_3d_proj_df['WORLD_Z'])

ax3.set_xlabel('X')
ax3.set_ylabel('Y')
ax3.set_zlabel('Z')

ax3.grid(True)

ax = fig.add_subplot(212)
ax.scatter(input_3d_proj_df['PROJ_X'].apply(lambda x: x*X_SCALING_FACTOR),
           input_3d_proj_df['PROJ_Y'].apply(lambda y: y*Y_SCALING_FACTOR), s=20)

ax.set_ylabel('Y')
ax.set_xlabel('X')
ax.grid(True)
idx = 11
ax3.plot(input_3d_proj_df['WORLD_X'].iloc[idx], input_3d_proj_df['WORLD_Y'].iloc[idx],
         input_3d_proj_df['WORLD_Z'].iloc[idx], 'ro', markersize=6)
ax.plot(input_3d_proj_df['PROJ_X'].iloc[idx]*X_SCALING_FACTOR, input_3d_proj_df['PROJ_Y'].iloc[idx]*Y_SCALING_FACTOR,
        'ro', markersize=6)
fig.suptitle('LIDAR road vertices in 3D world and projected camera coordinate systems')
plt.show()
