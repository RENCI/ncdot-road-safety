import bisect

from rs_core.models import RouteImage, AIImageAnnotation, UserImageAnnotation, AnnotationSet
from django.contrib.gis.geos import fromstr
from django.contrib.gis.geos import Point
from django.contrib.gis.db.models.functions import Distance


def save_metadata_to_db(route_id, set, image, lat, long):
    route_image = RouteImage.objects.create(
        route_id=str(route_id),
        set=str(set),
        image_base_name=str(image),
        location=fromstr(f'POINT({long} {lat})', srid=4326)
    )
    route_image.save()
    return


def get_image_base_names_by_annotation(annot_name, count, route_id=None):
    if route_id:
        images = AIImageAnnotation.objects.filter(
            annotation__name__iexact=annot_name,
            image__route_id=route_id).order_by('certainty').values_list("image__image_base_name",
                                                                        flat=True).distinct()[:count]
    else:
        images = AIImageAnnotation.objects.filter(
            annotation__name__iexact=annot_name).order_by('certainty').values_list("image__image_base_name",
                                                                                   flat=True).distinct()[:count]

    return list(images)


def get_image_annotations_queryset(image_base_name):
    ai_annot = AIImageAnnotation.objects.filter(image__image_base_name=image_base_name).values_list(
        'annotation__name', flat=True).distinct()
    u_annot = UserImageAnnotation.objects.filter(image__image_base_name=image_base_name).values_list(
        'annotation__name', flat=True).distinct()
    return ai_annot.union(u_annot)


def _create_ai_image_annotation(image, annotation, presence, certainty):
    AIImageAnnotation.objects.get_or_create(image=image,
                                            annotation=annotation,
                                            defaults={'presence': presence, 'certainty': certainty})


def save_guardrail_data_to_db(begin_long, begin_lat, end_long, end_lat, route_id):
    start_loc = Point(float(begin_long), float(begin_lat), srid=4326)
    end_loc = Point(float(end_long), float(end_lat), srid=4326)
    start_image = RouteImage.objects.filter(route_id=route_id).annotate(
        distance=Distance('location', start_loc)).order_by('distance')[0].image_base_name
    end_image = RouteImage.objects.filter(route_id=route_id).annotate(
        distance=Distance('location', end_loc)).order_by('distance')[0].image_base_name
    annot_obj = AnnotationSet.objects.get(name__iexact='guardrail')

    # get all images between start_image and end_image
    qs = RouteImage.objects.filter(image_base_name__gte=start_image, image_base_name__lte=end_image)
    # get total number of images being marked as guardrail
    count = qs.count()
    # partition images into 5 quantiles
    interval = count/5.0
    intervals = []
    for i in range(5):
        intervals.append((i+1) * interval)
    certainty_score_list = [0.5, 0.7, 0.9, 0.7, 0.5]
    index = 1
    for q in qs:
        if count < 5:
            index -= 1
            if count == 4 and index == 2:
                # make the third image certain score the same as the second image for 4 images
                index = 3
            elif (count == 2 or count == 3) and index == count - 1:
                # Make last image has the same certanty score at the first image to cover boundary conditions
                index = intervals[4]
        interval_idx = bisect.bisect_left(intervals, index)
        _create_ai_image_annotation(RouteImage.objects.get(image_base_name=q.image_base_name),
                                    annot_obj, True, certainty_score_list[interval_idx])
        index += 1
    return
