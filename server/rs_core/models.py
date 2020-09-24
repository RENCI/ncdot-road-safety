from django.db import models
from django.contrib.auth.models import User


class UserProfile(models.Model):

    user = models.OneToOneField(User, related_name='user_profile', on_delete=models.CASCADE)
    # cannot use email field in User model in order to guarantee uniqueness of emails at DB level
    email = models.EmailField(unique=True)
    organization = models.CharField(max_length=100)
    years_of_service = models.PositiveIntegerField()

    def __str__(self):
        return self.user.username
