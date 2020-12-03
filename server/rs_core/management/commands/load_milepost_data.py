from django.core.management.base import BaseCommand

import pandas as pd
from rs_core.models import RouteImage


class Command(BaseCommand):
    """
    This script load milepost from exported csv file into database
    To run this command, do:
    docker exec -ti dot-server python manage.py load_milepost_data <input_file_with_path>
    For example:
    docker exec -ti dot-server python manage.py load_milepost_data metadata/mapped_images_with_milepost.csv
    """
    help = "Process the metadata export input file in csv format to load metadata into database"

    def add_arguments(self, parser):
        # csv filename with full path to load metadata from
        parser.add_argument('input_file', help='input csv file name with full path to be '
                                               'processed and load milepost data from')

    def handle(self, *args, **options):
        input_file = options['input_file']
        df = pd.read_csv(input_file, header=0, index_col='MAPPED_IMAGE',
                         usecols=["MAPPED_IMAGE", "MILEPOST"])
        df.sort_index(inplace=True)
        print(len(df))
        for obj in RouteImage.objects.all():
            obj.mile_post = df.loc[int(obj.image_base_name)].at['MILEPOST']
            obj.save()
        print('Done')
