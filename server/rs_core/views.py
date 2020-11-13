import os
import json
import random
from datetime import timezone, datetime

from django.db import transaction
from django.contrib.auth.views import PasswordResetView, LogoutView
from django.contrib.auth import login, authenticate
from django.forms.models import inlineformset_factory
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.db import IntegrityError
from django.contrib import messages
from django.conf import settings
from django.contrib.messages import info
from django.utils.translation import ugettext_lazy as _
from django.core.mail import send_mail
from django.http import HttpResponse, HttpResponseForbidden, HttpResponseRedirect, \
    HttpResponseServerError, JsonResponse

from django_irods.storage import IrodsStorage
from django_irods.icommands import SessionException
from django.contrib.gis.db.models.functions import Distance
from django.contrib.gis.geos import Point
from rest_framework import status

from rs_core.forms import SignupForm, UserProfileForm, UserPasswordResetForm
from rs_core.models import UserProfile, RouteImage, AnnotationSet, AIImageAnnotation, UserImageAnnotation
from rs_core.utils import get_image_base_names_by_annotation, get_image_annotations_queryset


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

            new_user = User.objects.create_user(username, first_name=firstname,
                                                last_name=lastname,
                                                password=raw_pwd,
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
def get_image_by_name(request, name):
    istorage = IrodsStorage()
    image_path = os.path.join(settings.IRODS_ROOT, 'images')
    if not os.path.exists(image_path):
        os.makedirs(image_path)
    ifile = os.path.join(image_path, name)
    if not os.path.isfile(ifile):
        try:
            dest_path = istorage.get_one_image_frame(name, image_path)
            ifile = os.path.join(dest_path, name)
        except SessionException as ex:
            return HttpResponseServerError(ex.stderr)

    return HttpResponse(open(ifile, 'rb'), content_type='image/jpg')


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
def get_image_base_names_by_annot(request, annot_name):
    if not AnnotationSet.objects.filter(name__iexact=annot_name).exists():
        return JsonResponse({'error': 'annotation name is not supported'}, status=status.HTTP_400_BAD_REQUEST)
    if not AIImageAnnotation.objects.filter(annotation__name__iexact=annot_name).exists() and \
            not UserImageAnnotation.objects.filter(annotation__name__iexact=annot_name).exists():
        return JsonResponse({'image_base_names': []}, status=status.HTTP_200_OK)

    route_id = request.GET.get('route_id', None)
    images = get_image_base_names_by_annotation(annot_name, route_id)
    return JsonResponse({'image_base_names': images}, status=status.HTTP_200_OK)


@login_required
def get_next_images_for_annot(request, annot_name, count):
    # return requested <count> number of images sorted by needs for human annotation
    if not AnnotationSet.objects.filter(name__iexact=annot_name).exists():
        return JsonResponse({'error': 'annotation name is not supported'}, status=status.HTTP_400_BAD_REQUEST)

    route_id = request.GET.get('route_id', None)
    count = int(count)

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

    images = get_image_base_names_by_annotation(annot_name, count, route_id)
    return JsonResponse({'image_base_names': images}, status=status.HTTP_200_OK)


@login_required
def get_all_routes(request):
    route_list = list(RouteImage.objects.values_list("route_id", flat=True).distinct())
    return JsonResponse({'route_ids': route_list}, status=status.HTTP_200_OK)


@login_required
def get_route_info(request, route_id):
    route_images = list(RouteImage.objects.filter(route_id=route_id).values_list("image_base_name", flat=True))
    return JsonResponse({'route_image_base_names': route_images}, status=status.HTTP_200_OK)


@login_required
def get_annotation_set(request):
    annotation_list = list(AnnotationSet.objects.all().values_list("name", flat=True))
    return JsonResponse({'annotation_names': annotation_list}, status=status.HTTP_200_OK)


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
    annotations = json_data.get('annotations')
    if annotations is None:
        return JsonResponse({'error': 'no annotations list in the request post'},
                            status=status.HTTP_400_BAD_REQUEST)

    for annot in annotations:
        img_base_name = annot.get('image_base_name', '')
        annot_name = annot.get('annotation_name', '')
        annot_present = annot.get('is_present', None)
        annot_present_views = annot.get('is_present_views', [])
        annot_comment = annot.get('comment', '')
        if not img_base_name or not annot_name or annot_present is None:
            return JsonResponse({'error': 'bad request'}, status=status.HTTP_400_BAD_REQUEST)
        if not AnnotationSet.objects.filter(name__iexact=annot_name).exists():
            return JsonResponse({'error': 'annotation name is not supported'}, status=status.HTTP_400_BAD_REQUEST)
        if annot_present_views:
            annot_present_view_str = ','.join([str(x) for x in annot_present_views])
        else:
            annot_present_view_str = ''
        try:
            with transaction.atomic():
                obj = UserImageAnnotation(image=RouteImage.objects.get(image_base_name=img_base_name),
                                          annotation=AnnotationSet.objects.get(name__iexact=annot_name),
                                          user=User.objects.get(username=username),
                                          presence=annot_present,
                                          presence_views=annot_present_views,
                                          comment=annot_comment)
                obj.save()
        except Exception as ex:
            return JsonResponse({'error': str(ex)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    return JsonResponse({'message': 'annotations saved successfully'}, status=status.HTTP_200_OK)
