import pandas as pd

from django.core.management.base import BaseCommand
from django.conf import settings

from rs_core.utils import create_ai_image_annotation
from rs_core.models import RouteImage, AnnotationSet


class Command(BaseCommand):
    """
    This script output guardrail annotation data with 2 lanes for 2 lanes guardrail model training
    To run this command, do:
    docker exec -ti dot-server python manage.py output_guardrail_data_with_2lanes
    <input_file_with_path> <output_file_with_path>
    For example:
    docker exec -ti dot-server python manage.py output_guardrail_data_with_2lanes
    metadata/training_image_set_1370774.csv metadata/training_image_guardrail_yn_2lanes.csv
    """
    help = "Output guardrail label data with 2 lanes in csv format"

    def add_arguments(self, parser):
        # csv filename with full path to load metadata from
        parser.add_argument('input_file', help='input csv file name with full path for '
                                               'full guardrail training data')
        parser.add_argument('output_file', help='output csv file name with full path for '
                                                'processed guardrail training data with 2 lanes')

    def handle(self, *args, **options):
        input_file = options['input_file']
        output_file = options['output_file']
        df = pd.read_csv(input_file, header=0, index_col=False, dtype=str, usecols=['MAPPED_IMAGE', 'GUARDRAIL_YN'])
        image_list = list(RouteImage.objects.values_list("image_base_name", flat=True))
        df = df[df.MAPPED_IMAGE.isin(image_list)]
        print(df.shape)
        df_yes = df[df.GUARDRAIL_YN=='Y']
        df_no = df[df.GUARDRAIL_YN == 'N']
        df_yes_count = len(df_yes)
        print(df_yes.shape, df_yes_count)
        print(df_no.shape, len(df_no))
        df_no = df_no.sample(n=df_yes_count, random_state=1)
        df = pd.concat([df_yes, df_no], ignore_index=True)
        df.to_csv(output_file, index=False)
        print('Done')
