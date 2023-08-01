import argparse

import numpy as np
from scipy.linalg import svd
import pandas as pd
import matplotlib.pyplot as plt


def fit_plane_lmeds(points, num_iterations=2000, inlier_threshold=0.1):
    best_inliers = []
    all_indices = np.arange(len(points))
    for i in range(num_iterations):
        try:
            # Step 1: Randomly select 3 points to form a candidate plane
            idx = np.random.choice(all_indices, 3, replace=False)
            # remove sampled indices from all_indices to ensure next sampling will not repeat already sampled points
            all_indices = np.setdiff1d(all_indices, list(idx))
            candidate_plane_points = points[idx]

            # Step 2: Fit a plane to the candidate points using SVD
            A = np.vstack([candidate_plane_points[:, 0], candidate_plane_points[:, 1],
                           candidate_plane_points[:, 2]]).T
            _, _, v = svd(A)
            plane_normal = v[-1, :]
            plane_normal /= np.linalg.norm(plane_normal)

            # Step 3: Calculate the distance from each point to the plane
            # distances = np.square(np.dot(points - candidate_plane_points[0], plane_normal))
            # distance = np.median(distances)
            # if distance < min_dist:
            #     # Step 4: Count inliers (points whose distance to the plane is within the inlier threshold)
            #     best_inliers = points[distances < inlier_threshold]
            #     min_dist = distance
            #     print(f'min_dist: {min_dist}, len(best_inliers) = {len(best_inliers)}')
            distances = np.abs(np.dot(points - candidate_plane_points[0], plane_normal))
            # Step 4: Count inliers (points whose distance to the plane is within the inlier threshold)
            inliers = points[distances < inlier_threshold]
            # Step 5: Keep the plane with the most inliers
            if len(inliers) > len(best_inliers):
                best_inliers = inliers
            if len(all_indices) <= 0:
                break
        except ValueError:
            break

    # Step 6: Refit the plane using all inliers
    print(f'length of best_inliers: {len(best_inliers)}')
    A = np.vstack([best_inliers[:, 0], best_inliers[:, 1], best_inliers[:, 2]]).T
    # A = np.vstack([points[:, 0], points[:, 1], points[:, 2]]).T
    _, _, v = svd(A)
    best_plane_params = v[-1, :]
    best_plane_params /= np.linalg.norm(best_plane_params)

    # Calculate d from the fitted plane parameters
    d = -np.dot(best_plane_params, best_inliers[0])
    return np.append(best_plane_params, d), best_inliers


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Process arguments.')
    parser.add_argument('--input_depth_map', type=str,
                        default='data/d13_route_40001001011/oneformer/output/route_batch_3d/'
                                'road_alignment_with_lidar_926005420241.csv',
                        help='input file that contains reverse-projected segmented road boundary x, y, z vertices '
                             'with z as the predicted depth')
    parser.add_argument('--input_lidar_depth_map', type=str,
                        default='data/d13_route_40001001011/oneformer/output/route_batch_3d/'
                                'lidar_project_info_926005420241_depth.csv',
                        help='input file that contains reverse-projected LIDAR road vertices x, y, z vertices')
    parser.add_argument('--output_plane_param_file', type=str,
                        default='data/d13_route_40001001011/oneformer/output/route_batch_3d/'
                                'fit_depth_plane_pts_926005420241.csv',
                        help='output file for fit plane parameters of the input 3D depth map')
    parser.add_argument('--use_test_data', action='store_true',
                        help='use synthetically generated data to test plane fitting code or use real data')

    args = parser.parse_args()
    input_depth_map = args.input_depth_map
    input_lidar_depth_map = args.input_lidar_depth_map
    output_plane_param_file = args.output_plane_param_file
    use_test_data = args.use_test_data

    np.random.seed(0)

    if use_test_data:
        # Generate some example 3D points lying on a plane
        a, b, c, d = 1, 2, 3, 4
        num_points = 100
        x = np.random.rand(num_points) * 10 - 5
        y = np.random.rand(num_points) * 10 - 5
        # z = (-a * x - b * y - d) / c + np.random.randn(num_points) * 0.1
        z = (-a * x - b * y - d) / c
        input_data = np.stack((x, y, z), axis=1)
    else:
        df = pd.read_csv(input_depth_map, usecols=['X_3D', 'Y_3D', 'Z'])
        df = df[['X_3D', 'Y_3D', 'Z']]
        df_lidar = pd.read_csv(input_lidar_depth_map, usecols=['X_3D', 'Y_3D', 'Z', 'WORLD_Z'])
        input_data = df.to_numpy()
        # df_lidar = df_lidar[['X_3D', 'Y_3D', 'WORLD_Z']]
        # input_data = df_lidar.to_numpy()

    if use_test_data:
        d = 1
        coefficients, _, _, _ = np.linalg.lstsq(input_data, -np.ones(num_points),
                                                rcond=None)
        a, b, c = coefficients
        print(a, b, c)

        # plane_params, best_fit_pts = fit_plane_lmeds(input_data)
        # a, b, c, d = plane_params
        # print(a, b, c, d)
        # print(len(best_fit_pts))
    else:
        # Fit the plane using LMedS
        # plane_params, best_fit_pts = fit_plane_lmeds(input_data)
        # a, b, c, d = plane_params
        # print(plane_params)
        # print(len(best_fit_pts), df.shape)
        d = 1
        coefficients, _, _, _ = np.linalg.lstsq(input_data, -np.ones(len(input_data)),
                                               rcond=None)
        a, b, c = coefficients
        print(a, b, c, d)
        # np.savetxt(output_plane_param_file, best_fit_pts, fmt='%.3f',  header='X, Y, Z', comments='')
        # np.savetxt(f'{os.path.splitext(output_plane_param_file)[0]}_params.csv', [plane_params], fmt='%.3f',
        # header='a, b, c, d', comments='')
    # plot raw data
    plt.figure()
    ax = plt.subplot(111, projection='3d')
    if use_test_data:
        ax.scatter(input_data[:, 0], input_data[:, 1], input_data[:, 2], color='b')
    else:
        ax.scatter(df['X_3D'], df['Y_3D'], df['Z'], color='b')
        ax.scatter(df_lidar['X_3D'], df_lidar['Y_3D'], df_lidar['WORLD_Z'], color='r')
    # plot plane
    x_lim = ax.get_xlim()
    y_lim = ax.get_ylim()
    x, y = np.meshgrid(np.arange(x_lim[0], x_lim[1]),
                       np.arange(y_lim[0], y_lim[1]))
    z = np.zeros(x.shape)
    for row in range(x.shape[0]):
        for col in range(x.shape[1]):
            z[row, col] = (-a * x[row, col] - b * y[row, col] - d) / c
    ax.plot_wireframe(x, y, z, rstride=10, cstride=10, color='k')
    # ax.plot_wireframe(x, y, z, color='k')
    ax.set_xlabel('x')
    ax.set_ylabel('y')
    ax.set_zlabel('z')
    plt.show()
