import os
import io
import json
import random
from datetime import timezone, datetime
import logging
from PIL import Image

from django.db import transaction
from django.contrib.admin.views.decorators import user_passes_test
from django.contrib.auth.views import PasswordResetView, LogoutView
from django.contrib.auth import login, authenticate
from django.forms.models import inlineformset_factory
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.core.exceptions import ObjectDoesNotExist
from django.db import IntegrityError
from django.db.models import Sum, Count
from django.contrib import messages
from django.conf import settings
from django.contrib.messages import info
from django.utils.translation import ugettext_lazy as _
from django.core.mail import send_mail
from django.http import HttpResponse, HttpResponseForbidden, HttpResponseRedirect, \
    HttpResponseServerError, JsonResponse

from django_irods.icommands import SessionException
from django.contrib.gis.db.models.functions import Distance
from django.contrib.gis.geos import Point
from rest_framework import status

from rs_core.forms import SignupForm, UserProfileForm, UserPasswordResetForm
from rs_core.models import UserProfile, RouteImage, AnnotationSet, AIImageAnnotation, UserImageAnnotation, \
    UserAnnotationSummary, HoldoutTestInfo
from rs_core.utils import get_image_base_names_by_annotation, get_image_annotations_queryset, \
    save_annot_data_to_db, save_annot_data_cache, get_file_from_irods


logger = logging.getLogger('django')


class RequestPasswordResetView(PasswordResetView):
    form_class = UserPasswordResetForm


@login_required
def logout(request):
    return LogoutView.as_view(next_page='/')(request)


