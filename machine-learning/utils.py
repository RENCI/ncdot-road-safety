import os
import pandas as pd
import tensorflow as tf


def setup_gpu_memory(mem_limit=1024*30):
    # this code works with the latest tensorflow version 2.10
    # default memory limit is set to be 30GB, but can be configurable by passing in a different parameter
    try:
        gpus = tf.config.list_physical_devices('GPU')
        for gpu in gpus:
            tf.config.experimental.set_memory_growth(gpu, True)
            tf.config.set_logical_device_configuration(
                gpu,
                [tf.config.LogicalDeviceConfiguration(memory_limit=mem_limit)])
        logical_gpus = tf.config.list_logical_devices('GPU')
        print(len(gpus), "Physical GPUs,", len(logical_gpus), "Logical GPUs")
    except RuntimeError as e:
        print(e)


def setup_gpu_memory_old(mem_limit=1024*30):
    # this code works with old tensorflow version up to version 2.3, but does not work with the
    # latest tensorflow version 2.10
    # there are 2 GPUs with 32GB mem each on groucho. Need to set memory limit to 30G
    # for each to avoid running exceptions
    try:
        tf.config.experimental.set_memory_growth = True
        gpus = tf.config.experimental.list_physical_devices('GPU')
        for gpu in gpus:
            # Virtual devices must be set before GPUs have been initialized
            tf.config.experimental.set_virtual_device_configuration(
                gpu,
                [tf.config.experimental.VirtualDeviceConfiguration(memory_limit=mem_limit)])

        logical_gpus = tf.config.experimental.list_logical_devices('GPU')
        print(len(gpus), "Physical GPU,", len(logical_gpus), "Logical GPUs")
    except RuntimeError as e:
        print(e)


def get_image_names_with_path(data_dir, mapped_image):
    """
    get image path from the mapped image base name
    :param data_dir: the root data directory that contains the image
    :param mapped_image: the mapped image base name
    :return: image_path, left image name, front image name, right image name
    """
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
        return dest_img
    except OSError as ex:
        print(left_image_path, str(ex))
        return None


def split_to_train_valid_test(data_df, label_column, train_frac):
    """
    Split data randomly into train data by the specified training fraction, and
    split the rest of data equally and randomly into validation and test data
    :param data_df: input data dataframe
    :param label_column: the column in the input data_df that is used for training labels
    :param train_frac: the fraction of training data to split into from the input dataframe
    :return: split training dataframe, validation dataframe, test dataframe
    """
    labels = data_df[label_column].unique()
    split_train_df, split_valid_df, split_test_df = pd.DataFrame(), pd.DataFrame(), pd.DataFrame()
    for lbl in labels:
        lbl_df = data_df[data_df[label_column] == lbl]
        lbl_train_df = lbl_df.sample(frac=train_frac, random_state=1)
        lbl_valid_test_df = lbl_df.drop(lbl_train_df.index)
        # further split remaining data into two equal sets for validation and test
        lbl_valid_df = lbl_valid_test_df.sample(frac=0.5, random_state=1)
        lbl_test_df = lbl_valid_test_df.drop(lbl_valid_df.index)
        print(lbl, "total:", len(lbl_df), "train_df:", len(lbl_train_df), "valid_df", len(lbl_valid_df),
              "test_df:", len(lbl_test_df))
        split_train_df = split_train_df.append(lbl_train_df)
        split_valid_df = split_valid_df.append(lbl_valid_df)
        split_test_df = split_test_df.append(lbl_test_df)

    return split_train_df, split_valid_df, split_test_df


def split_to_train_valid_for_al(data_df, label_column, train_frac):
    """
    Split data randomly into train data by the specified training fraction, and leave the rest as validation data.
    For Active Learning, the collected user annotated dataset is not balanced. Since we have an annotated balanced
    holdout test set for model performance assessment across rounds, we only need to split data into train and
    validation sets.
    :param data_df: input data dataframe
    :param label_column: the column in the input data_df that is used for training labels
    :param train_frac: the fraction of training data to split into from the input dataframe
    :return: split training dataframe, validation dataframe
    """
    labels = data_df[label_column].unique()
    split_train_df, split_valid_df = pd.DataFrame(), pd.DataFrame()
    for lbl in labels:
        lbl_df = data_df[data_df[label_column] == lbl]
        lbl_train_df = lbl_df.sample(frac=train_frac, random_state=42)
        lbl_valid_df = lbl_df.drop(lbl_train_df.index)
        print(lbl, "total:", len(lbl_df), "train_df:", len(lbl_train_df), "valid_df", len(lbl_valid_df))
        split_train_df = split_train_df.append(lbl_train_df)
        split_valid_df = split_valid_df.append(lbl_valid_df)

    return split_train_df, split_valid_df


def create_yes_no_sub_dirs(root_path):
    os.makedirs(os.path.join(root_path, 'yes'), exist_ok=True)
    os.makedirs(os.path.join(root_path, 'no'), exist_ok=True)


