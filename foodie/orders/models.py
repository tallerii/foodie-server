import uuid

from django.contrib.gis.db import models
from django.contrib.gis.geos import Point

from foodie.users.models import User


class Order(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    notes = models.CharField(max_length=100, null=True)
    delivery_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='delivered_orders',
                                      limit_choices_to={'is_delivery': True}, null=True)
    client_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='orders_made',
                                    limit_choices_to={'is_delivery': False})
    delivered = models.BooleanField(default=False)
    date_time_ordered = models.DateTimeField(auto_now_add=True)
    price = models.FloatField(blank=True, null=True)
    start_location = models.PointField(blank=True, null=True)
    end_location = models.PointField(blank=True, null=True)
    actual_location = models.PointField(blank=True, null=True)

    def __str__(self):
        return self.notes
