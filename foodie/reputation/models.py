import uuid

from django.db import models
from django.db.models import Q

from foodie.orders.models import Order, DELIVERED_STATUS, DELIVER_ERROR_STATUS
from foodie.users.models import User


class Review(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    notes = models.CharField(max_length=100, null=True)
    value = models.IntegerField()
    # Just one review per user in every order
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='reviews',
                              limit_choices_to=Q(status=DELIVERED_STATUS) | Q(status=DELIVER_ERROR_STATUS))
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reviews')

    def __str__(self):
        return str(self.notes)
