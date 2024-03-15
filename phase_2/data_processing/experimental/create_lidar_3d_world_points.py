import argparse
import pandas as pd
import pickle


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Process arguments.')
    parser.add_argument('--lidar_projection_info_filename', type=str,
                        default='data/d13_route_40001001011/oneformer/output/route_batch/'
                                'lidar_project_info_926005420241.csv',
                        help='input lidar projection info file name with path')
    parser.add_argument('--output_file', type=str,
                        default='data/d13_route_40001001011/oneformer/output/input_3d.pkl',
                        help='output pickle data for world x, y, z vertices extracted from lidar projection info input')

    args = parser.parse_args()
    lidar_projection_info_filename = args.lidar_projection_info_filename
    output_file = args.output_file

    project_df = pd.read_csv(lidar_projection_info_filename, usecols=['WORLD_X', 'WORLD_Y', 'WORLD_Z'])
    # rearrange dataframe columns before dumping to pickle output file
    df = project_df[['WORLD_X', 'WORLD_Y', 'WORLD_Z']]
    vertices = [df.to_numpy()]
    with open(output_file, 'wb') as f:
        pickle.dump(vertices, f)
