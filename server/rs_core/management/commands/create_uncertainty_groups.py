from django.core.management.base import BaseCommand
from rs_core.models import AIImageAnnotation


class Command(BaseCommand):
    """
    This script create uncertainty groups from uncertainty measures in database
    To run this command, do:
    docker exec -ti dot-server python manage.py create_uncertainty_groups <annotation_name> <group_size>
    For example:
    docker exec -ti dot-server python manage.py create_uncertainty_groups guardrail 500
    """
    help = "Create the uncertainty groups from uncertainty measures in database"

    def add_arguments(self, parser):
        # csv filename with full path to load metadata from
        parser.add_argument('annot_name', help='annotation name for which uncertainty measures need to be saved')
        parser.add_argument('group_size', type=int, help='number of AIImageAnnotation objects in a group')


    def handle(self, *args, **options):
        annot_name = options['annot_name']
        group_size = options['group_size']
        filtered_images = AIImageAnnotation.objects.filter(annotation__name__iexact=annot_name).exclude(
            uncertainty_measure__isnull=True)
        group_idx = 0
        obj_idx = 0
        for obj in filtered_images.order_by('-uncertainty_measure', 'image__image_base_name'):
            if obj_idx < group_idx * group_size + group_size:
                obj.uncertainty_group = group_idx
            else:
                group_idx += 1
                obj.uncertainty_group = group_idx
            obj.save()
            obj_idx += 1
        print('Done')
