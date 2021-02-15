import pandas as pd
from django.core.management.base import BaseCommand
from django.db.models import Value
from django.db.models.functions import Concat
from rs_core.models import UserImageAnnotation


class Command(BaseCommand):
    """
    This script outputs user annotated image info to a text file from db for active learning
    To run this command, do:
    docker exec -ti dot-server python manage.py output_image_info_for_al <al_round> <output_file_name>
    For example:
    docker exec -ti dot-server python manage.py output_image_info_for_al 1 metadata/user_annoted_image_info.txt
    """
    help = "Output user annotated image info from db for active learning to a text file specified by " \
           "parameter <output_file_name>"

    def add_arguments(self, parser):
        parser.add_argument('al_round', help='the round for active learning, starting from 1')
        # filename with full path to output user annotated image info to
        parser.add_argument('output_file', help='file name with full path to output image info to')

    def handle(self, *args, **options):
        al_round = int(options['al_round'])
        output_file = options['output_file']
        if al_round <= 1:
            image_queryset = UserImageAnnotation.objects.all()
        else:
            image_queryset = UserImageAnnotation.objects.exclude(al_round__lt=al_round)

        # output data for the iniital first round of active learning
        image_list = list(image_queryset.annotate(
            image_with_path=Concat('image__image_path', Value('/'), 'image__image_base_name',
                                   Value('.jpg'))).values_list("image_with_path", 'presence'))
        df = pd.DataFrame(image_list, columns=['Image', 'Presence'])
        df.to_csv(output_file, index=False)
        for obj in image_queryset:
            obj.al_round = al_round
            obj.save()
        print('Done')
