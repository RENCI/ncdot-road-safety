from django.core.management.base import BaseCommand
import pandas as pd
from rs_core.models import AIImageAnnotation
from rs_core.utils import save_uncertainty_measure_to_db


class Command(BaseCommand):
    """
    This script creates uncertainty measures based on random sampling to sort images for annotation aimed at
    creating an unbiased test holdout dataset
    To run this command, do:
    docker exec -ti dot-server python manage.py create_random_uncertainty_measures <division> <annotation_name>
    For example:
    docker exec -ti dot-server python manage.py create_random_uncertainty_measures d04 guardrail
    """
    help = "create the uncertainty measures based on random sampling to sort images for annotation aimed at " \
           "creating an unbiased test holdout dataset"

    def add_arguments(self, parser):
        # csv filename with full path to load metadata from
        parser.add_argument('division', help='division str to create test holdout dataset for')
        parser.add_argument('annot_name', help='annotation name for which uncertainty measures need to be saved')


    def handle(self, *args, **options):
        division = options['division']
        annot_name = options['annot_name']
        # delete existing uncertainty measures and uncertainty groups if any
        for obj in AIImageAnnotation.objects.filter(annotation__name=annot_name, uncertainty_group__isnull=False):
            obj.uncertainty_measure = None
            obj.uncertainty_group = None
            obj.save()
        df = pd.DataFrame.from_records(
            AIImageAnnotation.objects.filter(
                annotation__name=annot_name, image__image_path__istartswith=division).values(
                "image__image_base_name"))
        print(df.shape)
        sub_df = df.sample(frac=0.02, random_state=42)
        sub_df.reset_index(drop=True)
        print(sub_df.shape)


        sub_df.apply(lambda row: save_uncertainty_measure_to_db(row['image__image_base_name'], annot_name,
                                                                row.name), axis=1)
        print('Done')
