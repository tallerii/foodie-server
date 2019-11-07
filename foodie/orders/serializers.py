from rest_framework_gis.serializers import GeoFeatureModelSerializer
from rest_framework import serializers
from foodie.users.serializers import PublicUserSerializer
from .models import Order


class ListOrdersSerializer(GeoFeatureModelSerializer):
    client_user = PublicUserSerializer(required=False)
    delivery_user = PublicUserSerializer(required=False)

    class Meta:
        model = Order
        geo_field = 'actual_location'

        fields = ('id', 'notes', 'delivery_user', 'client_user', 'date_time_ordered', 'delivery_price',
                  'price', 'start_location', 'end_location', 'actual_location', 'status')


class CreateOrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ('notes', 'price', 'start_location', 'end_location')
