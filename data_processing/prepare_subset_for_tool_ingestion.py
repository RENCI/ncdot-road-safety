import pandas as pd
import argparse
import os


parser = argparse.ArgumentParser(description='Process arguments.')
parser.add_argument('--input_map_file', type=str,
                    default='../server/metadata/data-mapping/secondary_road/mapped_2lane_sr_images_d4.csv',
                    help='input file with path for mapped images to create prepared subset from')
parser.add_argument('--input_pred_file', type=str,
                    default='../server/metadata/model-related/secondary_road/model_2lane_predict_d4.csv',
                    help='input file with path for model prediction to create prepared subset from')
parser.add_argument('--input_subset_file', type=str,
                    default='../server/metadata/model-related/secondary_road/d4_subset_with_manual_inspection_300.csv',
                    help='subset input file to be used for extracting image subset')
parser.add_argument('--map_common_path_prefix', type=str,
                    default='/projects/ncdot/NC_2018_Secondary/images/d4/',
                    help='common path prefix in the input map file to be replaced for iRODS image registration')
parser.add_argument('--output_map_file', type=str,
                    default='../server/metadata/data-mapping/secondary_road/mapped_2lane_sr_images_d4_subset_300.csv',
                    help='output file for the subset mapped secondary road images')
parser.add_argument('--output_pred_file', type=str,
                    default='../server/metadata/model-related/secondary_road/model_2lane_predict_d4_subset_300.csv',
                    help='output file for the subset model prediction secondary road images')

parser.add_argument('--output_irods_reg_path_prefix', type=str,
                    default='/projects/ncdot/NC_2018_Secondary/d04/',
                    help='output image registration path prefix to be registered in iRODS')

parser.add_argument('--output_irods_reg_file', type=str,
                    default='../server/metadata/irods/images_to_be_registered_300x3.csv',
                    help='output file for images to be registered in iRODS')

args = parser.parse_args()
input_map_file = args.input_map_file
input_pred_file = args.input_pred_file
input_subset_file = args.input_subset_file
output_map_file = args.output_map_file
output_pred_file = args.output_pred_file
map_common_path_prefix = args.map_common_path_prefix
output_irods_reg_file = args.output_irods_reg_file
output_irods_reg_path_prefix = args.output_irods_reg_path_prefix

input_map_df = pd.read_csv(input_map_file, header=0, index_col=False, dtype=str)
input_pred_df = pd.read_csv(input_pred_file, header=0, index_col=False, dtype=str, usecols=["MAPPED_IMAGE",
                                                                                            "ROUND_PREDICT"])
input_pred_df['MAPPED_IMAGE'] = input_pred_df['MAPPED_IMAGE'].str.replace('.jpg', '')
input_pred_df['MAPPED_IMAGE'] = input_pred_df['MAPPED_IMAGE'].str.split('/').str[-1]

input_subset_df = pd.read_csv(input_subset_file, header=0, index_col=False, dtype=str, usecols=['MAPPED_IMAGE'])
subset_list = list(input_subset_df['MAPPED_IMAGE'])
input_map_df = input_map_df[input_map_df["MAPPED_IMAGE"].isin(subset_list)]
input_pred_df = input_pred_df[input_pred_df["MAPPED_IMAGE"].isin(subset_list)]

input_map_df.to_csv(output_map_file, index=False)
input_pred_df.to_csv(output_pred_file, index=False)

images_to_be_registered_list = []


def append_to_register_image_list(mapped_image_str, path_str):
    images_to_be_registered_list.append(os.path.join(output_irods_reg_path_prefix,
                                                     path_str, f'{mapped_image_str}5.jpg'))
    images_to_be_registered_list.append(os.path.join(output_irods_reg_path_prefix,
                                                     path_str, f'{mapped_image_str}1.jpg'))
    images_to_be_registered_list.append(os.path.join(output_irods_reg_path_prefix,
                                                     path_str, f'{mapped_image_str}2.jpg'))


input_map_df.drop(columns=['ROUTEID', 'LATITUDE', 'LONGITUDE', 'MILE_POST'], inplace=True)
input_map_df.PATH = input_map_df.PATH.str.replace(map_common_path_prefix, '')

input_map_df.apply(lambda row: append_to_register_image_list(row['MAPPED_IMAGE'], row['PATH']), axis=1)
with open(output_irods_reg_file, 'w') as out_fp:
    out_fp.writelines(f'{item}\n' for item in images_to_be_registered_list)
print('Done')
