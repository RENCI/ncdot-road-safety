import os
import glob
import argparse
from p_tqdm import p_map
import numpy as np
from PIL import Image
from skimage.transform import resize
from detectron2.data.detection_utils import read_image


def get_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument("-d", "--directory", type=str, required=True, help="Directory of images")
    parser.add_argument("-o", "--output_path", type=str, required=True, help="Output path")
    parser.add_argument("-e", "--ext", type=str, default=".jpg", help="Image extension")
    parser.add_argument("-H", "--height", type=int, required=True, help="New image height")
    #parser.add_argument("-W", "--width", type=int, default=None, help="New image width")
    parser.add_argument("-a", "--anti_aliasing", action="store_true", help="Use antialiasing")

    return parser


def resize_image(image_file, args):
    #with Image.open(image_file) as i:
    #    image_array = np.array(i)

    height = args.height
    width = int(height * (2748 / 2198))

    image_array = read_image(image_file, format="RGB")
    resized = resize(image_array, (height, width), anti_aliasing=args.anti_aliasing)
    Image.fromarray((resized * 255).astype(np.uint8)).save(os.path.join(args.output_path, image_file.split("/")[-1]))


if __name__ == "__main__":
    args = get_parser().parse_args()

    if args.ext.startswith("."):
        args.ext = args.ext[1:]

    if not os.path.exists(args.output_path):
        os.makedirs(args.output_path)

    file_list = glob.glob(os.path.join(args.directory, f"*.{args.ext}"))
    for file in file_list:
        if file.split("/")[-1].replace(f".{args.ext}", "").endswith("6"):
            os.remove(file)
    file_list = glob.glob(os.path.join(args.directory, f"*.{args.ext}"))
    p_map(resize_image, file_list, [args] * len(file_list))
