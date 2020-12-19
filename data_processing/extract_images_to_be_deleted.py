import os
import pandas as pd


def get_image_path(image_name):
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
    return os.path.join(set_str, minute_str, image_name)


image_base_name_file = '../server/metadata/image_base_names.txt'
image_name_file = '../server/metadata/imageNamesWithExtension.txt'
output_file = '../server/metadata/image_to_be_deleted.txt'

image_base_name_df = pd.read_csv(image_base_name_file, header=0, dtype=str)
print(image_base_name_df.shape)
image_list = list(image_base_name_df['ImageBaseName'])

image_name_df = pd.read_csv(image_name_file, header=0, dtype=str)
print("image names before filtering with image base names", image_name_df.shape)
image_name_df = image_name_df[~image_name_df["ImageFileName"].str[:11].isin(image_list)]
print("image names after filtering with image base names", image_name_df.shape)
image_name_df["ImageFileName"] = image_name_df["ImageFileName"].apply(lambda name: get_image_path(name))
image_name_df.to_csv(output_file, index=False)
print('DONE')
