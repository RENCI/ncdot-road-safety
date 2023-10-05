import argparse
import pandas as pd


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Process arguments.')
    parser.add_argument('--input_file', type=str, default='data/pole_input.csv', help='input file name with path')
    parser.add_argument('--input_mapping_file', type=str,
                        default='data/route_40001001011_segment_object_mapping_input.csv',
                        help='input mapping file name with path')

    args = parser.parse_args()
    input_file = args.input_file
    input_mapping_file = args.input_mapping_file
    pole_input = pd.read_csv(input_file)
    pole_input = pole_input.drop(columns = ['bearing'])

    mapping_input = pd.read_csv(input_mapping_file)
    mapping_input = mapping_input.drop(columns = ['lat', 'lon', 'x', 'y'])

    mapping_input = mapping_input.rename(columns={'ImageBaseName': 'imageBaseName', 'Depth': 'depth'})

    updated_pole_input = pd.merge(pole_input, mapping_input, how='left', on=['imageBaseName', 'depth'])

    updated_pole_input = updated_pole_input[['imageBaseName', 'lat', 'lon', 'bearing', 'depth']]
    updated_pole_input.to_csv(input_file, index=False)
