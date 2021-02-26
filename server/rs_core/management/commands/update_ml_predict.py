import pandas as pd

from django.core.management.base import BaseCommand

from rs_core.models import AnnotationSet, AIImageAnnotation
from rs_core.utils import update_ai_image_annotation


class Command(BaseCommand):
    """
    This script load ML prediction from csv file to update database
    To run this command, do:
    docker exec dot-server python manage.py update_ml_predict <input_file_with_path>
    or
    docker exec dot-server python manage.py update_ml_predict <input_file_with_path> --feature_name guardrail
    For example:
    docker exec dot-server python manage.py update_ml_predict
    /projects/ncdot/NC_2018_Secondary/active_learning/guardrail/round0/predict/predict_d13.csv
    """
    help = "Load the ML prediction in csv format to update database"

    def add_arguments(self, parser):
        # csv filename with full path to load metadata from
        parser.add_argument('input_file', help='input csv file name with full path to be '
                                               'processed and load prediction data from')
        parser.add_argument('--feature_name', type=str,
                            help=('Optional. The feature name the ML prediction is for'))

    def handle(self, *args, **options):
        input_file = options['input_file']
        feature_name = options['feature_name']
        if not feature_name:
            feature_name = 'guardrail'
        df = pd.read_csv(input_file, header=0, index_col=False, dtype={'MAPPED_IMAGE': 'str',
                                                                       'ROUND_PREDICT': 'float'})
        print(df.shape)
        df['MAPPED_IMAGE'] = df['MAPPED_IMAGE'].str.replace('.jpg', '')
        df['MAPPED_IMAGE'] = df['MAPPED_IMAGE'].str.split('/').str[-1]
        image_list = list(AIImageAnnotation.objects.values_list("image", flat=True))
        df = df[df.MAPPED_IMAGE.isin(image_list)]
        annot_obj = AnnotationSet.objects.get(name__iexact=feature_name)
        df.apply(lambda row: update_ai_image_annotation(row['MAPPED_IMAGE'], annot_obj,
                                                        True if row["ROUND_PREDICT"] >= 0.5 else False,
                                                        row["ROUND_PREDICT"]), axis=1)
        print('Done')
