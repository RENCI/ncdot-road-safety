import pandas as pd

from django.core.management.base import BaseCommand

from rs_core.models import RouteImage


def image_covered(ref_data, mile_post):
    if isinstance(ref_data, pd.Series):
        mp1 = min(ref_data['BeginMp1'], ref_data['EndMp1'])
        mp2 = max(ref_data['BeginMp1'], ref_data['EndMp1'])
        if mp1 <= mile_post <= mp2:
            return True
        else:
            return False
    else: # DataFrame
        intervals = list(zip(ref_data['BeginMp1'], ref_data['EndMp1']))
        for start, stop in intervals:
            if start <= mile_post <= stop or stop <= mile_post <= start:
                return True
        return False


class Command(BaseCommand):
    """
    This script remove 4 lane images from database by mileposts
    To run this command, do:
    docker exec -ti dot-server python manage.py remove_four_lane_images_by_milepost <input_file_with_path>
    For example:
    docker exec -ti dot-server python manage.py remove_four_lane_images_by_milepost metadata/NCRural2LanePrimaryRoadsInfo.csv
    """
    help = "Remove 4 lane images from database by only keeping images on the routes loaded from the input file " \
           "according to mileposts"

    def add_arguments(self, parser):
        # csv filename with full path to load metadata from
        parser.add_argument('input_file', help='input csv file name with full path to include routes and milepost '
                                               'info for each segment in shape file to be kept')

    def handle(self, *args, **options):
        input_file = options['input_file']
        route_df = pd.read_csv(input_file, header=0, usecols=['RouteID', 'BeginMp1', 'EndMp1'],
                               dtype={'RouteID': str, 'BeginMp1': float, 'EndMp1': float})
        route_df.set_index('RouteID', inplace=True)
        route_df.sort_index()
        print(route_df.shape)

        for obj in RouteImage.objects.all():
            if not image_covered(route_df.loc[obj.route_id], obj.mile_post):
                obj.delete()
            break
        print('Done - remaining images:', RouteImage.objects.count())
