import argparse
import numpy as np
from PIL import Image


def join_images(left_image_path, front_image_path, right_image_path):
    """
    join input left, front, and right images into a single image
    """
    from PIL import Image
    img_names = [left_image_path, front_image_path, right_image_path]
    imgs = []
    try:
        for idx in range(3):
            imgs.append(Image.open(img_names[idx]))

        dest_img = Image.new('RGB', (imgs[0].width+imgs[1].width+imgs[2].width, imgs[0].height))

        dest_img.paste(imgs[0], (0, 0))
        dest_img.paste(imgs[1], (imgs[0].width, 0))
        dest_img.paste(imgs[2], (imgs[0].width+imgs[1].width, 0))
        return dest_img, imgs[0].width, imgs[0].height
    except OSError as ex:
        print(left_image_path, str(ex))
        return None, -1, -1


parser = argparse.ArgumentParser(description='Process arguments.')
parser.add_argument('--input_file_base', type=str,
                    default='../images/input/92600542024',
                    # default='../images/input/92600542105',
                    help='input file base name with path to create joined left+center+right image')
parser.add_argument('--output_file_base', type=str,
                    default='../images/output/grayscale_92600542024',
                    # default='../images/output/grayscale_92600542105',
                    # default='../images/output/hist_eq_92600542024',
                    # default='../images/output/hist_eq_92600542105',
                    help='output file base name with path for the histogram equalized image')


args = parser.parse_args()
input_file_base = args.input_file_base
output_file_base = args.output_file_base
do_hist_eq = False
if output_file_base.startswith('hist_eq_'):
   do_hist_eq = True
input_image_left = f'{input_file_base}5.jpg'
input_image_center = f'{input_file_base}1.jpg'
input_image_right = f'{input_file_base}2.jpg'
input_image, width, height = join_images(input_image_left, input_image_center, input_image_right)
# Perform histogram equalization
# reference: https://levelup.gitconnected.com/introduction-to-histogram-equalization-for-digital-image-enhancement-420696db9e43
# convert to grayscale
imgray = input_image.convert(mode='L')
#convert to NumPy array
img_array = np.asarray(imgray)
if do_hist_eq:
    #flatten image array and calculate histogram via binning
    histogram_array = np.bincount(img_array.flatten(), minlength=256)
    #normalize
    num_pixels = np.sum(histogram_array)
    histogram_array = histogram_array/num_pixels
    #normalized cumulative histogram
    chistogram_array = np.cumsum(histogram_array)
    # Pixel mapping lookup table
    transform_map = np.floor(255 * chistogram_array).astype(np.uint8)
    # transform
    img_list = list(img_array.flatten())
    processed_img_list = [transform_map[p] for p in img_list]
    # reshape and write back into img_array
    processed_img_array = np.reshape(np.asarray(processed_img_list), img_array.shape)
else:
    # write grayscale images out without doing histogram equalization
    processed_img_array = img_array
#convert NumPy array to pillow Image and write to file
processed_img = Image.fromarray(processed_img_array, mode='L')
processed_img.save(f'{output_file_base}.jpg')
processed_image_left = processed_img.crop((0, 0, width, height))
processed_image_left.save(f'{output_file_base}5.jpg')
processed_image_center = processed_img.crop((width, 0, width*2, height))
processed_image_center.save(f'{output_file_base}1.jpg')
processed_image_right = processed_img.crop((width*2, 0, width*3, height))
processed_image_right.save(f'{output_file_base}2.jpg')