def sym_link_single_view_image(src, dst, left, front, right, presence, irelevant_as_false=True, prepare_opposite=True):
    try:
        dst_path, dst_ext = os.path.splitext(dst)
        if src.endswith('.jpg'):
            src_path, src_ext = os.path.splitext(src)
        else:
            src_path = os.path.join(src, dst_path.split('/')[-1])
            src_ext = '.jpg'
        if presence == 'True':
            opposite_dst_path = dst_path.replace('/yes/', '/no/')
            if left == 'p' or (not irelevant_as_false and left == 'i'):
                os.symlink(f'{src_path}5{src_ext}', f'{dst_path}5{dst_ext}')
            elif prepare_opposite:
                os.makedirs(opposite_dst_path, exist_ok=True)
                os.symlink(f'{src_path}5{src_ext}', f'{opposite_dst_path}5{dst_ext}')
            if front == 'p' or (not irelevant_as_false and front == 'i'):
                os.symlink(f'{src_path}1{src_ext}', f'{dst_path}1{dst_ext}')
            elif prepare_opposite:
                os.makedirs(opposite_dst_path, exist_ok=True)
                os.symlink(f'{src_path}1{src_ext}', f'{opposite_dst_path}1{dst_ext}')
            if right == 'p' or (not irelevant_as_false and right == 'i'):
                os.symlink(f'{src_path}2{src_ext}', f'{dst_path}2{dst_ext}')
            elif prepare_opposite:
                os.makedirs(opposite_dst_path, exist_ok=True)
                os.symlink(f'{src_path}2{src_ext}', f'{opposite_dst_path}2{dst_ext}')
        else:
            opposite_dst_path = dst_path.replace('/no/', '/yes/')
            if left == 'a' or (irelevant_as_false and left == 'i'):
                os.symlink(f'{src_path}5{src_ext}', f'{dst_path}5{dst_ext}')
            elif prepare_opposite:
                os.makedirs(opposite_dst_path, exist_ok=True)
                os.symlink(f'{src_path}5{src_ext}', f'{opposite_dst_path}5{dst_ext}')
            if front == 'a' or (irelevant_as_false and front == 'i'):
                os.symlink(f'{src_path}1{src_ext}', f'{dst_path}1{dst_ext}')
            elif prepare_opposite:
                os.makedirs(opposite_dst_path, exist_ok=True)
                os.symlink(f'{src_path}1{src_ext}', f'{opposite_dst_path}1{dst_ext}')
            if right == 'a' or (irelevant_as_false and right == 'i'):
                os.symlink(f'{src_path}2{src_ext}', f'{dst_path}2{dst_ext}')
            elif prepare_opposite:
                os.makedirs(opposite_dst_path, exist_ok=True)
                os.symlink(f'{src_path}2{src_ext}', f'{opposite_dst_path}2{dst_ext}')
    except FileExistsError as ex:
        print(irelevant_as_false, prepare_opposite, ex)
    return


def sym_link_single_image(src, dst):
    dst_path = os.path.dirname(dst)
    os.makedirs(dst_path, exist_ok=True)

    src_path = os.path.dirname(src)
    base_name = os.path.basename(src)
    base_name_strs = base_name.split('.')
    base_name = base_name_strs[0]
    ext_name = base_name_strs[1]
    single_names = (f'{base_name}5.{ext_name}',
                    f'{base_name}1.{ext_name}',
                    f'{base_name}2.{ext_name}'
                    )
    for name in single_names:
        os.symlink(os.path.join(src_path, name), os.path.join(dst_path, name))
    return


def _create_single_image_data(base_image_name, left_view, front_view, right_view, single_data_list, full_path=None,
                              remove_i=False):
    if full_path:
        base_path, ext = os.path.splitext(full_path)
        base_path_img, ext_img = os.path.splitext(base_image_name)
        if not(remove_i and left_view == 'i'):
            single_data_list.append([f'{base_path_img}5{ext_img}', 'True' if left_view == 'p' else 'False',
                                     f'{base_path}5{ext}'])
        if not (remove_i and front_view == 'i'):
            single_data_list.append([f'{base_path_img}1{ext_img}', 'True' if front_view == 'p' else 'False',
                                     f'{base_path}1{ext}'])
        if not (remove_i and right_view == 'i'):
            single_data_list.append([f'{base_path_img}2{ext_img}', 'True' if right_view == 'p' else 'False',
                                     f'{base_path}2{ext}'])
    else:
        if not (remove_i and left_view == 'i'):
            single_data_list.append([f'{base_image_name}5', 'True' if left_view == 'p' else 'False'])
        if not (remove_i and front_view == 'i'):
            single_data_list.append([f'{base_image_name}1', 'True' if front_view == 'p' else 'False'])
        if not (remove_i and right_view == 'i'):
            single_data_list.append([f'{base_image_name}2', 'True' if right_view == 'p' else 'False'])
    return


def create_single_data_frame(joined_df, full_path=False, remove_i=False):
    single_image_data_list = []
    if full_path is True:
        joined_df.apply(lambda row: _create_single_image_data(row.name, row.LeftView, row.FrontView,
                                                              row.RightView, single_image_data_list,
                                                              row.Full_Path_Image, remove_i=remove_i),
                        axis=1)
        return pd.DataFrame(single_image_data_list, columns=['Image', 'Presence', 'Full_Path_Image'])
    else:
        joined_df.apply(lambda row: _create_single_image_data(row.name, row.LeftView, row.FrontView,
                                                              row.RightView, single_image_data_list, remove_i=remove_i),
                        axis=1)
        return pd.DataFrame(single_image_data_list, columns=['Image', 'Presence'])


def draw_plots(y_true, y_predict):
    from sklearn.metrics import precision_recall_curve
    from sklearn.metrics import roc_curve
    import matplotlib.pyplot as plt

    precision, recall, threshold = precision_recall_curve(y_true, y_predict)
    plt.plot(threshold, precision[:-1], "b--", label='Precision')
    plt.plot(threshold, recall[:-1], "g--", label='Recall')
    plt.grid(True)
    plt.show()

    fpr, tpr, threshold = roc_curve(y_true, y_predict)
    plt.plot(fpr, tpr, linewidth=2)
    plt.plot([0, 1], [0, 1], 'k--')
    plt.grid(True)
    plt.show()
    return
