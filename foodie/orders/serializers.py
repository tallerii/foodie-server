from rest_framework import serializers
from rest_framework_gis.serializers import GeoFeatureModelSerializer
from rest_framework_gis.serializers import GeometryField

from .models import Order


class ListOrdersSerializer(GeoFeatureModelSerializer):
    class Meta:
        model = Order
        geo_field = 'actual_location'

        fields = ('id', 'notes', 'delivery_user', 'client_user', 'date_time_ordered',
                  'price', 'start_location', 'end_location', 'actual_location')
        read_only_fields = ('delivery_user', 'client_user', 'delivered', 'date_time_ordered', 'status',
                            'actual_location')


class ActivateOrdersSerializer(GeoFeatureModelSerializer):
    class Meta:
        model = Order
        geo_field = 'actual_location'
        fields = ('id', 'notes', 'delivery_user', 'client_user', 'date_time_ordered',
                  'price', 'start_location', 'end_location', 'actual_location', 'status')
        read_only_fields = ('id', 'notes', 'delivery_user', 'client_user', 'date_time_ordered',
                            'price', 'start_location', 'end_location', 'actual_location', 'status')
