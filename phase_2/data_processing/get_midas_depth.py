import os
import argparse
import pandas as pd
from pypfm import PFMLoader
import matplotlib.pyplot as plt
from utils import load_pickle_data, IMAGE_WIDTH, IMAGE_HEIGHT, get_depth_data, get_depth_of_pixel


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
    parser.add_argument('--show_scatter_plot', action="store_false",
                        help='show scatter plot to see relationship between Y and Z')

    args = parser.parse_args()
    input_data_filename = args.input_data_filename
    output_file = args.output_file
    input_depth_image_filename = args.input_depth_image_filename
    show_scatter_plot = args.show_scatter_plot

    if not os.path.isfile(output_file):
        input_2d_points = load_pickle_data(input_data_filename)
        df = pd.DataFrame(input_2d_points, columns=["X", "Y"])
        loader = PFMLoader((IMAGE_WIDTH, IMAGE_HEIGHT), color=False, compress=False)
        input_pfm = get_depth_data(loader, input_depth_image_filename)
        min_depth = input_pfm.min()
        max_depth = input_pfm.max()
        df['Z'] = df.apply(lambda row: get_depth_of_pixel(row['Y'], row['X'], input_pfm, min_depth, max_depth), axis=1)
        df.to_csv(output_file, index=False, float_format='%.3f')
    elif show_scatter_plot:
        df = pd.read_csv(output_file, usecols=['Y', 'Z'])

    if show_scatter_plot:
        plt.scatter(df['Y'], df['Z'], s=20)
        plt.title('Scatter plot of Z vs Y for road edges in image 926005420241')
        plt.ylabel('Normalized depth Z')
        plt.xlabel('Y')
        plt.grid(True)
        # plt.legend(loc='lower left')
        plt.show()