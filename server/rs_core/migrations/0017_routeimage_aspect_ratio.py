# Generated by Django 3.1.8 on 2021-04-27 20:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rs_core', '0016_auto_20210414_2348'),
    ]

    operations = [
        migrations.AddField(
            model_name='routeimage',
            name='aspect_ratio',
            field=models.FloatField(blank=True, null=True),
        ),
    ]
