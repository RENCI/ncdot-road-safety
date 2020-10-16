from django.core.management.base import BaseCommand
from django.conf import settings
import pandas as pd
from rs_core.utils import save_metadata_to_db


class Command(BaseCommand):
    """
    This script load metadata from exported csv file into database
    To run this command, do:
    docker exec -ti dot-server python manage.py load_metadata <input_file_with_path>
    For example:
    docker exec -ti dot-server python manage.py load_metadata metadata/sensor_data_mapped.csv
    """
    help = "Process input the metadata export file in csv format to process and load metadata into database"

    def add_arguments(self, parser):
        # csv filename with full path to load metadata from
        parser.add_argument('input_file', help='input csv file name with full path to be '
                                               'processed and load metadata from')

    def save_to_db(self):
        return

    def handle(self, *args, **options):
        input_file = options['input_file']
        if settings.DEBUG:
            # only loads the first 18240 rows into database for local development
            df = pd.read_csv(input_file, header=0, index_col=False,
                             nrows=18240,
                             usecols=["ROUTEID", "SET", "IMAGE", "LATITUDE", "LONGITUDE", "MAPPED_IMAGE"])
        else:
            df = pd.read_csv(input_file, header=0, index_col=False,
                             usecols=["ROUTEID", "SET", "IMAGE", "LATITUDE", "LONGITUDE", "MAPPED_IMAGE"])
        print('Before removing potential duplicates:', len(df))
        df.drop_duplicates(subset=['MAPPED_IMAGE'], keep='first', inplace=True)
        print('After removing potential duplicates:', len(df))
        df.apply(lambda row: save_metadata_to_db(row['ROUTEID'], row['SET'], row['MAPPED_IMAGE'], row['LATITUDE'],
                                                 row['LONGITUDE']), axis=1)
        print('Done')
