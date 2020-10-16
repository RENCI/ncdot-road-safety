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
    route_id = models.CharField(max_length=20)
    # 1 set contains around 100 miles or roughly 2 hours of collected data
    set = models.CharField(max_length=5)
    # 8 digit number string with first 2 digit representing hour (00 or 01), next 2 digit
    # representing minute (00 to 59), next 2 digit representing second (00 to 59), and the
    # last 2 digit representing frame number (max of 29)
    # The file name can be created using set number and image_base_name as <set><image_base_name><1,2,5>.jpg
    image_base_name = models.CharField(max_length=15, primary_key=True)
    location = models.PointField()

    def __str__(self):
        return "{}{}".format(self.set, self.image_base_name)


class AnnotationSet(models.Model):
    TYPE_CHOICES = (
        ('pt', 'Point'),
        ('cont', 'Continuous')
    )
    name = models.CharField(max_length=100, primary_key=True)
    type = models.CharField(max_length=10, choices=TYPE_CHOICES, default='pt')


class ImageAnnotation(models.Model):
    image = models.ForeignKey(RouteImage, on_delete=models.CASCADE)
    annotation = models.ForeignKey(AnnotationSet, on_delete=models.CASCADE)
    pred_centainty_score = models.FloatField(default=-1)
    pred_timestamp = models.DateTimeField(blank=True, null=True)
    annotator = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
    feature_present = models.BooleanField(blank=True, null=True)
    annotator_timestamp = models.DateTimeField(blank=True, null=True)
    comment = models.CharField(max_length=1000, blank=True, null=True)

    class Meta:
        unique_together = ('image', 'annotation', 'annotator')
