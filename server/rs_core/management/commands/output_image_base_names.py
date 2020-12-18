import pandas as pd
from django.core.management.base import BaseCommand
from rs_core.models import RouteImage


class Command(BaseCommand):
    """
    This script output image base names to a text file from db
    To run this command, do:
    docker exec -ti dot-server python manage.py output_image_base_names <output_file_name>
    For example:
    docker exec -ti dot-server python manage.py output_image_base_names metadata/image_base_names.txt
    """
    help = "Output image base name from db to a text file specified by parameter <output_file_name>"

    def add_arguments(self, parser):
        # filename with full path to output image base names to
        parser.add_argument('output_file', help='file name with full path to output image base names to')

    def handle(self, *args, **options):
        output_file = options['output_file']
        image_list = list(RouteImage.objects.values_list("image_base_name", flat=True))
        df = pd.DataFrame(image_list, columns=['ImageBaseName'])
        df.to_csv(output_file, index=False)
        print('Done')
