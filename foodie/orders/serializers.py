from rest_framework_gis.serializers import GeoFeatureModelSerializer
from rest_framework import serializers
from foodie.users.serializers import PublicUserSerializer
from .models import Order


class ListOrdersSerializer(serializers.ModelSerializer):
    client_user = PublicUserSerializer(required=False)
    delivery_user = PublicUserSerializer(required=False)

    class Meta:
        model = Order
        fields = ('id', 'notes', 'delivery_user', 'client_user', 'date_time_ordered', 'delivery_price',
                  'price', 'start_location', 'start_address', 'end_location', 'end_address', 'status')

class CreateOrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ('notes', 'price', 'start_location', 'start_address', 'end_location', 'end_address')
