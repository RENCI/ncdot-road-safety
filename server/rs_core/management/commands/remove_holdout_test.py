import pandas as pd
from django.core.management.base import BaseCommand
from rs_core.models import AIImageAnnotation


class Command(BaseCommand):
    """
    This script removes holdout test images from AIImageAnnotation so they will not be selected for user annotation
    To run this command, do:
    docker exec -ti dot-server python manage.py remove_holdout_test <input_file>
    For example:
    docker exec -ti dot-server python manage.py remove_holdout_test metadata/user_annotated_balanced_image_info.csv
    """
    help = "Remove holdout test from AIImageAnnotation so they will not be selected for user annotation"

    def add_arguments(self, parser):
        parser.add_argument('input_file', help='input file that has holdout test image names')

    def handle(self, *args, **options):
        input_file = options['input_file']
        df = pd.read_csv(input_file, header=0, dtype=str, usecols=['Image'])
        df.Image = df.Image.str.split('/').str[-1]
        df.Image = df.Image.str.replace('.jpg', '')

        AIImageAnnotation.objects.filter(image__in=list(df.Image)).delete()
        print('Done')
