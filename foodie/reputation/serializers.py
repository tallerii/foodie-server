from rest_framework_gis.serializers import GeoFeatureModelSerializer
from rest_framework import serializers

from foodie.orders.serializers import ListOrdersSerializer
from foodie.users.serializers import PublicUserSerializer
from .models import Order, Review


class ListReviewSerializer(serializers.ModelSerializer):
    user = PublicUserSerializer()
    order = ListOrdersSerializer()

    class Meta:
        model = Review
        fields = ('id', 'notes', 'value', 'order', 'user')
        read_only = ('id', 'order', 'user')


class CreateReviewSerializer(serializers.ModelSerializer):
    def validate_value(self, value):
        if value not in range(1, 6):
            raise serializers.ValidationError("Value not in range 1-5")
        return value

    def validate(self, data):
        if data['user'].pk not in [data['order'].client_user_id, data['order'].delivery_user_id]:
            raise serializers.ValidationError("Review must be for users in the order")
        if Review.objects.filter(user=data['user'], order=data['order'].pk).count() > 0:
            raise serializers.ValidationError("Review already registered for this user and order")
        return data

    class Meta:
        model = Review
        fields = ('id', 'notes', 'value', 'order', 'user')
