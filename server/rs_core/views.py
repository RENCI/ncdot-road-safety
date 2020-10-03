import os
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
from rs_core.models import UserProfile, RouteImage


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
def get_image_names_by_loc(request, long, lat, direction, count):
    dir = direction.lower()
    if dir == 'front':
        code = 1
    elif dir == 'left':
        code = 2
    elif dir == 'right':
        code = 5
    elif dir == 'rear':
        code = 6
    else:
        return JsonResponse({'error': 'direction parameter must be front, left, or right'},
                            status=status.HTTP_400_BAD_REQUEST)
    count = int(count)
    if count <= 0:
        return JsonResponse({'error': 'count parameter must be greater than 0'},
                            status=status.HTTP_400_BAD_REQUEST)
    in_loc = Point(float(long), float(lat), srid=4326)
    queryset = RouteImage.objects.annotate(
        distance=Distance('location', in_loc)).order_by('distance')[0:count]
    image_list = []
    for q in queryset:
        image_list.append('{}{}{}.jpg'.format(q.set, q.image_base_name, code))
    return JsonResponse({'image_file_names': image_list}, status=status.HTTP_200_OK)
