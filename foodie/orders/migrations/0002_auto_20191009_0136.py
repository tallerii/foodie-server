# Generated by Django 2.2.5 on 2019-10-09 01:36

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='item',
            name='product',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='+', to='orders.Product'),
        ),
        migrations.AlterField(
            model_name='order',
            name='client_user',
            field=models.ForeignKey(limit_choices_to={'is_delivery': False}, on_delete=django.db.models.deletion.CASCADE, related_name='orders_made', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='order',
            name='date_time_ordered',
            field=models.DateTimeField(auto_now_add=True),
        ),
        migrations.AlterField(
            model_name='order',
            name='delivery_user',
            field=models.ForeignKey(limit_choices_to={'is_delivery': True}, on_delete=django.db.models.deletion.CASCADE, related_name='delivered_orders', to=settings.AUTH_USER_MODEL),
        ),
    ]