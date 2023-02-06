import os
import shutil
import argparse
import pandas as pd


def prepare_image(mapped_image, path, output_path):
    image_suffix_list = ('5.jpg', '1.jpg', '2.jpg')
    for suffix in image_suffix_list:
        shutil.copyfile(os.path.join(path, f'{mapped_image}{suffix}'),
                        os.path.join(output_path, f'{mapped_image}{suffix}'))



parser = argparse.ArgumentParser(description='Process arguments.')
parser.add_argument('--input_csv_file_with_path', type=str,
                    default='/projects/ncdot/test_route_segmentation/test_route_road_pole_labels.csv',
                    help='input csv file that includes input image path and name for MiDAS depth prediction')
parser.add_argument('--route_id', type=str,
                    default='40001001011',
                    help='route id to filter the input label with')
parser.add_argument('--output_file_path', type=str,
                    default='/projects/ncdot/geotagging/midas_input/d13_route_40001001011/oneformer',
                    help='output path to put input images to feed to the MiDAS model')


args = parser.parse_args()
input_csv_file_with_path = args.input_csv_file_with_path
route_id = args.route_id
output_file_path = args.output_file_path

df = pd.read_csv(input_csv_file_with_path, index_col=None, usecols=['ROUTEID', 'MAPPED_IMAGE', 'PATH'],
                 dtype=str)
if route_id:
    df = df[df.ROUTEID == route_id]
df.apply(lambda row: prepare_image(row['MAPPED_IMAGE'], row['PATH'], output_file_path), axis=1)
