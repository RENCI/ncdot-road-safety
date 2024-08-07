import os
import argparse
import pandas as pd
from pypfm import PFMLoader
import matplotlib.pyplot as plt
from data_processing.utils import load_pickle_data, get_depth_data, get_depth_of_pixel


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Process arguments.')
    parser.add_argument('--input_data_filename', type=str,
                        default='data/d13_route_40001001011/oneformer/output/input_2d.pkl',
                        help='input data points to get midas depth for')
    parser.add_argument('--input_depth_image_filename', type=str,
                        default='../midas/images/output/d13_route_40001001011/926005420241-dpt_beit_large_512.pfm')
    parser.add_argument('--output_file', type=str,
                        default='data/d13_route_40001001011/oneformer/output/input_2d_depth.csv',
                        help='output csv with midas depth prediction added')
    parser.add_argument('--input_depth_file_3d', type=str,
                        default='data/d13_route_40001001011/oneformer/output/route_batch_3d/'
                                'lidar_project_info_926005420241_depth.csv',
                        help='input file containing predicted depth for projected 3D LIDAR data')
    parser.add_argument('--depth_scaling_factor', type=int, default=189, help='depth scaling factor corresponding to '
                                                                              'the input_depth_file_3d input')
    parser.add_argument('--image_width', type=int, default=2748, help='image width for the depth image')
    parser.add_argument('--image_height', type=int, default=2198, help='image height for the depth image')
    parser.add_argument('--show_scatter_plot', action="store_true",
                        help='show scatter plot to see relationship between Y and Z')
    parser.add_argument('--show_3d_plot', action="store_true",
                        help='show 3D plot to see relationship between X, Y and Z')

    args = parser.parse_args()
    input_data_filename = args.input_data_filename
    output_file = args.output_file
    input_depth_image_filename = args.input_depth_image_filename
    input_depth_file_3d = args.input_depth_file_3d
    image_width = args.image_width
    image_height = args.image_height
    dsf = args.depth_scaling_factor
    show_scatter_plot = args.show_scatter_plot
    show_3d_plot = args.show_3d_plot

    if not os.path.isfile(output_file):
        input_2d_points = load_pickle_data(input_data_filename)
        df = pd.DataFrame(input_2d_points, columns=["X", "Y"])
        loader = PFMLoader((image_width, image_height), color=False, compress=False)
        input_pfm = get_depth_data(loader, input_depth_image_filename)
        min_depth = input_pfm.min()
        max_depth = input_pfm.max()
        df['Z'] = df.apply(lambda row: get_depth_of_pixel(row['Y'], row['X'], input_pfm, min_depth, max_depth), axis=1)
        df.to_csv(output_file, index=False, float_format='%.3f')
    elif show_scatter_plot:
        df = pd.read_csv(output_file, usecols=['X', 'Y', 'Z'])
        if input_depth_file_3d:
            df_3d = pd.read_csv(input_depth_file_3d)

    if show_scatter_plot:
        if show_3d_plot:
            fig = plt.figure(figsize=(10, 8))
            ax = fig.add_subplot(111, projection='3d')
            ax.scatter3D(df['X'], df['Y'], df['Z'])
            ax.scatter3D(df_3d['PROJ_SCREEN_X'], df_3d['PROJ_SCREEN_Y'], df_3d['Z'] / dsf)
            ax.set_xlabel('X')
            ax.set_ylabel('Y')
            ax.set_zlabel('Z')
            plt.title('Scatter plot of Z vs Y and X for segmented road edges (blue) and '
                      'projected LIDAR road edges (orange) in image 926005420241')
            ax.grid(True)
        else:
            plt.scatter(df['Y'], df['Z'], s=20)
            if input_depth_file_3d:
                plt.scatter(df_3d['PROJ_SCREEN_Y'], df_3d['Z'] / dsf, s=20)
                plt.title('Scatter plot of Z vs Y for segmented road edges (blue) and '
                          'projected LIDAR road edges (orange) in image 926005420241')
            else:
                plt.title('Scatter plot of Z vs Y for segmented road edges in image 926005420241')
            plt.ylabel('Normalized depth Z')
            plt.xlabel('Y')
            plt.grid(True)
        # plt.legend(loc='lower left')
        plt.show()
