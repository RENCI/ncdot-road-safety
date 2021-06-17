import os
import numpy as np


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
