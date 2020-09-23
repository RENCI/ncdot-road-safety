from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User


class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    organization = forms.CharField(max_length=100, required=True)
    yrs_of_serv = forms.IntegerField(required=True, help_text='Years of experience in roadway safety')

    class Meta(UserCreationForm):
        model = User
        fields = ['first_name', 'last_name', "username", "email", "organization", "yrs_of_serv",
                  "password1", "password2"]
