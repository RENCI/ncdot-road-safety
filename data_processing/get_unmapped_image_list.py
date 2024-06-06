# This script checks videolog images in a division against the mapped image dataframe and output the list of images
# that are not already in the mapped image dataframe for further mapping later.
# Command to run the script: python get_unmapped_image_list.py
import argparse
import pandas as pd


parser = argparse.ArgumentParser(description='Process arguments.')
parser.add_argument('--mapping_input_file', type=str,
                    default='/projects/ncdot/secondary_road/output/d13/mapped_2lane_sr_images_d13_all.csv',
                    help='input file with mapped images')
parser.add_argument('--seg_path_input_file', type=str,
                    default='/projects/ncdot/NC_2018_Secondary_2/depth_prediction/'
                            'd13_segmentation_path_mapping_updated.csv',
                    help='segmentation path input file that contains all videolog images in a division')
parser.add_argument('--output_file', type=str,
                    default='/projects/ncdot/secondary_road/output/d13/images_to_be_further_mapped.csv',
                    help='output file that includes images to be further mapped')

args = parser.parse_args()
mapping_input_file = args.mapping_input_file
seg_path_input_file = args.seg_path_input_file
output_file = args.output_file


df_map = pd.read_csv(mapping_input_file, header=0, dtype={'MAPPED_IMAGE': int}, usecols=['MAPPED_IMAGE'])
df_seg = pd.read_csv(seg_path_input_file, header=0, dtype=str, usecols=['IMAGE_PATH'])
df_seg['IMAGE_BASE_NAME'] = df_seg['IMAGE_PATH'].str.split('/').str[-1].str[:11]
df_seg.IMAGE_BASE_NAME = df_seg.IMAGE_BASE_NAME.astype(int)
df = pd.merge(df_seg, df_map[['MAPPED_IMAGE']], how='outer', left_on='IMAGE_BASE_NAME', right_on='MAPPED_IMAGE',
              indicator=True)
df_to_be_mapped = df[df['_merge'] == 'left_only']
df_to_be_mapped = df_to_be_mapped.drop(columns=['_merge', 'MAPPED_IMAGE', 'IMAGE_PATH'])
df_to_be_mapped = df_to_be_mapped.drop_duplicates()
df_to_be_mapped.to_csv(output_file, index=False)
print('DONE')
