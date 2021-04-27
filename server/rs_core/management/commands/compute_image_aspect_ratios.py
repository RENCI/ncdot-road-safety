import os
from PIL import Image

from django.core.management.base import BaseCommand

from django_irods.icommands import SessionException
from django.conf import settings
from rs_core.models import AIImageAnnotation
from rs_core.utils import get_file_from_irods


class Command(BaseCommand):
    """
    This script computes aspect ratio for each image in AIImageAnnotation and update database
    To run this command, do:
    docker exec dot-server python manage.py compute_image_aspect_ratios
    """
    help = "compute image aspect ratio and write to RouteImage model"

    def add_arguments(self, parser):
        pass

    def handle(self, *args, **options):
        for im_obj in AIImageAnnotation.objects.filter(annotation__name='guardrail'):
            im_base_name = im_obj.image.image_base_name
            im_base_path = im_obj.image.image_path
            img_name = f'{im_base_name}1.jpg'
            if settings.USE_IRODS:
                # load image from iRODS
                try:
                    ifile = get_file_from_irods(img_name)
                except SessionException as ex:
                    print(ex.stderr)
            else:
                ifile = os.path.join(settings.DATA_ROOT, im_base_path, img_name)
                if not os.path.isfile(ifile):
                    print(f'{ifile} cannot be found')
            img = Image.open(ifile)
            img_size = img.size
            ar = img_size[0]/img_size[1]
            im_obj.image.aspect_ratio = round(ar, 2)
            im_obj.image.save()
        print('Done')
