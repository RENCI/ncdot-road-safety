import argparse
import matplotlib.pyplot as plt
import pandas as pd

X_SCALING_FACTOR = 2748
Y_SCALING_FACTOR = 2198

parser = argparse.ArgumentParser(description='Process arguments.')
parser.add_argument('--input_3d', type=str,
                    default='data/d13_route_40001001011/oneformer/output/route_batch_3d/lidar_project_info_926005420241.csv',
                    help='3d vertices')
parser.add_argument('--input_2d', type=str,
                    default='data/d13_route_40001001011/oneformer/output/route_batch_3d/road_alignment_with_lidar_926005420241.csv',
                    help='2d vertices projected to 3d')

args = parser.parse_args()
input_3d = args.input_3d
input_2d = args.input_2d

df_2d = pd.read_csv(input_2d)
df_3d = pd.read_csv(input_3d)

fig = plt.figure(figsize=(10, 8))
ax3 = fig.add_subplot(111, projection='3d')
ax3.scatter3D(df_3d['WORLD_X'], df_3d['WORLD_Y'], df_3d['WORLD_Z'])
ax3.scatter3D(df_2d['X_3D'], df_2d['Y_3D'], df_2d['Z'])
ax3.set_xlabel('X')
ax3.set_ylabel('Y')
ax3.set_zlabel('Z')

ax3.grid(True)
plt.show()
