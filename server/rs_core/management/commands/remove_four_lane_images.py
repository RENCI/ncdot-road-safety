import pandas as pd
from json import load, dumps
from django.contrib.gis.geos import GEOSGeometry
from django.contrib.gis.db.models.functions import Distance

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
        parser.add_argument('--geojson_input_file', type=str,
                            help=('Optional. The geojson input file name for rural 2 lane roads'))

    def handle(self, *args, **options):
        input_file = options['input_file']
        route_df = pd.read_csv(input_file, header=0, dtype=str)
        print(route_df.shape)
        route_list = list(route_df['RouteID'])
        RouteImage.objects.all().exclude(route_id__in=route_list).delete()
        print('remaining image count in db after route id filtering: ', RouteImage.objects.count())
        geojson_input_file = options['geojson_input_file']
        if not geojson_input_file:
            geojson_input_file = 'rs_core/static/rs_core/gis/NCRural2LanePrimaryRoads.geojson'

        # create line geometries by route ids
        line_geoms = {}
        for route in route_list:
            line_geoms[route] = None
        with open(geojson_input_file) as f:
            geo_data = load(f)
            features = geo_data['features']
            print('total number of line strings: ', len(features))
            for feat in features:
                rid = feat['properties']['RouteID']
                if not line_geoms[rid]:
                    line_geoms[rid] = GEOSGeometry(dumps(feat['geometry']), srid=4326)
                else:
                    line_geoms[rid].union(GEOSGeometry(dumps(feat['geometry']), srid=4326))
        for rid, value in line_geoms.items():
            print('processing ', rid)
            # distance unit is in meter
            RouteImage.objects.filter(route_id=rid).annotate(
                distance=Distance('location', value, spheroid=True)).exclude(distance__lt=500).delete()
            print('remaining count: ', RouteImage.objects.count())
        print('Done, remaining image count: ', RouteImage.objects.count())
