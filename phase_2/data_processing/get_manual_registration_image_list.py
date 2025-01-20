import argparse
import pandas as pd
from utils import get_image_resolution


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Process arguments.')
    parser.add_argument('--input_sensor_mapping_file_with_path', type=str,
                        default='/projects/ncdot/secondary_road/output/d13/mapped_2lane_images_d13.csv',
                        help='input csv file that includes mapped image lat/lon info')
    parser.add_argument('--output_file', type=str,
                        default='/projects/ncdot/NC_2018_Secondary_2/manual_registration/d13_initial_camera_params.csv',
                        help='output file name with path')

    args = parser.parse_args()
    input_sensor_mapping_file_with_path = args.input_sensor_mapping_file_with_path
    output_file = args.output_file

    map_df = pd.read_csv(input_sensor_mapping_file_with_path, usecols=['ROUTEID', 'MAPPED_IMAGE', 'PATH'], dtype=str)
    map_df['MAPPED_IMAGE'] = map_df['MAPPED_IMAGE'].str[:11]
    map_df.sort_values(by=['ROUTEID', 'MAPPED_IMAGE'], inplace=True, ignore_index=True)
    map_df['FRONT_IMAGE_NAME_WITH_PATH'] = map_df['PATH'] + '/' + map_df['MAPPED_IMAGE'] + '1.jpg'
    map_df['RESOLUTION'] = map_df['FRONT_IMAGE_NAME_WITH_PATH'].apply(get_image_resolution)
    # Drop duplicates based on the resolution
    unique_images_df = map_df.drop_duplicates(subset='RESOLUTION', keep='first')
    unique_images_df.rename(columns={'ROUTEID': 'routeID', 'MAPPED_IMAGE': 'imageBaseName'}, inplace=True)
    unique_images_df['vFOV'] = None
    unique_images_df['posX'] = None
    unique_images_df['posY'] = None
    unique_images_df['posZ'] = None
    unique_images_df['rotX'] = None
    unique_images_df['rotY'] = None
    unique_images_df['rotZ'] = None
    unique_images_df.to_csv(output_file, index=False)
    exit(0)
