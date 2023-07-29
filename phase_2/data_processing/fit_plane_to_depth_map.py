import argparse
import numpy as np
from scipy.linalg import svd
import pandas as pd


def fit_plane_lmeds(points, num_iterations=1000, inlier_threshold=0.1):
    best_inliers = []
    for _ in range(num_iterations):
        # Step 1: Randomly select 3 points to form a candidate plane
        idx = np.random.choice(len(points), 3, replace=False)
        candidate_plane_points = points[idx]

        # Step 2: Fit a plane to the candidate points using SVD
        A = np.vstack([candidate_plane_points[:, 0], candidate_plane_points[:, 1],
                       candidate_plane_points[:, 2]]).T
        _, _, v = svd(A)
        plane_normal = v[-1, :]
        plane_normal /= np.linalg.norm(plane_normal)

        # Step 3: Calculate the distance from each point to the plane
        distances = np.abs(np.dot(points - candidate_plane_points[0], plane_normal))
        # Step 4: Count inliers (points whose distance to the plane is within the inlier threshold)
        inliers = points[distances < inlier_threshold]

        # Step 5: Keep the plane with the most inliers
        if len(inliers) > len(best_inliers):
            best_inliers = inliers

    # Step 6: Refit the plane using all inliers
    A = np.vstack([best_inliers[:, 0], best_inliers[:, 1], best_inliers[:, 2]]).T
    _, _, v = svd(A)
    best_plane_params = v[-1, :]
    best_plane_params /= np.linalg.norm(best_plane_params)

    return best_plane_params, best_inliers


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Process arguments.')
    parser.add_argument('--input_depth_map', type=str,
                        default='data/d13_route_40001001011/oneformer/output/route_batch_3d/'
                                'road_alignment_with_lidar_926005420241.csv',
                        help='input file that contains reverse-projected segmented road boundary x, y, z vertices '
                             'with z as the predicted depth')
    parser.add_argument('--output_plane_param_file', type=str,
                        default='data/d13_route_40001001011/oneformer/output/route_batch_3d/'
                                'fit_depth_plane_pts_926005420241.csv',
                        help='output file for fit plane parameters of the input 3D depth map')

    args = parser.parse_args()
    input_depth_map = args.input_depth_map
    output_plane_param_file = args.output_plane_param_file
    df = pd.read_csv(input_depth_map, usecols=['X_3D', 'Y_3D', 'Z'])
    df = df[['X_3D', 'Y_3D', 'Z']]
    input_data = df.to_numpy()

    # Fit the plane using LMedS
    plane_params, best_fit_pts = fit_plane_lmeds(input_data)
    print("Fitted Plane Normal:", plane_params)
    print("best_fit_pts length:", len(best_fit_pts))
    np.savetxt(output_plane_param_file, best_fit_pts, fmt='%.3f',  header='X, Y, Z', comments='')
