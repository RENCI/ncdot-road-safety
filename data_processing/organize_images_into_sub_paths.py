import os
import argparse
from utils import get_image_path


parser = argparse.ArgumentParser(description='Process arguments.')
parser.add_argument('--input_path', type=str,
                    default='/projects/ncdot/NC_2018_Secondary_2/depth_prediction/d13',
                    help='input path to move images into sub paths named by '
                         'sets/minutes/seconds/series accordingly')
args = parser.parse_args()
input_path = args.input_path
img_list = os.listdir(input_path)

for img in img_list:
    if img.endswith('.png'):
        img_path = get_image_path(img, prefix_path=input_path)
        img_dir_name = os.path.dirname(img_path)
        if img_dir_name:
            os.makedirs(img_dir_name, exist_ok=True)
            os.rename(os.path.join(input_path, img), img_path)
