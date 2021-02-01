import bisect

from django.contrib.gis.geos import fromstr
from django.contrib.gis.geos import Point
from django.db.models import F
from django.db.models.functions import Abs
from django.contrib.gis.db.models.functions import Distance
from django.contrib.auth.models import User
from django.db import transaction

from rs_core.models import RouteImage, AIImageAnnotation, UserImageAnnotation, AnnotationSet


def save_metadata_to_db(route_id, image, lat, long, milepost='', path='', predict=None, feature_name='guardrail'):

    route_image, created = RouteImage.objects.get_or_create(
        route_id=str(route_id),
        image_base_name=str(image),
        defaults={'location': fromstr(f'POINT({long} {lat})', srid=4326),
                  'mile_post': milepost,
                  'image_path': path}
    )

    if predict is not None:
        annot_obj = AnnotationSet.objects.get(name__iexact=feature_name)
        presence = True if predict >= 0.5 else False
        AIImageAnnotation.objects.get_or_create(image=route_image,
                                                annotation=annot_obj,
                                                defaults={'presence': presence, 'certainty': predict})
    return


def get_image_base_names_by_annotation(annot_name, count=10, route_id=None, offset=None):
    if count and offset:
        idx1 = offset
        idx2 = offset + count
    else:
        idx1 = 0
        idx2 = count

    if route_id:
        user_images = UserImageAnnotation.objects.filter(annotation__name__iexact=annot_name,
                                                         image__route_id=route_id).values_list("image__image_base_name")
        filtered_images = AIImageAnnotation.objects.filter(
            annotation__name__iexact=annot_name, image__route_id=route_id).exclude(
            image__image_base_name__in=user_images)
    else:
        user_images = UserImageAnnotation.objects.filter(
            annotation__name__iexact=annot_name).values_list("image__image_base_name")
        filtered_images = AIImageAnnotation.objects.filter(
            annotation__name__iexact=annot_name).exclude(image__image_base_name__in=user_images)

    filtered_images_2 = filtered_images.exclude(uncertainty_measure__isnull=True)
    if filtered_images_2:
        images = filtered_images_2.order_by('uncertainty_measure', 'image__image_base_name')[idx1:idx2].values_list(
            "image__image_base_name", flat=True)
    else:
        images = filtered_images.annotate(uncertainty=Abs(F('certainty')-0.5)).order_by(
             'uncertainty', 'image__image_base_name')[idx1:idx2].values_list("image__image_base_name", flat=True)

    return list(images)


def get_image_annotations_queryset(image_base_name):
    ai_annot = AIImageAnnotation.objects.filter(image__image_base_name=image_base_name).values_list(
        'annotation__name', flat=True).distinct()
    u_annot = UserImageAnnotation.objects.filter(image__image_base_name=image_base_name).values_list(
        'annotation__name', flat=True).distinct()
    return ai_annot.union(u_annot)


def save_annot_data_to_db(img_base_name, username, annot_name, annot_present, annot_flag=None,
                          annot_present_views='', annot_comment=''):
    with transaction.atomic():
        obj, created = UserImageAnnotation.objects.get_or_create(
            image=RouteImage.objects.get(image_base_name=img_base_name),
            annotation=AnnotationSet.objects.get(name__iexact=annot_name),
            user=User.objects.get(username=username),
            defaults={
                'presence': annot_present,
                'presence_views': annot_present_views,
                'comment': annot_comment,
                'flag': annot_flag if annot_flag is not None and annot_flag else False
            }
        )
        if not created:
            # update user annotation
            obj.presence = annot_present
            obj.presence_views = annot_present_views
            obj.comment = annot_comment

            if annot_flag is not None:
                obj.flag = annot_flag
            obj.save()
    return


def create_ai_image_annotation(image_base_name, annotation, presence, certainty):
    try:
        image = RouteImage.objects.get(image_base_name=image_base_name)
    except RouteImage.DoesNotExist:
        return
    AIImageAnnotation.objects.get_or_create(image=image,
                                            annotation=annotation,
                                            defaults={'presence': presence, 'certainty': certainty})


def update_or_create_ai_image_annotation(image_base_name, annotation, presence, certainty):
    try:
        image = RouteImage.objects.get(image_base_name=image_base_name)
    except RouteImage.DoesNotExist:
        return
    AIImageAnnotation.objects.update_or_create(image=image, annotation=annotation,
                                               defaults={'presence': presence, 'certainty': certainty})


def save_uncertainty_measure_to_db(image_base_name, annotation, uncertainty):
    try:
        image = RouteImage.objects.get(image_base_name=image_base_name)
    except RouteImage.DoesNotExist:
        return
    obj = AIImageAnnotation.objects.get(image=image, annotation=annotation)
    obj.uncertainty_measure = uncertainty
    obj.save()


def save_guardrail_data_to_db_old(begin_long, begin_lat, end_long, end_lat, route_id):
    start_loc = Point(float(begin_long), float(begin_lat), srid=4326)
    end_loc = Point(float(end_long), float(end_lat), srid=4326)
    start_image_filter = RouteImage.objects.filter(route_id=route_id).annotate(
        distance=Distance('location', start_loc)).order_by('distance')
    if not start_image_filter:
        print('route', route_id, 'does not exist')
        return
    if start_image_filter[0].distance.m > 10:
        print('distance ', start_image_filter[0].distance, ' is too big, not counting as guardrail')
        start_image = None
    else:
        start_image = start_image_filter[0].image_base_name
    end_image_filter = RouteImage.objects.filter(route_id=route_id).annotate(
        distance=Distance('location', end_loc)).order_by('distance')
    if end_image_filter[0].distance.m > 10:
        print('distance ', end_image_filter[0].distance, ' is too big, not counting as guardrail')
        end_image = None
    else:
        end_image = end_image_filter[0].image_base_name

    if not start_image and not end_image:
        print('both start and end images are None: ', begin_long, begin_lat, end_long, end_lat, route_id)
        return
    elif not start_image:
        print('start image is None: ', begin_long, begin_lat, end_long, end_lat, route_id)
        return
    elif not end_image:
        print('end image is None: ', begin_long, begin_lat, end_long, end_lat, route_id)
        return

    annot_obj = AnnotationSet.objects.get(name__iexact='guardrail')


    # get all images between start_image and end_image
    qs = RouteImage.objects.filter(image_base_name__gte=start_image, image_base_name__lte=end_image)
    # get total number of images being marked as guardrail
    count = qs.count()
    print(begin_long, begin_lat, end_long, end_lat, route_id, start_image, end_image, count)
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
        create_ai_image_annotation(q.image_base_name,
                                    annot_obj, True, certainty_score_list[interval_idx])
        index += 1
    return
