import argparse
import pandas as pd
import os
from align_segmented_road_with_lidar import (get_left_right_side_df_and_values, compute_grid_minimum_distances,
                                             transform_3d_points)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Process arguments.')
    parser.add_argument('--obj_image_input', type=str,
                        default='/projects/ncdot/NC_2018_Secondary_2/'
                                'route_40001001012_input_corrected_updated_with_cam_paras.csv',
                        help='input csv file coming from align_segmented_road_with_lidar.py output that contains '
                             'image base names with optimized camera parameters')
    parser.add_argument('--input_init_cam_param_file_with_path', type=str,
                        default='/projects/ncdot/NC_2018_Secondary_2/route_40001001012_initial_camera_params.csv',
                        help='input csv file that includes initial camera parameters for manually registered images')
    parser.add_argument('--lidar_proj_file_path', type=str,
                        default='/projects/ncdot/NC_2018_Secondary_2/route_40001001012_geotagging_output',
                        help='path where projected LIDAR data is stored')
    parser.add_argument('--img_width', type=int, default=2356)
    parser.add_argument('--img_height', type=int, default=1200)
    parser.add_argument('--output_lidar_proj_file_path', type=str,
                        default='/projects/ncdot/NC_2018_Secondary_2/route_40001001012_geotagging_output_updated',
                        help='path where updated projected LIDAR data will be saved')

    args = parser.parse_args()
    obj_image_input = args.obj_image_input
    input_init_cam_param_file_with_path = args.input_init_cam_param_file_with_path
    lidar_proj_file_path = args.lidar_proj_file_path
    img_width = args.img_width
    img_height = args.img_height
    output_lidar_proj_file_path = args.output_lidar_proj_file_path

    init_cam_param_df = pd.read_csv(input_init_cam_param_file_with_path,
                                    usecols=['vFOV', 'posX', 'posY', 'posZ', 'rotX', 'rotY', 'rotZ'], nrows=1,
                                    dtype=float)
    init_cam_param_df['OBJ_BASE_TRANS_LIST'] = init_cam_param_df.apply(
        lambda row: [0.1, row['vFOV'], -row['posX'], -row['posY'], -row['posZ'], -row['rotZ'], -row['rotY'],
                     -row['rotX']], axis=1)
    init_cam_list = init_cam_param_df['OBJ_BASE_TRANS_LIST'].iloc[0]
    input_images = pd.read_csv(obj_image_input, usecols=['imageBaseName', 'BASE_ALIGN_ERROR'])
    image_list = input_images.imageBaseName.tolist()
    align_error_list = input_images.BASE_ALIGN_ERROR.tolist()

    images_with_changed_alignment = []
    for image, base_align_error in zip(image_list[1:], align_error_list[1:]):
        filename_3d = os.path.join(lidar_proj_file_path, f'lidar_project_info_{image}.csv')
        if os.path.isfile(filename_3d):
            df_2d = pd.read_csv(os.path.join(lidar_proj_file_path, f'input_2d_{image}.csv'))
            df_3d_whole = pd.read_csv(filename_3d,
                                      usecols=['PROJ_SCREEN_X', 'PROJ_SCREEN_Y', 'BOUND', 'SIDE', 'C', 'OCCLUDED'])
            df_3d = df_3d_whole[(df_3d_whole.BOUND == 1) & (df_3d_whole.OCCLUDED == False)].reset_index(drop=True).copy()
            # split df_2d and df_3d based on SIDE
            df_2d_l, df_2d_r = get_left_right_side_df_and_values(df_2d)
            df_3d_l, df_3d_r = get_left_right_side_df_and_values(df_3d)

            # compute grid-based distances for both left and right sides
            x_3d_l = df_3d_l['PROJ_SCREEN_X'].values
            y_3d_l = df_3d_l['PROJ_SCREEN_Y'].values
            x_3d_r = df_3d_r['PROJ_SCREEN_X'].values
            y_3d_r = df_3d_r['PROJ_SCREEN_Y'].values
            dists_l = compute_grid_minimum_distances(x_3d_l, y_3d_l, df_2d_l['X'].values, df_2d_l['Y'].values,
                                             50, 50)
            dists_r = compute_grid_minimum_distances(x_3d_r, y_3d_r, df_2d_r['X'].values, df_2d_r['Y'].values,
                                                     50, 50)
            alignment_error = dists_l + dists_r
            if alignment_error < base_align_error:
                # use base alignment instead of optimized alignment
                input_3d_gdf = transform_3d_points(df_3d_whole, init_cam_list, img_width, img_height)
                input_3d_gdf.to_csv(os.path.join(output_lidar_proj_file_path, f'lidar_project_info_{image}.csv'),
                                    index=False)
                cam_output_columns = ['translation_x', 'translation_y', 'translation_z',
                                      'rotation_z', 'rotation_y', 'rotation_x']
                # output optimized camera parameter for the image
                cam_para_df = pd.DataFrame(data=[init_cam_list], columns=cam_output_columns)
                cam_para_df.to_csv(os.path.join(output_lidar_proj_file_path,
                                                f'lidar_project_info_{image}_cam_paras.csv'),
                                   index=False)
                images_with_changed_alignment.append(image)

    if len(images_with_changed_alignment) > 0:
        print(f'The following images have changed alignment: {images_with_changed_alignment}')

    exit(0)