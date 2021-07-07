from django.core.management.base import BaseCommand
from rs_core.models import RouteImage


class Command(BaseCommand):
    """
    This script compute image index along its route and populate the new route_index field in RouteImage model
    To run this command, do:
    docker exec dot-server python manage.py compute_image_route_index
    """
    help = "compute image route index along its route and write to RouteImage model"

    def add_arguments(self, parser):
        pass

    def handle(self, *args, **options):
        for rid in RouteImage.objects.values_list("route_id").distinct():
            idx = 1
            for img in RouteImage.objects.filter(route_id=rid[0]).order_by('mile_post'):
                img.route_index = idx
                img.save()
                idx += 1

        print('Done')