def signup(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            form.save(commit=False)
            # concatenate first_name and last_name to create username and append a number if
            # that username already exists to create a unique username
            firstname = form.cleaned_data.get('first_name')
            lastname = form.cleaned_data.get('last_name')
            org = form.cleaned_data.get('organization')
            years_of_service = form.cleaned_data.get('years_of_service')
            email = form.cleaned_data.get('email')
            username = form.cleaned_data.get('username')
            raw_pwd = form.cleaned_data.get('password1')

            # it is important to set email field on User object even though email field is already set on user profile
            # otherwise, password reset will not work
            new_user = User.objects.create_user(username, first_name=firstname,
                                                last_name=lastname,
                                                password=raw_pwd,
                                                email=email,
                                                is_active=False if settings.ACCOUNTS_APPROVAL_REQUIRED else True
            )
            up = UserProfile(user=new_user, organization=org, years_of_service=years_of_service, email=email)
            try:
                up.save()
            except IntegrityError as ex:
                # violate email uniqueness, raise error and roll back
                new_user.delete()
                return render(request, 'registration/signup.html', {'form': form,
                                                                    'error_message': ex.message})
            if new_user.is_active:
                user = authenticate(username=username, password=raw_pwd)
                info(request, _("Successfully signed up"))
                login(request, user)
                return redirect('home')
            else:
                # email admin that a new user has signed up and need approval
                email_recip_str = settings.EMAIL_ADMIN_LIST
                email_recip_list = email_recip_str.split('---')
                message = """Dear administrator,
                <p>NCDOT Annotation Tool received a sign up request from {first_name} {last_name} (username: {username},
                 email: {email}). Please go to <a href="{url}">{url}</a> to look at the user profile detail and approve
                 the user as appropriate. The user will not be able to login until being approved. 
                <p>Thank you</p>
                """.format(first_name=new_user.first_name, last_name=new_user.last_name, username=new_user.username,
                           email=new_user.user_profile.email, scheme=request.scheme, host=request.get_host,
                           url=request.build_absolute_uri('/admin/')
                           )
                send_mail(subject="Need approval of a user signed up for DOT annotation tool",
                          message=message,
                          html_message=message,
                          from_email= settings.DEFAULT_FROM_EMAIL,
                          recipient_list=email_recip_list,
                          fail_silently=True)
                info(request, _("Thanks for signing up! You'll receive an email when your account is approved and "
                                "activated."))
                return redirect('home')
    else:
        form = SignupForm()
    return render(request, 'registration/signup.html', {'form': form})


@login_required
def edit_user(request, pk):
    user = User.objects.get(pk=pk)
    user_form = UserProfileForm(instance=user)

    if not user.is_authenticated or request.user.id != user.id:
        return HttpResponseForbidden('You are not authenticated to edit user profile')

    ProfileInlineFormset = inlineformset_factory(User, UserProfile,
                                                 fields=('organization', 'years_of_service', 'email'),
                                                 can_delete=False)
    formset = ProfileInlineFormset(instance=user)

    if request.method == "POST":
        user_form = UserProfileForm(request.POST, instance=user)
        formset = ProfileInlineFormset(request.POST, instance=user)
        if user_form.is_valid():
            created_user = user_form.save(commit=False)
            formset = ProfileInlineFormset(request.POST, instance=created_user)
            if formset.is_valid():
                created_user.email = formset.cleaned_data[0]['email']
                created_user.save()
                formset.save()
                messages.info(request, "Your profile is updated successfully")
                return HttpResponseRedirect(request.META['HTTP_REFERER'])

    return render(request, 'accounts/account_update.html', {"profile_form": user_form,
                                                            "formset": formset
                                                            })


@login_required
def get_user_info(request, uid):
    if not request.user.is_authenticated:
        return JsonResponse({'error': 'you are not authenticated to get user info'}, status=status.HTTP_401_UNAUTHORIZED)
    try:
        user = User.objects.get(pk=uid)
        up = user.user_profile
    except ObjectDoesNotExist as ex:
        return JsonResponse({'error': 'requested user does not exist'}, status=status.HTTP_404_NOT_FOUND)

    user_info_dict = {'username': user.username,
                      'firstname': user.first_name,
                      'lastname': user.last_name,
                      'email': up.email,
                      'organization': up.organization,
                      'years_of_service': up.years_of_service
                      }
    return JsonResponse(user_info_dict, status=status.HTTP_200_OK)


@login_required
def get_user_annot_info(request, uid):
    if not request.user.is_authenticated:
        return JsonResponse({'error': 'you are not authenticated to get user annotation info'},
                            status=status.HTTP_401_UNAUTHORIZED)
    try:
        user = User.objects.get(pk=uid)
        summary_annot_list = list(UserAnnotationSummary.objects.values_list('annotation__name', flat=True).distinct())
        annot_total_dict = {}
        if summary_annot_list:
            for annot in summary_annot_list:
                total_pos_val = UserAnnotationSummary.objects.filter(user=user,
                                                                     annotation__name=annot,
                                                                     presence=True).aggregate(Sum('total'))
                total_neg_val = UserAnnotationSummary.objects.filter(user=user,
                                                                     annotation__name=annot,
                                                                     presence=False).aggregate(Sum('total'))
                annot_total_dict[annot] = {
                    'positive': total_pos_val['total__sum'] if total_pos_val['total__sum'] is not None else 0,
                    'negative': total_neg_val['total__sum'] if total_pos_val['total__sum'] is not None else 0
                }
        else:
            annot_total_dict['guardrail'] = {'positive': 0,
                                             'negative': 0}
        annot_current_dict = {}
        user_annot_list = list(UserImageAnnotation.objects.values_list('annotation__name', flat=True).distinct())
        if user_annot_list:
            for annot in user_annot_list:
                total_pos_current = UserImageAnnotation.objects.filter(user=user,
                                                                       annotation__name=annot,
                                                                       presence=True).aggregate(Count('image'))
                total_neg_current = UserImageAnnotation.objects.filter(user=user,
                                                                       annotation__name=annot,
                                                                       presence=False).aggregate(Count('image'))
                annot_current_dict[annot] = {
                    'positive': total_pos_current['image__count'] if total_pos_current['image__count'] is not None else 0,
                    'negative': total_neg_current['image__count'] if total_neg_current['image__count'] is not None else 0
                }
        else:
            annot_current_dict['guardrail'] = {'positive': 0,
                                               'negative': 0}

    except ObjectDoesNotExist as ex:
        return JsonResponse({'error': 'requested user does not exist'}, status=status.HTTP_404_NOT_FOUND)

    user_annot_info_dict = {'username': user.username,
                      'total_annots_in_previous_rounds': annot_total_dict,
                      'total_annots_in_current_round': annot_current_dict
                      }
    return JsonResponse(user_annot_info_dict, status=status.HTTP_200_OK)


@login_required
def get_original_image_by_name(request, name):
    if settings.USE_IRODS:
        try:
            ifile = get_file_from_irods(name)
        except SessionException as ex:
            return HttpResponseServerError(ex.stderr)
    else:
        image_base_name = name[:11]
        image_path = RouteImage.objects.get(image_base_name=image_base_name).image_path
        ifile = os.path.join(settings.DATA_ROOT, image_path, name)
        if not os.path.isfile(ifile):
            return HttpResponseServerError(f'{ifile} cannot be found')

    return HttpResponse(open(ifile, 'rb'), content_type='image/jpg')


@login_required
def get_image_by_name(request, name):
    if settings.USE_IRODS:
        try:
            ifile = get_file_from_irods(name)
        except SessionException as ex:
            return HttpResponseServerError(ex.stderr)
    else:
        image_base_name = name[:11]
        image_path = RouteImage.objects.get(image_base_name=image_base_name).image_path
        ifile = os.path.join(settings.DATA_ROOT, image_path, name)
        if not os.path.isfile(ifile):
            return HttpResponseServerError(f'{ifile} cannot be found')
    with Image.open(ifile) as im:
        im_resized = im.resize((100, 300))
        buf = io.BytesIO()
        im_resized.save(buf, format='JPEG')
        byte_im = buf.getvalue()
        return HttpResponse(byte_im, content_type='image/jpg')


@login_required
def get_image_names_by_loc(request, long, lat, count):
    count = int(count)
    if count <= 0:
        return JsonResponse({'error': 'count parameter must be greater than 0'},
                            status=status.HTTP_400_BAD_REQUEST)
    in_loc = Point(float(long), float(lat), srid=4326)
    queryset = RouteImage.objects.annotate(
        distance=Distance('location', in_loc)).order_by('distance')[0:count]
    image_list = []
    for q in queryset:
        image_list.append(q.image_base_name)
    return JsonResponse({'image_base_names': list(queryset.values_list('image_base_name', flat=True))},
                        status=status.HTTP_200_OK)


@login_required
def get_image_metadata(request, image_base_name):
    ret_metadata = {}
    obj = RouteImage.objects.filter(image_base_name=image_base_name).first()
    if not obj:
        return JsonResponse({'error': 'the requested image does not exist'}, status=status.HTTP_400_BAD_REQUEST)

    ret_metadata['metadata'] = {
        'image_base_name': image_base_name,
        'route_id': obj.route_id,
        'lat': obj.location.y,
        'long': obj.location.x
    }

    return JsonResponse(ret_metadata, status=status.HTTP_200_OK)


@login_required
def get_image_prediction(request, image_base_name, feature_name):
    ret = {}
    obj = AIImageAnnotation.objects.filter(image__image_base_name=image_base_name,
                                           annotation__name__iexact=feature_name).first()
    if not obj:
        return JsonResponse({'error': 'the requested image does not exist or does not have a prediction'},
                            status=status.HTTP_400_BAD_REQUEST)

    annot_obj = UserImageAnnotation.objects.filter(image__image_base_name=image_base_name,
                                                   annotation__name__iexact=feature_name).first()
    ret['prediction'] = {
        'image_base_name': image_base_name,
        'feature_name': feature_name,
        'probability': obj.certainty,
        'presence': obj.presence if not annot_obj else annot_obj.presence
    }
    return JsonResponse(ret, status=status.HTTP_200_OK)


@login_required
@user_passes_test(lambda u: False if u.is_superuser else True)
def get_next_images_for_annot(request, annot_name, count):
    # return requested <count> number of images sorted by needs for human annotation
    if not AnnotationSet.objects.filter(name__iexact=annot_name).exists():
        return JsonResponse({'error': 'annotation name is not supported'}, status=status.HTTP_400_BAD_REQUEST)

    route_id = request.GET.get('route_id', None)
    offset = request.GET.get('offset', None)
    if offset is not None:
        offset = int(offset)
    count = int(count)
    req_username = request.user.username

    if not AIImageAnnotation.objects.filter(annotation__name__iexact=annot_name).exists() and \
            not UserImageAnnotation.objects.filter(annotation__name__iexact=annot_name).exists():
        # this should not happen since some AI annotations should present, but keep the code here to return some
        # random images for annotation for potential development scenarios where annotation data is not available
        if not route_id:
            images = random.sample(list(RouteImage.objects.filter(set='100').values_list("image_base_name", flat=True)),
                                   count)
        else:
            images = random.sample(list(RouteImage.objects.filter(route_id=route_id).values_list("image_base_name",
                                                                                                 flat=True)), count)

        return JsonResponse({'image_base_names': images}, status=status.HTTP_200_OK)

    images = get_image_base_names_by_annotation(annot_name, req_username, count=count, route_id=route_id, offset=offset)
    if not offset:
        # save the requested images to cache so they will not be sent to a different user later
        save_annot_data_cache(images, req_username, annot_name)
    image_list = [{'base_name': img_base_name, 'aspect_ratio': img_ar} for img_base_name, img_ar in images]
    return JsonResponse({'image_info_list': image_list}, status=status.HTTP_200_OK)


@login_required
def get_all_routes(request):
    route_list = list(RouteImage.objects.values_list("route_id", flat=True).distinct())
    return JsonResponse({'route_ids': route_list}, status=status.HTTP_200_OK)


@login_required
def get_route_info(request, route_id):
    feature_name = request.GET.get('feature_name', None)
    start_image_index = int(request.GET.get('start_image_index', -1))
    end_image_index = int(request.GET.get('end_image_index', -1))
    if start_image_index >= 0 and end_image_index >= 0 and start_image_index >= end_image_index:
        return JsonResponse({"error": "start_image_index parameter must be smaller than end_image_index parameter"},
                            status=status.HTTP_400_BAD_REQUEST)
    image_base_filter = RouteImage.objects.filter(route_id=route_id).order_by('mile_post')
    if not feature_name:
        route_images = list(image_base_filter.values("image_base_name", "mile_post", 'location'))
    else:
        route_images = list(image_base_filter.filter(aiimageannotation__annotation__name=feature_name).values(
            "image_base_name", "mile_post", "location", "aiimageannotation__certainty", "userimageannotation__presence"))
    if start_image_index >= 0 and end_image_index >= 0:
        updated_route_images = route_images[start_image_index:end_image_index]
    elif start_image_index >= 0:
        updated_route_images = route_images[start_image_index:]
    elif end_image_index >= 0:
        updated_route_images = route_images[:end_image_index]
    else:
        updated_route_images = route_images

    for image_dict in route_images:
        image_dict['location'] = {
            'lat': image_dict['location'].y,
            'long': image_dict['location'].x
        }
        if feature_name:
            image_dict['probability'] = image_dict.pop('aiimageannotation__certainty')
            image_dict['presence'] = image_dict.pop('userimageannotation__presence')
            if image_dict['presence'] is None:
                image_dict['presence'] = 'N/A'

    return JsonResponse({'route_image_info': updated_route_images}, status=status.HTTP_200_OK)


@login_required
def get_annotation_set(request):
    annot_list = []
    # for obj in AnnotationSet.objects.all():
    for obj in AnnotationSet.objects.order_by('-name'):
        obj_dict = {}
        obj_dict['name'] = obj.name
        obj_dict['flags'] = list(obj.flags.all().values_list("title", flat=True))
        annot_list.append(obj_dict)
    return JsonResponse({'annotations': annot_list}, status=status.HTTP_200_OK)


@login_required
def get_image_annotations(request, image_base_name):
    ret_annots = {'annotations': []}
    annot_qs = get_image_annotations_queryset(image_base_name=image_base_name)
    for annot in annot_qs:
        annot_dict = {
            'annotation_name': annot
        }
        annot_dict['AI_prediction'] = []
        for ai_annot in AIImageAnnotation.objects.filter(image__image_base_name=image_base_name,
                                                         annotation__name__iexact=annot).order_by('-certainty'):
            annot_dict['AI_prediction'].append({
                'certainty_score': ai_annot.certainty,
                'feature_presence': ai_annot.presence,
                'timestamp': ai_annot.timestamp
            })
        annot_dict['annotator'] = []
        for user_annot in UserImageAnnotation.objects.filter(
                image__image_base_name=image_base_name, annotation__name__iexact=annot):
            annot_dict_entry = {
                'user_name': user_annot.user.username,
                "user_full_name": user_annot.user.get_full_name(),
                'feature_presence': user_annot.presence,
                'timestamp': user_annot.timestamp
            }
            if user_annot.comment:
                annot_dict_entry['comment'] = user_annot.comment
            annot_dict['annotator'].append(annot_dict_entry)

        ret_annots['annotations'].append(annot_dict)
    return JsonResponse(ret_annots, status=status.HTTP_200_OK)


@login_required
def save_annotations(request):
    username = request.user.username
    json_data = json.loads(request.body)
    annotations = json_data.get('annotations', None)
    ret_image_count = json_data.get('return_image_count', 0)
    ret_annot_name = json_data.get('annotation_name', '')
    if annotations is None:
        return JsonResponse({'error': 'no annotations list in the request post'},
                            status=status.HTTP_400_BAD_REQUEST)

    for annot in annotations:
        img_base_name = annot.get('image_base_name', '')
        annot_name = annot.get('annotation_name', '')
        annot_views = annot.get('views', [])
        flags = annot.get('flags', None)
        comments = annot.get('comments', '')
        if not img_base_name or not annot_name or not annot_views:
            return JsonResponse({'error': 'bad request'}, status=status.HTTP_400_BAD_REQUEST)
        if not AnnotationSet.objects.filter(name__iexact=annot_name).exists():
            return JsonResponse({'error': 'annotation name is not supported'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            save_annot_data_to_db(img_base_name, username, annot_name, annot_views, annot_flags=flags,
                                  annot_comments=comments)
        except Exception as ex:
            return JsonResponse({'error': str(ex)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    if ret_image_count > 0 and ret_annot_name:
        # return the next ret_image_count images
        images = get_image_base_names_by_annotation(ret_annot_name, username, count=ret_image_count)
        # save the requested images to cache so they will not be sent to a different user later
        save_annot_data_cache(images, username, ret_annot_name)
    else:
        images = []
    image_list = [{'base_name': img_base_name, 'aspect_ratio': img_ar} for img_base_name, img_ar in images]
    return JsonResponse({'image_info_list': image_list}, status=status.HTTP_200_OK)


@login_required
def get_holdout_test_info(request, annot_name, round_no, category):
    ret_info = {'holdout_test_info': []}
    info_qs = HoldoutTestInfo.objects.filter(annotation__name__iexact=annot_name, round_number=int(round_no),
                                             category=category)
    for info in info_qs:
        info_dict = {
            'image_base_name': info.image.image_base_name,
            'presence': info.presence,
            'in_balance_set': info.in_balance_set,
            'certainty': info.certainty,
            'left_view_certainty': info.left_certainty,
            'front_view_certainty': info.front_certainty,
            'right_view_certainty': info.right_certainty
        }
        ret_info['holdout_test_info'].append(info_dict)
    return JsonResponse(ret_info, status=status.HTTP_200_OK)
