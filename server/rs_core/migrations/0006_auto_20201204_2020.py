# Generated by Django 3.1.1 on 2020-12-04 20:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rs_core', '0005_routeimage_mile_post'),
    ]

    operations = [
        migrations.RemoveIndex(
            model_name='routeimage',
            name='rs_core_rou_image_b_eff58f_idx',
        ),
        migrations.RemoveField(
            model_name='routeimage',
            name='set',
        ),
        migrations.AddIndex(
            model_name='routeimage',
            index=models.Index(fields=['route_id', 'image_base_name'], name='rs_core_rou_route_i_b54be0_idx'),
        ),
    ]
