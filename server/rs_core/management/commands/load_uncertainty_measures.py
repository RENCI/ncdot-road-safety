from django.core.management.base import BaseCommand
from django.conf import settings
import pandas as pd
from rs_core.models import RouteImage, AIImageAnnotation
from rs_core.utils import save_uncertainty_measure_to_db


class Command(BaseCommand):
    """
    This script load uncertainty measures from csv file into database
    To run this command, do:
    docker exec -ti dot-server python manage.py load_uncertainty_measures <input_csv_file_with_path> <annotation_name>
    For example:
    docker exec -ti dot-server python manage.py load_uncertainty_measures
    metadata/image_uncertainty_scores.csv guardrail
    """
    help = "Load the uncertainty measures file in csv format into database"

    def add_arguments(self, parser):
        # csv filename with full path to load metadata from
        parser.add_argument('input_file', help='input csv file name with full path to be '
                                               'processed and load user annotation from')
        parser.add_argument('annot_name', help='annotation name for which uncertainty measures need to be saved')


    def handle(self, *args, **options):
        input_file = options['input_file']
        annot_name = options['annot_name']
        df = pd.read_csv(input_file, header=0, index_col=False, dtype=str, usecols=["MAPPED_IMAGE",
                                                                                    "UNCERTAINTY"])
        count = RouteImage.objects.count()
        df_len = len(df)
        print(count, df_len, settings.USE_IRODS)
        if settings.USE_IRODS:
            # cannot load uncertainty score from csv file, computing uncertainty score instead
            for obj in AIImageAnnotation.objects.all():
                obj.uncertainty_measure = abs(obj.certainty - 0.5)
                obj.save()
        else:
            df.apply(lambda row: save_uncertainty_measure_to_db(row['MAPPED_IMAGE'], annot_name, row['UNCERTAINTY']),
                     axis=1)
        print('Done')
