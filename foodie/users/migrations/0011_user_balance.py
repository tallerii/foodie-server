# Generated by Django 2.2.5 on 2019-11-07 02:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0010_auto_20191106_2132'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='balance',
            field=models.FloatField(default=0),
        ),
    ]