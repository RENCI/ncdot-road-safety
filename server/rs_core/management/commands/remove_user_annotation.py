from django.core.management.base import BaseCommand
from rs_core.models import UserImageAnnotation


class Command(BaseCommand):
    """
    This script removes user annotation
    To run this command, do:
    docker exec -ti dot-server python manage.py remove_user_annotation <username>
    For example:
    docker exec -ti dot-server python manage.py remove_user_annotation <username>
    """
    help = "Remove user annotation from a user specified by input parameter <username>"

    def add_arguments(self, parser):
        parser.add_argument('user_name', help='user name to remove user annotation for')

    def handle(self, *args, **options):
        user_name = options['user_name']
        UserImageAnnotation.objects.filter(user__username=user_name).delete()
        print('Done')
