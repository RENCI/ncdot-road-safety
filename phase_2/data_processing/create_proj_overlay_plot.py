import argparse
import matplotlib.pyplot as plt
import pandas as pd
from pypfm import PFMLoader
from utils import get_depth_data, get_depth_of_pixel, IMAGE_WIDTH, IMAGE_HEIGHT
from align_segmented_road_with_lidar import transform_2d_points_to_3d, INIT_CAMERA_PARAMS, \
    FOCAL_LENGTH_Y, FOCAL_LENGTH_X


def create_depth(input_pfm, input_df, x_header, y_header, dsf=1):
    min_depth = input_pfm.min()
    max_depth = input_pfm.max()
    input_df['Z'] = input_df.apply(lambda row: get_depth_of_pixel(row[y_header], row[x_header],
                                                                  input_pfm, min_depth, max_depth, scaling=dsf), axis=1)
    return input_df


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Process arguments.')
    parser.add_argument('--image_base_name', type=str, default='926005420241', help='image base name to use to replace '
                                                                        'input_depth_image_filename_pattern pattern')
    parser.add_argument('--depth_scaling_factor', type=int, default=189, help='depth scaling factor')
    parser.add_argument('--input_3d', type=str,
                        default='data/d13_route_40001001011/oneformer/output/route_batch_3d/'
                                'lidar_project_info_926005420241_depth.csv',
                        help='3d vertices')
    parser.add_argument('--input_2d', type=str,
                        default='data/d13_route_40001001011/oneformer/output/route_batch_3d/'
                                'road_alignment_with_lidar_926005420241.csv',
                        help='2d vertices projected to 3d')
    parser.add_argument('--input_depth_image_filename_pattern', type=str,
                        default='../midas/images/output/d13_route_40001001011/{image_base_name}-dpt_beit_large_512.pfm',
                        help='input depth image file name pattern with image_base_name to be replaced')
    parser.add_argument('--output_depth_data_file', type=str,
                        default='data/d13_route_40001001011/oneformer/output/route_batch_3d/'
                                'lidar_project_info_926005420241_depth.csv',
                        help='output depth data file name if depth data needs to be written out; otherwise, '
                             'leave it blank')
    parser.add_argument('--show_lidar_proj', action="store_true",
                        help='show lidar projection overlay or segmented road boundary pixel overlay')
    parser.add_argument('--show_3d_plot', action="store_true",
                        help='show 3D X-Y-Z plot or show 2D plot')

    args = parser.parse_args()
    image_base_name = args.image_base_name
    depth_scaling_factor = args.depth_scaling_factor
    input_3d = args.input_3d
    input_2d = args.input_2d
    input_depth_image_filename_pattern = args.input_depth_image_filename_pattern
    output_depth_data_file = args.output_depth_data_file
    show_lidar_proj = args.show_lidar_proj
    show_3d_plot = args.show_3d_plot

    df_2d = pd.read_csv(input_2d)
    df_3d = pd.read_csv(input_3d)
    if show_lidar_proj:
        loader = PFMLoader((IMAGE_WIDTH, IMAGE_HEIGHT), color=False, compress=False)
        pfm = get_depth_data(loader, input_depth_image_filename_pattern.format(image_base_name=image_base_name))
        df_3d = create_depth(pfm, df_3d, 'PROJ_SCREEN_X', 'PROJ_SCREEN_Y', dsf=depth_scaling_factor)
        df_3d = transform_2d_points_to_3d(df_3d, INIT_CAMERA_PARAMS[FOCAL_LENGTH_X], INIT_CAMERA_PARAMS[FOCAL_LENGTH_Y],
                                          IMAGE_WIDTH, IMAGE_HEIGHT, x_header='PROJ_SCREEN_X', y_header='PROJ_SCREEN_Y',
                                          z_header='Z')

        if output_depth_data_file:
            df_3d.to_csv(output_depth_data_file, index=False)

    fig = plt.figure(figsize=(10, 8))
    if show_3d_plot:
        ax = fig.add_subplot(111, projection='3d')
        if show_lidar_proj:
            ax.scatter3D(df_3d['WORLD_X'], df_3d['WORLD_Y'], df_3d['WORLD_Z'])
            ax.scatter3D(df_3d['X_3D'], df_3d['Y_3D'], df_3d['WORLD_Z'])
            # ax.scatter3D(df_3d['WORLD_X'], df_3d['WORLD_Y'], df_3d['Z'])
        else:
            # ax.scatter3D(df_3d['WORLD_X'], df_3d['WORLD_Y'], df_3d['WORLD_Z'])
            ax.scatter3D(df_3d['X_3D'], df_3d['Y_3D'], df_3d['Z'])
            ax.scatter3D(df_2d['X_3D'], df_2d['Y_3D'], df_2d['Z'])
        ax.set_xlabel('X')
        ax.set_ylabel('Y')
        ax.set_zlabel('Z')
    else:
        ax = fig.add_subplot(111)
        if show_lidar_proj:
            # ax.scatter(df_3d['PROJ_SCREEN_X'], df_3d['WORLD_Z'])
            ax.scatter(df_3d['Y_3D'], df_3d['WORLD_Z'])
            ax.set_xlabel('Y_3D')
            ax.set_ylabel('LIDAR Transformed Z')
        else:
            ax.scatter(df_2d['Y_3D'], df_2d['Z'])
            ax.scatter(df_3d['Y_3D'], df_3d['Z'])
            ax.set_xlabel('Y_3D')
            ax.set_ylabel('Z')
    ax.grid(True)
    plt.show()
