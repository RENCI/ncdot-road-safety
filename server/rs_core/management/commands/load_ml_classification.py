import pandas as pd

from django.core.management.base import BaseCommand

from rs_core.models import AnnotationSet
from rs_core.utils import update_or_create_ai_image_annotation


class Command(BaseCommand):
    """
    This script load guardrail classification data from csv file into database
    To run this command, do:
    docker exec -ti dot-server python manage.py load_ml_classification <input_file_with_path>
    or
    docker exec -ti dot-server python manage.py load_ml_classification <input_file_with_path> --feature_name guardrail
    For example:
    docker exec -ti dot-server python manage.py load_ml_classification metadata/guardrail_classification_dev.csv
    """
    help = "Load the ML-predicted classification data in csv format into database"

    def add_arguments(self, parser):
        # csv filename with full path to load metadata from
        parser.add_argument('input_file', help='input csv file name with full path to be '
                                               'processed and load guardrail data from')
        parser.add_argument('--feature_name', type=str,
                            help=('Optional. The feature name for classification'))

    def handle(self, *args, **options):
        input_file = options['input_file']
        feature_name = options['feature_name']
        if not feature_name:
            feature_name = 'guardrail'
        df = pd.read_csv(input_file, header=0, index_col='MAPPED_IMAGE', dtype={'MAPPED_IMAGE': 'str',
                                                                                'Probability': 'float'})
        print(df.shape)
        annot_obj = AnnotationSet.objects.get(name__iexact='guardrail')
        for image_name in df.index:
            certainty = df.loc[image_name].at['Probability']
            if pd.isna(certainty):
                certainty = -1
            presence = True if certainty >= 0.5 else False
            update_or_create_ai_image_annotation(image_name, annot_obj, presence, certainty)
        print('Done')
