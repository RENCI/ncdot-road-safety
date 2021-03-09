import pandas as pd
from django.core.management.base import BaseCommand
from django.db.models import Value
from django.db.models.functions import Concat
from rs_core.models import UserImageAnnotation, AIImageAnnotation


class Command(BaseCommand):
    """
    This script outputs user annotated image info to a text file from db for active learning
    To run this command, do:
    docker exec -ti dot-server python manage.py output_image_info_for_al <feature_name> <output_file_name>
    For example:
    docker exec -ti dot-server python manage.py output_image_info_for_al guardrail metadata/user_annoted_image_info.txt
    """
    help = "Output user annotated image info from db for active learning to a text file specified by " \
           "parameter <output_file_name>"

    def add_arguments(self, parser):
        parser.add_argument('feature_name', help='the feature name to get annotation for, e.g., guardrail')
        # filename with full path to output user annotated image info to
        parser.add_argument('output_file', help='file name with full path to output image info to')

    def handle(self, *args, **options):
        feature_name = options['feature_name']
        output_file = options['output_file']
        image_queryset = UserImageAnnotation.objects.filter(annotation__name__iexact=feature_name,
                                                            presence__isnull=False)
        # output data for active learning
        image_list = list(image_queryset.annotate(
            image_with_path=Concat('image__image_path', Value('/'), 'image__image_base_name',
                                   Value('.jpg'))).values_list('image_with_path', 'presence', 'user__username',
                                                               'left_view', 'front_view', 'right_view',
                                                               'timestamp', 'comment', 'flags__title'))
        df = pd.DataFrame(image_list, columns=['Image', 'Presence', 'Username', 'LeftView', 'FrontView', 'RightView',
                                               'Timestamp', 'Comment', 'Flags'])
        df.to_csv(output_file, index=False)

        # Delete those images from AIImageAnnotation and UserImageAnnotation models since they are not useful for
        # active learning anymore
        image_list = image_queryset.values('image')
        AIImageAnnotation.objects.filter(image__in=image_list).delete()
        image_queryset.delete()
        # delete cached images for the feature as well so that they can be re-sampled and re-annotated
        UserImageAnnotation.objects.filter(annotation__name__iexact=feature_name,
                                           presence__isnull=True).delete()
        print('Done')
