import pandas as pd

from django.core.management.base import BaseCommand

from rs_core.models import RouteImage


class Command(BaseCommand):
    """
    This script remove 4 lane images from database
    To run this command, do:
    docker exec -ti dot-server python manage.py remove_four_lane_images <input_file_with_path>
    For example:
    docker exec -ti dot-server python manage.py remove_four_lane_images metadata/route_ids_with_2_lanes.csv
    """
    help = "Remove 4 lane images from database by only keeping routes loaded from the input file"

    def add_arguments(self, parser):
        # csv filename with full path to load metadata from
        parser.add_argument('input_file', help='input csv file name with full path to include '
                                               'routes to be kept')

    def handle(self, *args, **options):
        input_file = options['input_file']
        route_df = pd.read_csv(input_file, header=0, dtype=str)
        print(route_df.shape)
        route_list = list(route_df['RouteID'])
        RouteImage.objects.all().exclude(route_id__in=route_list).delete()
        print('Done - remaining image count in db: ', RouteImage.objects.count())
