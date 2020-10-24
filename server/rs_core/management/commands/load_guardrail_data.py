import pandas as pd

from django.core.management.base import BaseCommand
from django.conf import settings

from rs_core.utils import save_guardrail_data_to_db
from rs_core.models import RouteImage


class Command(BaseCommand):
    """
    This script load guardrail annotation data from csv file into database
    To run this command, do:
    docker exec -ti dot-server python manage.py load_guardrail_data <input_file_with_path>
    For example:
    docker exec -ti dot-server python manage.py load_guardrail_data metadata/Guardrail.csv
    """
    help = "Process the guardrail data in csv format to load guardrail data into database"

    def add_arguments(self, parser):
        # csv filename with full path to load metadata from
        parser.add_argument('input_file', help='input csv file name with full path to be '
                                               'processed and load guardrail data from')

    def handle(self, *args, **options):
        input_file = options['input_file']
        df = pd.read_csv(input_file, header=0, index_col=False)
        df['Route'] = df['Route'].astype('string')
        if settings.DEBUG:
            route_list = list(RouteImage.objects.values_list("route_id", flat=True).distinct())
            df = df[df.Route.isin(route_list)]

        print(df.shape)
        df.apply(lambda row: save_guardrail_data_to_db(row['beginLongitude'], row['beginLatitude'],
                                                       row['endLongitude'], row['endLatitude'], row['Route']), axis=1)
        print('Done')
