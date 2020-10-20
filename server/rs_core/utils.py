from rs_core.models import RouteImage, AIImageAnnotation, UserImageAnnotation
from django.contrib.gis.geos import fromstr


def save_metadata_to_db(route_id, set, image, lat, long):
    route_image = RouteImage.objects.create(
        route_id=str(route_id),
        set=str(set),
        image_base_name=str(image),
        location=fromstr(f'POINT({long} {lat})', srid=4326)
    )
    route_image.save()
    return


def get_image_base_names_by_annotation(annot_name, route_id=None):
    if route_id:
        images1 = AIImageAnnotation.objects.filter(annotation__name__iexact=annot_name,
                                                   image__route_id=route_id).values_list("image__image_base_name",
                                                                                         flat=True).distinct()
        images2 = UserImageAnnotation.objects.filter(annotation__name__iexact=annot_name,
                                                     image__route_id=route_id).values_list("image__image_base_name",
                                                                                           flat=True).distinct()
    else:
        images1 = AIImageAnnotation.objects.filter(
            annotation__name__iexact=annot_name).values_list("image__image_base_name", flat=True).distinct()
        images2 = UserImageAnnotation.objects.filter(
            annotation__name__iexact=annot_name).values_list("image__image_base_name", flat=True).distinct()

    return list(images1.union(images2))


def get_image_annotations_queryset(image_base_name):
    ai_annot = AIImageAnnotation.objects.filter(image__image_base_name=image_base_name).values_list(
        'annotation__name', flat=True).distinct()
    u_annot = UserImageAnnotation.objects.filter(image__image_base_name=image_base_name).values_list(
        'annotation__name', flat=True).distinct()
    return ai_annot.union(u_annot)
