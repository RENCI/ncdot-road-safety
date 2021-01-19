from django.core.management.base import BaseCommand
import pandas as pd
from rs_core.utils import save_annot_data_to_db


class Command(BaseCommand):
    """
    This script load user annotated data from csv file into database
    To run this command, do:
    docker exec -ti dot-server python manage.py load_user_annot_data <input_csv_file_with_path>
    For example:
    docker exec -ti dot-server python manage.py load_user_annot_data
    metadata/model-related/secondary_road/d4_subset_with_manual_inspection_300.csv hongyi guardrail
    """
    help = "Process the user annotation file in csv format to load into database"

    def add_arguments(self, parser):
        # csv filename with full path to load metadata from
        parser.add_argument('input_file', help='input csv file name with full path to be '
                                               'processed and load user annotation from')
        parser.add_argument('user_name', help='username of the user whose annotation needs to be saved')
        parser.add_argument('annot_name', help='annotation name for which annotation needs to be saved')


    def handle(self, *args, **options):
        input_file = options['input_file']
        user_name = options['user_name']
        annot_name = options['annot_name']
        df = pd.read_csv(input_file, header=0, index_col=False, dtype=str, usecols=["MAPPED_IMAGE",
                                                                                    "MANUAL_YN"])
        df.apply(lambda row: save_annot_data_to_db(row['MAPPED_IMAGE'], user_name, annot_name,
                                                   True if row['MANUAL_YN'] == 'Y' else False), axis=1)
        print('Done')
