from django.core.management.base import BaseCommand
import pandas as pd
from rs_core.utils import save_user_annot_summary_to_db


class Command(BaseCommand):
    """
    This script load user annotated data summary for a specified active learning round into database
    To run this command, do:
    docker exec -ti dot-server python manage.py load_user_annot_summary <input_csv_file_with_path>
    <annotation_name> <round_number>
    For example:
    docker exec -ti dot-server python manage.py load_user_annot_summary metadata/user_annots_1.txt guardrail 1
    """
    help = "Process the user annotation file in csv format to compute summary and load into database"

    def add_arguments(self, parser):
        # csv filename with full path to load metadata from
        parser.add_argument('input_file', help='input csv file name with full path to be '
                                               'processed and load user annotation from')
        parser.add_argument('annot_name', help='annotation name for which annotation needs to be saved')
        parser.add_argument('round_number', help='The AL round number for the user annotation to be loaded')


    def handle(self, *args, **options):
        input_file = options['input_file']
        annot_name = options['annot_name']
        round_no = options['round_number']
        df = pd.read_csv(input_file, header=0, index_col=False, dtype=str, usecols=["Image", "Username", "Presence"])
        df.drop_duplicates(subset=['Image'], keep='first', inplace=True)
        print(df.shape)
        df_group = df.groupby(['Username', 'Presence']).agg('count')
        df_group.apply(lambda row: save_user_annot_summary_to_db(row.name[0], row.name[1], annot_name, round_no,
                                                                 row.Image), axis=1)
        print('Done')
