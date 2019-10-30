# Generated by Django 2.2.5 on 2019-10-30 22:48

from django.conf import settings
import django.contrib.gis.db.models.fields
import django.contrib.gis.geos.point
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0002_auto_20191009_0136'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='item',
            name='order',
        ),
        migrations.RemoveField(
            model_name='item',
            name='product',
        ),
        migrations.DeleteModel(
            name='Product',
        ),
        migrations.AddField(
            model_name='order',
            name='actual_location',
            field=django.contrib.gis.db.models.fields.PointField(default=django.contrib.gis.geos.point.Point(0, 0), srid=4326),
        ),
        migrations.AddField(
            model_name='order',
            name='delivered',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='order',
            name='end_location',
            field=django.contrib.gis.db.models.fields.PointField(default=django.contrib.gis.geos.point.Point(0, 0), srid=4326),
        ),
        migrations.AddField(
            model_name='order',
            name='price',
            field=models.FloatField(default=0),
        ),
        migrations.AddField(
            model_name='order',
            name='start_location',
            field=django.contrib.gis.db.models.fields.PointField(default=django.contrib.gis.geos.point.Point(0, 0), srid=4326),
        ),
        migrations.AlterField(
            model_name='order',
            name='delivery_user',
            field=models.ForeignKey(limit_choices_to={'is_delivery': True}, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='delivered_orders', to=settings.AUTH_USER_MODEL),
        ),
        migrations.DeleteModel(
            name='Item',
        ),
    ]
