# Generated by Django 2.2.5 on 2019-11-07 02:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0009_auto_20191106_2306'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='delivery_price',
            field=models.FloatField(blank=True, null=True),
        ),
    ]
