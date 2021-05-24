from django.core.management.base import BaseCommand
from django.db.models import Q
import pandas as pd
import random
from rs_core.models import RouteImage, AnnotationSet
from rs_core.utils import create_ai_image_annotation


class Command(BaseCommand):
    """
    This script creates AI info in AIImageAnnotation table based on random uniform sampling across all divisions
    to prepare for initial annotation aimed at creating an unbiased test holdout dataset
    To run this command, do:
    docker exec -ti dot-server python manage.py create_random_image_ai_info_for_al <annotation_name>
    <image_count_per_region>
    For example:
    docker exec -ti dot-server python manage.py create_random_image_ai_info_for_al pole 320
    """
    help = "create the AI info based on random sampling for annotation aimed at creating an unbiased test " \
           "holdout dataset"

    def add_arguments(self, parser):
        parser.add_argument('annot_name', help='annotation name for which AI info need to be saved')
        parser.add_argument('image_count_per_region', help='number of images to sample from each region')

    def handle(self, *args, **options):
        annot_name = options['annot_name']
        img_count = int(options['image_count_per_region'])

        d4_img_queryset = RouteImage.objects.filter(image_path__istartswith='d04')
        d8_img_queryset = RouteImage.objects.filter(image_path__istartswith='d08')
        query = Q(image_path__istartswith='d13')
        query.add(Q(image_path__istartswith='d14'), Q.OR)
        d1314_img_queryset = RouteImage.objects.filter(query)

        qs_list = [
            d4_img_queryset,
            d8_img_queryset,
            d1314_img_queryset
        ]

        df_list = []

        for qs in qs_list:
            if qs.exists():
                df_list.append(pd.DataFrame.from_records(qs.values("image_base_name")).sample(n=img_count,
                                                                                              random_state=42))

        df = pd.concat(df_list)
        df = df.reset_index(drop=True)
        print(df.shape)
        annot_obj = AnnotationSet.objects.get(name__iexact=annot_name)
        df.apply(lambda row: create_ai_image_annotation(row['image_base_name'], annot_obj, False,
                                                        round(random.uniform(0, 0.5), 2), row.name, 0),
                 axis=1)
        print('Done')
