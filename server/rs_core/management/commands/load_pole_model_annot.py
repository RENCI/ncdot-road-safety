from django.core.management.base import BaseCommand
import pandas as pd
import random
from rs_core.models import AnnotationSet
from rs_core.utils import create_ai_image_annotation


class Command(BaseCommand):
    """
    This script creates AI info in AIImageAnnotation table by loading annotation info from a csv input file
    To run this command, do:
    docker exec -ti dot-server python manage.py load_pole_model_annot <input_annot_file>
    For example:
    docker exec -ti dot-server python manage.py load_pole_model_annot
    /projects/ncdot/NC_2018_Secondary/active_learning/pole/round0/ncdot_pole_annotations.csv
    """
    help = "load the AI info from input model annotation file"

    def add_arguments(self, parser):
        parser.add_argument('annot_file', help='annotation file to load AI info')

    def handle(self, *args, **options):
        annot_file = options['annot_file']

        df = pd.read_csv(annot_file, header=0, index_col=None, usecols=['MAPPED_IMAGE', 'POLES_ALL'],
                         dtype={'MAPPED_IMAGE': str, 'POLES_ALL': bool})
        print(df.shape)
        annot_obj = AnnotationSet.objects.get(name__iexact='pole')
        df.apply(lambda row: create_ai_image_annotation(row.MAPPED_IMAGE, annot_obj, row.POLES_ALL,
                                                        round(random.uniform(0, 0.5), 2), row.name, 0),
                 axis=1)
        print('Done')
