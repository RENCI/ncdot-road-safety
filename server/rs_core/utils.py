from rs_core.models import RouteImage
from django.contrib.gis.geos import fromstr


def save_metadata_to_db(route_id, set, image, lat, long):
    route_image = RouteImage.objects.create(
        route_id=route_id,
        set=set,
        image_base_name=''.join(image.split(':')),
        location=fromstr(f'POINT({long} {lat})', srid=4326)
    )
    route_image.save()
    return
