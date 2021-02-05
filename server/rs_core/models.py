from django.contrib.gis.db import models
from django.contrib.auth.models import User


class UserProfile(models.Model):
    user = models.OneToOneField(User, related_name='user_profile', on_delete=models.CASCADE)
    # cannot use email field in User model in order to guarantee uniqueness of emails at DB level
    email = models.EmailField(unique=True)
    organization = models.CharField(max_length=100)
    years_of_service = models.PositiveIntegerField()

    def __str__(self):
        return self.user.username


class RouteImage(models.Model):
    route_id = models.CharField(max_length=20, db_index=True)
    # 8 digit number string with first 2 digit representing hour (00 or 01), next 2 digit
    # representing minute (00 to 59), next 2 digit representing second (00 to 59), and the
    # last 2 digit representing frame number (max of 29)
    # The file name can be created using set number and image_base_name as <set><image_base_name><1,2,5>.jpg
    image_base_name = models.CharField(max_length=15, primary_key=True)
    mile_post = models.FloatField(blank=True, null=True)
    location = models.PointField()
    image_path = models.CharField(max_length=100, default='')


class AnnotationSet(models.Model):
    TYPE_CHOICES = (
        ('pt', 'Point'),
        ('cont', 'Continuous')
    )
    name = models.CharField(max_length=100, primary_key=True)
    type = models.CharField(max_length=10, choices=TYPE_CHOICES, default='pt')


class AIImageAnnotation(models.Model):
    image = models.ForeignKey(RouteImage, on_delete=models.CASCADE)
    annotation = models.ForeignKey(AnnotationSet, on_delete=models.CASCADE)
    presence = models.BooleanField()
    certainty = models.FloatField()
    uncertainty_measure = models.IntegerField(null=True, blank=True)
    uncertainty_group = models.IntegerField(null=True, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        indexes = [
            models.Index(fields=['image', 'annotation']),
            models.Index(fields=['annotation', 'uncertainty_group', '-uncertainty_measure', 'image']),
        ]
        unique_together = ('image', 'annotation')
        # ordering = ['-uncertainty_measure', 'image__image_base_name']


class UserImageAnnotation(models.Model):
    image = models.ForeignKey(RouteImage, on_delete=models.CASCADE)
    annotation = models.ForeignKey(AnnotationSet, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    presence = models.BooleanField()
    presence_views = models.CharField(max_length=10, null=True, blank=True, default='')
    flag = models.BooleanField(default=False)
    timestamp = models.DateTimeField(auto_now_add=True)
    comment = models.CharField(max_length=1000, blank=True, null=True)

    class Meta:
        indexes = [
            models.Index(fields=['image', 'annotation']),
        ]
        unique_together = ('user', 'image', 'annotation')
