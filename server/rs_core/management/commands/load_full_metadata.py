from django.core.management.base import BaseCommand
import pandas as pd
from rs_core.utils import save_metadata_to_db


class Command(BaseCommand):
    """
    This script load metadata from exported csv file into database
    To run this command, do:
    docker exec -ti dot-server python manage.py load_full_metadata <input_metadata_file_with_path>
    <input_predict_file_with_path>
    For example:
    docker exec -ti dot-server python manage.py load_full_metadata
    metadata/data-mapping/secondary_road/mapped_2lane_sr_images_d4.csv
    metadata/metadata/data-mapping/secondary_road/model_2lane_predict_d4.csv d4 d04
    """
    help = "Process the metadata file and model prediction file both in csv format to load into database"

    def add_arguments(self, parser):
        # csv filename with full path to load metadata from
        parser.add_argument('input_metadata_file', help='input csv file name with full path to be '
                                                        'processed and load metadata from')
        parser.add_argument('input_predict_file', help='input csv file name with full path to be '
                                                        'processed and load model prediction from')
        parser.add_argument('division_str', help='division string on the path, e.g., d4, d8, d13 or d14')
        parser.add_argument('replace_division_str', help='replace division string on the path, e.g., d04, d08, '
                                                         'd13 or d14')

    def handle(self, *args, **options):
        input_metadata_file = options['input_metadata_file']
        input_predict_file = options['input_predict_file']
        division_str = options['division_str']
        replace_division_str = options['replace_division_str']
        df_metadata = pd.read_csv(input_metadata_file, header=0, index_col=False, dtype=str, usecols=["ROUTEID",
                                                                                                      "MAPPED_IMAGE",
                                                                                                      "LATITUDE",
                                                                                                      "LONGITUDE",
                                                                                                      "MILE_POST",
                                                                                                      "PATH"])
        if division_str != replace_division_str:
            df_metadata.PATH = df_metadata.PATH.str.replace(
                '/projects/ncdot/NC_2018_Secondary/images/{}'.format(division_str), replace_division_str)
        else:
            df_metadata.PATH = df_metadata.PATH.str.replace('/projects/ncdot/NC_2018_Secondary/images/', '')

        print(len(df_metadata))

        df_predict = pd.read_csv(input_predict_file, header=0, index_col=False, dtype={"MAPPED_IMAGE": str,
                                                                                       "ROUND_PREDICT": float},
                                 usecols=["MAPPED_IMAGE", "ROUND_PREDICT"])
        df_predict['MAPPED_IMAGE'] = df_predict['MAPPED_IMAGE'].str.replace('.jpg', '')
        df_predict['MAPPED_IMAGE'] = df_predict['MAPPED_IMAGE'].str.split('/').str[-1]

        print(len(df_predict))
        df = pd.merge(df_metadata, df_predict, on='MAPPED_IMAGE')
        df.apply(lambda row: save_metadata_to_db(row['ROUTEID'], row['MAPPED_IMAGE'], row['LATITUDE'],
                                                 row['LONGITUDE'], milepost=row['MILE_POST'], path=row['PATH'],
                                                 predict=row["ROUND_PREDICT"]), axis=1)
        print('Done')
