import os
import numpy as np
import pandas as pd
from PIL import Image


SECOND_ROAD_PREFIX_PATH = '/projects/ncdot/NC_2018_Secondary/images'
div_path_dict = {
    'd4': 'd04',
    'd8': 'd08',
    'd13': 'd13',
    'd14': 'd14'
}


def get_image_path(image_name, prefix_path=None):
    set_str = image_name[:3]
    hour = image_name[3:5]
    minute = image_name[5:7]
    if hour not in ['00', '01', '02']:
        print(f"{image_name}: hour in the image base name must be 00 or 01 or 02")
        return image_name
    if int(minute) > 59:
        print(f"{image_name}: minute in the image base name must be less than 60")
        return image_name
    if hour == '00':
        # strip prefix 0 from minute if any
        minute_str = str(int(minute))
    else:  # hour == '01'
        minute_str = str(int(minute) + int(hour)*60)
    if prefix_path:
        ret_path = os.path.join(prefix_path, set_str, minute_str, image_name)
    else:
        ret_path = os.path.join(set_str, minute_str, image_name)
    return ret_path


def round_feature(df):
    out_series = df.map_partitions(lambda sdf: sdf.apply(lambda row: np.round(np.asarray(row.FEATURES), 3).tolist(),
                                                         axis=1),
                                   meta=('FEATURES', 'float')).compute(scheduler='processes')
    df = df.drop(columns=['FEATURES'])
    df = df.compute(scheduler='processes')
    df['FEATURES'] = out_series
    return df


def image_covered(ref_data, mile_post):
    if isinstance(ref_data, pd.Series):
        mp1 = min(ref_data['BeginMp1'], ref_data['EndMp1'])
        mp2 = max(ref_data['BeginMp1'], ref_data['EndMp1'])
        if mp1 <= mile_post <= mp2:
            return True
        else:
            return False
    else: # DataFrame
        intervals = list(zip(ref_data['BeginMp1'], ref_data['EndMp1']))
        for start, stop in intervals:
            if start <= mile_post <= stop or stop <= mile_post <= start:
                return True
        return False


def join_images(left_image_path, front_image_path, right_image_path):
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


def map_image(geo_df, base_image_name, file_list, root_dir, dir_name, output_dir, is_join_image=False):
    file_name = f'{base_image_name}1.jpg'
    file_name2 = f'{base_image_name}2.jpg'
    file_name5 = f'{base_image_name}5.jpg'
    if file_name2 not in file_list or file_name5 not in file_list:
        print(base_image_name, 'cannot be mapped', flush=True)
        return {}
    base_df = geo_df[geo_df['Start-Image'] == base_image_name]
    if base_df.empty:
        base_name_int = int(base_image_name)
        if base_image_name.endswith('01') or base_image_name.endswith('00'):
            base_name_next = str(base_name_int + 1)
        else:
            base_name_next = str(base_name_int - 1)
        base_df = geo_df[geo_df['Start-Image'] == base_name_next]
        if base_df.empty:
            # cannot be mapped
            print(base_image_name, 'cannot be mapped', flush=True)
            return {}

    # check if images already exist in target directory
    idx = dir_name.index(root_dir) + len(root_dir)
    rel_input_dir = dir_name[idx:]
    if rel_input_dir.startswith('/') or rel_input_dir.startswith('\\'):
        rel_input_dir = rel_input_dir[1:]
    target_dir = os.path.join(output_dir, rel_input_dir)
    if is_join_image:
        target = os.path.join(target_dir, f'{base_image_name}.jpg')
    else:
        target = os.path.join(target_dir, file_name)
        target_left = os.path.join(target_dir, file_name5)
        target_right = os.path.join(target_dir, file_name2)
    if os.path.isfile(target):
        return {'ROUTEID': base_df['RouteID'].values[0],
                'MAPPED_IMAGE': base_image_name,
                'LATITUDE': base_df['StaLatitude'].values[0],
                'LONGITUDE': base_df['StaLongitude'].values[0],
                'MILE_POST': base_df['Start-MP'].values[0],
                'PATH': target_dir}
    else:
        os.makedirs(target_dir, exist_ok=True)
        front = os.path.join(dir_name, file_name)
        left = os.path.join(dir_name, file_name5)
        right = os.path.join(dir_name, file_name2)
        if is_join_image:
            dst_img = join_images(left, front, right)
            if dst_img:
                dst_img.save(target)
        else:
            os.symlink(front, target)
            os.symlink(left, target_left)
            os.symlink(right, target_right)
        if (not is_join_image) or (is_join_image and dst_img):
            return {'ROUTEID': base_df['RouteID'].values[0],
                    'MAPPED_IMAGE': base_image_name,
                    'LATITUDE': base_df['StaLatitude'].values[0],
                    'LONGITUDE': base_df['StaLongitude'].values[0],
                    'MILE_POST': base_df['Start-MP'].values[0],
                    'PATH': target_dir}
        else:
            return {}


def find_closest_mapped_metadata(input_base_img_num, map_df, map_col='Start-Image'):
    map_img_array = map_df[map_col].to_numpy()
    differences = np.abs(map_img_array - input_base_img_num)
    closest_idx = np.argmin(differences)
    return closest_idx, map_img_array[closest_idx]
