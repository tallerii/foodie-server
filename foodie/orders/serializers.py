from rest_framework import serializers

from foodie.reputation.serializers import ShowReviewSerializer
from foodie.users.serializers import PublicUserSerializer
from .models import Order


class ListOrdersSerializer(serializers.ModelSerializer):
    client_user = PublicUserSerializer(required=False)
    delivery_user = PublicUserSerializer(required=False)
    reviews = ShowReviewSerializer(required=False, many=True)

    class Meta:
        model = Order
        fields = ('id', 'notes', 'delivery_user', 'client_user', 'date_time_ordered', 'delivery_price', 'reviews',
                  'price', 'start_location', 'start_address', 'end_location', 'end_address', 'status')


class CreateOrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ('notes', 'price', 'start_location', 'start_address', 'end_location', 'end_address')
