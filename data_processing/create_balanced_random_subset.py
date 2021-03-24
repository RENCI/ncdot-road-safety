import pandas as pd
import argparse

from create_balanced_random_subset_html_for_inspection import create_html_file_for_inspection


parser = argparse.ArgumentParser(description='Process arguments.')
parser.add_argument('--input_file', type=str,
                    default='../server/metadata/model-related/secondary_road/round2/predict_d13_d14.csv',
                    help='input model prediction file with path for mapped images to create random subset from')
parser.add_argument('--subset_size', type=int, default=100, help='number of images in the subset')
parser.add_argument('--division', type=str, default='d04', help='division str on the path')
parser.add_argument('--output_irods_file', type=str,
                    default='../server/metadata/irods/images_to_be_registered_d13.csv',
                    help='output file for the images to be registered in iRODS')
parser.add_argument('--output_html_file', type=str, default='../server/templates/model_2lane_d13_d14_subset.html',
                    help='the output html file for looking at images')

args = parser.parse_args()
input_file = args.input_file
subset_size = args.subset_size
division = args.division
output_irods_file = args.output_irods_file
output_html_file = args.output_html_file


df = pd.read_csv(input_file, header=0, index_col=False, dtype={'MAPPED_IMAGE': 'str', 'ROUND_PREDICT': 'float'},
                 usecols=['MAPPED_IMAGE', 'ROUND_PREDICT'])
print(df.shape)
df['PATH'] = df['MAPPED_IMAGE'].str.slice(stop=-15)
df['MAPPED_IMAGE'] = df['MAPPED_IMAGE'].str.replace('.jpg', '')
df['MAPPED_IMAGE'] = df['MAPPED_IMAGE'].str.split('/').str[-1]

df_yes = df[df.ROUND_PREDICT >= 0.5]
df_no = df[df.ROUND_PREDICT < 0.5]
print(df_yes.shape, df_no.shape)
sample_size = (int)(subset_size / 2)
sub_df = pd.concat([df_yes.sample(n=sample_size, random_state=42),
                    df_no.sample(n=sample_size, random_state=42)])
print(sub_df.shape)
sub_df = sub_df.rename(columns={'ROUND_PREDICT': 'ROUND_PREDICT_2'})
create_html_file_for_inspection(sub_df, output_html_file, two_models=False, predict_only=True)

#prefix_str = f'/projects/ncdot/NC_2018_Secondary/images/{division}/'
#irods_df = prefix_str + sub_df['PATH'] + sub_df['MAPPED_IMAGE'] + '.jpg'
#irods_df.to_csv(output_irods_file, index=False)
print('Done')
