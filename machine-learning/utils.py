import os
from PIL import Image
import tensorflow as tf


def setup_gpu_memory():
    # there are 2 GPUs with 32GB mem each on groucho. Need to set memory limit to 30G for each to avoid
    # running exceptions
    tf.config.experimental.set_memory_growth = True
    gpus = tf.config.experimental.list_physical_devices('GPU')
    if len(gpus) == 2:
      try:
        tf.config.experimental.set_virtual_device_configuration(
            gpus[0],
            [tf.config.experimental.VirtualDeviceConfiguration(memory_limit=1024*30)])
        tf.config.experimental.set_virtual_device_configuration(
            gpus[1],
            [tf.config.experimental.VirtualDeviceConfiguration(memory_limit=1024*30)])
        logical_gpus = tf.config.experimental.list_logical_devices('GPU')
        print(len(gpus), "Physical GPU,", len(logical_gpus), "Logical GPUs")
      except RuntimeError as e:
        # Virtual devices must be set before GPUs have been initialized
        print(e)


def get_image_names_with_path(data_dir, mapped_image):
    if len(mapped_image) != 11:
        print("mapped image in metadata must have a length of 11")
        return '', '', '', ''
    set_str = mapped_image[:3]
    hour = mapped_image[3:5]
    minute = mapped_image[5:7]
    if hour not in ['00', '01', '02']:
        print("hour in the mapped image must be 00 or 01 or 02", mapped_image)
        return '', '', '', ''
    if int(minute) > 59:
        print("minute in the mapped image must be less than 60")
        return '', '', '', ''
    if hour == '00':
        # strip prefix 0 from minute if any
        minute_str = str(int(minute))
    else:  # hour == '01'
        minute_str = str(int(minute) + int(hour)*60)
    path = os.path.join(data_dir, set_str, minute_str)
    left_image_name = '{}5.jpg'.format(mapped_image)
    front_image_name = '{}1.jpg'.format(mapped_image)
    right_image_name = '{}2.jpg'.format(mapped_image)
    return path, left_image_name, front_image_name, right_image_name


def join_images(left_image_path, front_image_path, right_image_path):
    if not os.path.exists(left_image_path) or not os.path.exists(front_image_path) or \
            not os.path.exists(right_image_path):
        print("at least one of the images", left_image_path, front_image_path, right_image_path, "do not exist")
        return None
    img_names = [left_image_path, front_image_path, right_image_path]
    imgs = []
    try:
        for idx in range(3):
            imgs.append(Image.open(img_names[idx]))

        dest_img = Image.new('RGB', (imgs[0].width+imgs[1].width+imgs[2].width, imgs[0].height))

        dest_img.paste(imgs[0], (0, 0))
        dest_img.paste(imgs[1], (imgs[0].width, 0))
        dest_img.paste(imgs[2], (imgs[0].width+imgs[1].width, 0))
        return dest_img
    except OSError as ex:
        print(left_image_path, str(ex))
        return None
