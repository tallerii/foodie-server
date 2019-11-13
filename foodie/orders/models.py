import uuid

from django.contrib.gis.db import models

from foodie.users.models import User

UNASSIGNED_STATUS = "unassigned"
IN_PROGRESS_STATUS = "in_progress"
DELIVERED_STATUS = "delivered"
DELIVER_ERROR_STATUS = "deliver_error"
POSSIBLE_STATUS = [(UNASSIGNED_STATUS, UNASSIGNED_STATUS), (IN_PROGRESS_STATUS, IN_PROGRESS_STATUS),
                   (DELIVERED_STATUS, DELIVERED_STATUS), (DELIVER_ERROR_STATUS, DELIVER_ERROR_STATUS)]


class Order(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    notes = models.CharField(max_length=100, null=True)
    delivery_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='delivered_orders',
                                      limit_choices_to={'is_delivery': True}, null=True, default=None)
    client_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='orders_made',
                                    limit_choices_to={'is_delivery': False})
    status = models.CharField(choices=POSSIBLE_STATUS, default=UNASSIGNED_STATUS, max_length=100)
    date_time_ordered = models.DateTimeField(auto_now_add=True)
    price = models.FloatField(blank=True, null=True)
    delivery_price = models.FloatField(blank=True, null=True)
    start_location = models.PointField(blank=True, null=True)
    end_location = models.PointField(blank=True, null=True)
    actual_location = models.PointField(blank=True, null=True)

    def __str__(self):
        return str(self.notes)
