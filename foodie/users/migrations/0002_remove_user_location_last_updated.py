# Generated by Django 2.2.5 on 2019-09-29 23:41

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='location_last_updated',
        ),
    ]
