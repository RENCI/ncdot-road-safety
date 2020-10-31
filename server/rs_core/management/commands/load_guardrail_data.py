import pandas as pd

from django.core.management.base import BaseCommand
from django.conf import settings

from rs_core.utils import create_ai_image_annotation
from rs_core.models import RouteImage, AnnotationSet


class Command(BaseCommand):
    """
    This script load guardrail annotation data from csv file into database
    To run this command, do:
    docker exec -ti dot-server python manage.py load_guardrail_data <input_file_with_path>
    For example:
    docker exec -ti dot-server python manage.py load_guardrail_data metadata/training_Image_guardrail_yn.csv
    """
    help = "Load the processed guardrail data in csv format into database"

    def add_arguments(self, parser):
        # csv filename with full path to load metadata from
        parser.add_argument('input_file', help='input csv file name with full path to be '
                                               'processed and load guardrail data from')

    def handle(self, *args, **options):
        input_file = options['input_file']
        df = pd.read_csv(input_file, header=0, index_col=False, dtype=str)
        if settings.DEBUG:
            route_list = list(RouteImage.objects.values_list("route_id", flat=True).distinct())
            df = df[df.ROUTEID.isin(route_list)]
        print(df.shape)
        annot_obj = AnnotationSet.objects.get(name__iexact='guardrail')
        df.apply(lambda row: create_ai_image_annotation(row['MAPPED_IMAGE'],
                                                        annot_obj, True if row['GUARDRAIL_YN'] == 'Y' else False,
                                                        float(row['CERTAINTY'])), axis=1)
        print('Done')
