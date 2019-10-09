import uuid

from django.db import models
from django.utils.encoding import python_2_unicode_compatible

from foodie.users.models import User


@python_2_unicode_compatible
class Order(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    notes = models.CharField(max_length=100, null=True)
    delivery_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="delivered_orders",
                                      limit_choices_to={'is_delivery': True})
    client_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="orders_made",
                                    limit_choices_to={'is_delivery': False})
    date_time_ordered = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.notes

@python_2_unicode_compatible
class Product(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100, null=True)
    description = models.CharField(max_length=100, null=True)
    price = models.FloatField()
    # TODO: this should be the shop class entity
    shop = models.CharField(max_length=100, null=True)

    def __str__(self):
        return self.name


@python_2_unicode_compatible
class Item(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="items")
    quantity = models.IntegerField()
    notes = models.CharField(max_length=100, null=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='+')

    def __str__(self):
        return self.notes
