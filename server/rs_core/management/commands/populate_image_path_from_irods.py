from django.core.management.base import BaseCommand
from django_irods.storage import IrodsStorage

from rs_core.models import RouteImage


class Command(BaseCommand):
    """
    This script populate image_path field in RouteImage model from iRODS
    To run this command, do:
    docker exec -ti dot-server python manage.py populate_image_path_from_irods
    """
    help = "Populate image_path field in RouteImage model in database from iRODS"

    def add_arguments(self, parser):
        pass

    def handle(self, *args, **options):
        istorage = IrodsStorage()
        irods_prefix_str = '/ncdotZone/home/dotProxyUser/images/'
        vault_prefix_str = '/projects/ncdot/2018/NC_2018_Images/'
        for obj in RouteImage.objects.all():
            path = istorage.get_image_coll_path(f'{obj.image_base_name}5.jpg')
            if path.startswith(irods_prefix_str):
                path = '{}{}'.format(vault_prefix_str, path[len(irods_prefix_str):])
                obj.image_path = path
                obj.save()
            else:
                print(f'{path} does not start with irods_prefix_str', flush=True)
        print('Done')
