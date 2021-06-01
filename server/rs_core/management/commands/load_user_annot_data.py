from django.core.management.base import BaseCommand
import pandas as pd
from rs_core.utils import save_annot_data_to_db


class Command(BaseCommand):
    """
    This script load user annotated data from csv file into database
    To run this command, do:
    docker exec -ti dot-server python manage.py load_user_annot_data <input_csv_file_with_path> <annot_name>
    For example:
    docker exec -ti dot-server python manage.py load_user_annot_data
    metadata/all_user_annots.txt guardrail
    """
    help = "Process the user annotation file in csv format to load into database"

    def add_arguments(self, parser):
        # csv filename with full path to load metadata from
        parser.add_argument('input_file', help='input csv file name with full path to be '
                                               'processed and load user annotation from')
        parser.add_argument('annot_name', help='annotation name for which annotation needs to be saved')


    def handle(self, *args, **options):
        input_file = options['input_file']
        annot_name = options['annot_name']
        df = pd.read_csv(input_file, header=0, index_col=False, usecols=['Image', 'Username', 'LeftView',
                                                                         'FrontView', 'RightView'])
        df.Image = df.Image.str.split('/').str[-1].str.split('.')[0]
        df.apply(lambda row: save_annot_data_to_db(row['Image'], row['Username'], annot_name,
                                                   {'left': row['LeftView'],
                                                    'front': row['FrontView'],
                                                    'right': row['RightView']}), axis=1)

        print('Done')
