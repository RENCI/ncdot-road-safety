import pandas as pd
from utils import get_image_path


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
