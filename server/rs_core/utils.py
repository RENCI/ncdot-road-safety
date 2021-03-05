import bisect

from django.db.models import Min, Max
from django.conf import settings
from django.contrib.gis.geos import fromstr
from django.contrib.gis.geos import Point
from django.db.models import F
from django.db.models.functions import Abs
from django.contrib.gis.db.models.functions import Distance
from django.contrib.auth.models import User
from django.db import transaction

from rs_core.models import RouteImage, AIImageAnnotation, UserImageAnnotation, AnnotationSet, AnnotationFlag


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


def get_image_base_names_by_annotation(annot_name, req_username, count=5, route_id=None, offset=None):
    if route_id:
        cached_images = UserImageAnnotation.objects.filter(annotation__name__iexact=annot_name,
                                                           user__username=req_username,
                                                           image__route_id=route_id,
                                                           presence__isnull=True).values_list("image__image_base_name",
                                                                                              flat=True)
    else:
        cached_images = UserImageAnnotation.objects.filter(annotation__name__iexact=annot_name,
                                                           user__username=req_username,
                                                           presence__isnull=True).values_list("image__image_base_name",
                                                                                              flat=True)
    cache_cnt = len(cached_images)

    if offset:
        idx1 = offset
        idx2 = offset + count
        if cache_cnt >= idx2:
            return list(cached_images)[idx1:idx2]
    else:
        if cache_cnt >= count:
            return list(cached_images)[:count]
        idx1 = 0
        idx2 = count

    if route_id:
        user_images = UserImageAnnotation.objects.filter(annotation__name__iexact=annot_name,
                                                         image__route_id=route_id).values_list("image__image_base_name")
        filtered_images = AIImageAnnotation.objects.filter(
            uncertainty_group__isnull=False,
            annotation__name__iexact=annot_name, image__route_id=route_id).exclude(
            image__image_base_name__in=user_images)
    else:
        user_images = UserImageAnnotation.objects.filter(
            annotation__name__iexact=annot_name).values_list("image__image_base_name")
        filtered_images = AIImageAnnotation.objects.filter(
            uncertainty_group__isnull=False,
            annotation__name__iexact=annot_name).exclude(image__image_base_name__in=user_images)

    min_group_idx = filtered_images.aggregate(Min('uncertainty_group'))['uncertainty_group__min']
    if settings.USE_IRODS:
        if not filtered_images.exists():
            # images runs out, return empty list
            return []
        max_group_idx = filtered_images.aggregate(Max('uncertainty_group'))['uncertainty_group__max']
        if min_group_idx < max_group_idx:
            group_list = [min_group_idx, min_group_idx + 1]
        else:
            group_list = [min_group_idx]
    else:
        group_list = [min_group_idx, min_group_idx + 1]

    images = filtered_images.filter(uncertainty_group__in=group_list).order_by(
        '-uncertainty_measure', 'image__image_base_name')[:idx2-cache_cnt].values_list(
        'image__image_base_name', flat=True)
    if not images:
        images = filtered_images.annotate(uncertainty=Abs(F('certainty')-0.5)).order_by(
             'uncertainty', 'image__image_base_name')[:idx2-cache_cnt].values_list("image__image_base_name", flat=True)
    if cache_cnt > 0:
        ret_list = list(cached_images)
        ret_list.extend(list(images))
        return ret_list[idx1:]
    else:
        return list(images)[idx1:]


def get_image_annotations_queryset(image_base_name):
    ai_annot = AIImageAnnotation.objects.filter(image__image_base_name=image_base_name).values_list(
        'annotation__name', flat=True).distinct()
    u_annot = UserImageAnnotation.objects.filter(image__image_base_name=image_base_name).values_list(
        'annotation__name', flat=True).distinct()
    return ai_annot.union(u_annot)


def save_annot_data_cache(img_base_name_list, username, annot_name):
    annot_obj = AnnotationSet.objects.get(name__iexact=annot_name)
    user_obj = User.objects.get(username=username)
    obj_list = [UserImageAnnotation(image=RouteImage.objects.get(image_base_name=img_base_name),
                                    annotation=annot_obj,
                                    user=user_obj) for img_base_name in img_base_name_list]
    UserImageAnnotation.objects.bulk_create(obj_list, ignore_conflicts=True)
    return


def save_annot_data_to_db(img_base_name, username, annot_name, annot_views, annot_flags=None, annot_comments=''):
    with transaction.atomic():
        if annot_views['left'] == 'present' or annot_views['front'] == 'present' or annot_views['right'] == 'present':
            presence = True
        else:
            presence = False
        obj, created = UserImageAnnotation.objects.get_or_create(
            image=RouteImage.objects.get(image_base_name=img_base_name),
            annotation=AnnotationSet.objects.get(name__iexact=annot_name),
            user=User.objects.get(username=username),
            defaults={
                'presence': presence,
                'left_view': annot_views['left'][0],
                'front_view': annot_views['front'][0],
                'right_view': annot_views['right'][0],
                'comment': ';'.join(annot_comments) if annot_comments else ''
            }
        )

        if not created:
            # update user annotation
            obj.presence = presence
            obj.left_view = annot_views['left'][0]
            obj.front_view = annot_views['front'][0]
            obj.right_view = annot_views['right'][0]
            obj.comment = ';'.join(annot_comments) if annot_comments else ''
            obj.flags.clear()
            obj.save()
        if annot_flags:
            for flag in annot_flags:
                try:
                    flag_to_add = AnnotationFlag.objects.get(title__iexact=flag)
                    obj.flags.add(flag_to_add)
                except AnnotationFlag.DoesNotExist:
                    continue
    return


def create_ai_image_annotation(image_base_name, annotation, presence, certainty):
    try:
        image = RouteImage.objects.get(image_base_name=image_base_name)
    except RouteImage.DoesNotExist:
        return
    AIImageAnnotation.objects.get_or_create(image=image,
                                            annotation=annotation,
                                            defaults={'presence': presence, 'certainty': certainty})


def update_ai_image_annotation(image_base_name, annotation, presence, certainty):
    try:
        image = RouteImage.objects.get(image_base_name=image_base_name)
    except RouteImage.DoesNotExist:
        return
    obj = AIImageAnnotation.objects.get(image=image, annotation=annotation)
    obj.presence = presence
    obj.certainty = certainty
    obj.save()


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
