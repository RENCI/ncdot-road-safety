import argparse
import os
import numpy as np
from scipy.linalg import svd
import pandas as pd
import matplotlib.pyplot as plt
from pypfm import PFMLoader
from get_road_boundary_points import get_image_road_points
from utils import get_depth_data, get_depth_of_pixel
from align_segmented_road_with_lidar import transform_2d_points_to_3d, INIT_CAMERA_PARAMS, \
    FOCAL_LENGTH_X, FOCAL_LENGTH_Y

DEPTH_SCALING_FACTOR = 189


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
                        # default='data/d13_route_40001001011/oneformer/input/926005420241.png',
                        help='input csv file that contains reverse-projected segmented road boundary x, y, z vertices '
                             'with z as the predicted depth or the road pixel depth map in an png image file')
    parser.add_argument('--input_depth_image_filename_pattern', type=str,
                        help='the image pfm depth file pattern with image_base_name to be passed in via string format',
                        default='../midas/images/output/d13_route_40001001011/{image_base_name}-dpt_beit_large_512.pfm')
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
    parser.add_argument('--fit_lidar_road_edge', action='store_false',
                        help='fit lidar road edge or reverse-projected road boundary vertices in the '
                             'intermediate world/camera coordinate system')

    args = parser.parse_args()
    input_depth_map = args.input_depth_map
    input_lidar_depth_map = args.input_lidar_depth_map
    input_depth_image_filename_pattern = args.input_depth_image_filename_pattern
    output_plane_param_file = args.output_plane_param_file
    use_test_data = args.use_test_data
    fit_lidar_road_edge = args.fit_lidar_road_edge

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
        ext = os.path.splitext(input_depth_map)[1]
        if ext == '.csv':
            df = pd.read_csv(input_depth_map, usecols=['X', 'Y', 'X_3D', 'Y_3D', 'Z'])
            df = df[['X_3D', 'Y_3D', 'Z']]
            # df = df[['X', 'Y', 'Z']]
            df_lidar = pd.read_csv(input_lidar_depth_map, usecols=['X_3D', 'Y_3D', 'Z', 'INITIAL_WORLD_Z', 'WORLD_Z'])
            df_lidar = df_lidar[df_lidar['INITIAL_WORLD_Z'] < 200]
            print(df_lidar.shape)
            if fit_lidar_road_edge:
                df_lidar = df_lidar[['X_3D', 'Y_3D', 'Z']]
                input_data = df_lidar.to_numpy()
            else:
                input_data = df.to_numpy()
        elif ext == '.png':
            image_width, image_height, road_contours = get_image_road_points(input_depth_map, boundary_only=True)
            base_img_file_name = os.path.splitext(input_depth_map)[0].split('/')[-1]
            loader = PFMLoader((image_width, image_height), color=False, compress=False)
            input_pfm = get_depth_data(loader, input_depth_image_filename_pattern.format(
                image_base_name=f'{base_img_file_name}'))
            min_depth = input_pfm.min()
            max_depth = input_pfm.max()
            df = pd.DataFrame(road_contours[0], columns=['X', 'Y'])

            df['Z'] = df.apply(lambda row: get_depth_of_pixel(row['Y'], row['X'],
                                                              input_pfm, min_depth, max_depth,
                                                              scaling=DEPTH_SCALING_FACTOR), axis=1)
            input_data = df.to_numpy()
            df = transform_2d_points_to_3d(df, INIT_CAMERA_PARAMS[FOCAL_LENGTH_X],
                                           INIT_CAMERA_PARAMS[FOCAL_LENGTH_Y], image_width, image_height)
            # df = df[['X_3D', 'Y_3D', 'Z']]
            # input_data = df.to_numpy()
            df.to_csv('data/d13_route_40001001011/oneformer/output/route_batch_3d/road_boundary_project_info.csv', index=False)
            df_lidar = None

    xy = input_data[:, 0:2]
    z = input_data[:, 2]
    xy_augmented = np.hstack((xy, np.ones((xy.shape[0], 1))))
    coefficients, _, _, _ = np.linalg.lstsq(xy_augmented, z,
                                            rcond=None)
    a, b, d = coefficients
    print(a, b, d)
    c = -1
    # plane_params, best_fit_pts = fit_plane_lmeds(input_data)
    # a, b, c, d = plane_params
    # print(a, b, c, d)
    # print(len(best_fit_pts))

    # plot raw data
    plt.figure()
    ax = plt.subplot(111, projection='3d')
    if use_test_data:
        ax.scatter(input_data[:, 0], input_data[:, 1], input_data[:, 2], color='b')
    else:
        if df_lidar is not None:
            # ax.scatter(df['X'], df['Y'], df['Z'], color='b')
            # ax.scatter(df['X_3D'], df['Y_3D'], df['Z'], color='b')
            ax.scatter(df_lidar['X_3D'], df_lidar['Y_3D'], df_lidar['Z'], color='r')
        else:
            # draw fit plane for each 10 road pixel
            # df_filtered = df.iloc[::1000]
            # ax.scatter(df_filtered['X_3D'], df_filtered['Y_3D'], df_filtered['Z'], color='b')
            ax.scatter(df['X_3D'], df['Y_3D'], df['Z'], color='b')

    # plot plane
    x_lim = ax.get_xlim()
    y_lim = ax.get_ylim()
    x, y = np.meshgrid(np.arange(x_lim[0], x_lim[1]),
                       np.arange(y_lim[0], y_lim[1]))
    z = np.zeros(x.shape)
    for row in range(x.shape[0]):
        for col in range(x.shape[1]):
            z[row, col] = (-a * x[row, col] - b * y[row, col] - d) / c
    # ax.plot_wireframe(x, y, z, rstride=10, cstride=10, color='k')
    ax.plot_wireframe(x, y, z, color='k')
    ax.set_xlabel('x')
    ax.set_ylabel('y')
    ax.set_zlabel('z')
    plt.show()
