from rest_framework_gis.serializers import GeoFeatureModelSerializer

from foodie.users.serializers import PublicUserSerializer
from .models import Order


class ListOrdersSerializer(GeoFeatureModelSerializer):
    client_user = PublicUserSerializer(required=False)
    delivery_user = PublicUserSerializer(required=False)

    class Meta:
        model = Order
        geo_field = 'actual_location'

        fields = ('id', 'notes', 'delivery_user', 'client_user', 'date_time_ordered',
                  'price', 'start_location', 'end_location', 'actual_location')
        read_only_fields = ('delivery_user', 'client_user', 'delivered', 'date_time_ordered', 'status',
                            'actual_location')


class ActivateOrdersSerializer(GeoFeatureModelSerializer):
    client_user = PublicUserSerializer(required=False)
    delivery_user = PublicUserSerializer(required=False)

    class Meta:
        model = Order
        geo_field = 'actual_location'
        fields = ('id', 'notes', 'delivery_user', 'client_user', 'date_time_ordered',
                  'price', 'start_location', 'end_location', 'actual_location', 'status')
        read_only_fields = ('id', 'notes', 'delivery_user', 'client_user', 'date_time_ordered',
                            'price', 'start_location', 'end_location', 'actual_location', 'status')
