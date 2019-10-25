from rest_framework import serializers
from rest_framework_gis.fields import GeometryField
from rest_framework_gis.serializers import GeoFeatureModelSerializer

from .models import Order


class OrderSerializer(serializers.ModelSerializer):
    start_location = GeometryField()
    end_location = GeometryField()
    actual_location = GeometryField()

    class Meta:
        model = Order
        fields = ('id', 'notes', 'date_time_ordered', 'start_location', 'end_location', 'actual_location')
        read_only_fields = ('delivery_user', 'date_time_ordered',
                            'delivered', 'price', 'client_user')
