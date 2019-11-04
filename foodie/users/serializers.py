from rest_framework import serializers
from rest_framework_gis.serializers import GeoFeatureModelSerializer

from .models import User


class PrivateUserSerializer(GeoFeatureModelSerializer):

    class Meta:
        model = User
        geo_field = 'last_location'

        fields = ('id', 'username', 'avatar', 'first_name', 'last_name', 'email',
                  'phone_number', 'is_premium', 'is_delivery', 'reputation',
                  'location_last_updated', 'FCMToken')
        read_only_fields = ('username', 'is_premium', 'reputation', 'location_last_updated')


class PublicUserSerializer(GeoFeatureModelSerializer):

    class Meta:
        model = User
        geo_field = 'last_location'

        fields = ('id', 'username', 'avatar', 'first_name', 'last_name', 'is_premium',
                  'is_delivery', 'reputation', 'location_last_updated', 'FCMToken')


class CreateUserSerializer(GeoFeatureModelSerializer):

    def create(self, validated_data):
        # call create_user on user object. Without this
        # the password will be stored in plain text.
        user = User.objects.create_user(**validated_data)
        return user

    class Meta:
        model = User
        geo_field = 'last_location'
        fields = ('id', 'username', 'password', 'avatar', 'first_name', 'last_name', 'email',
                  'phone_number', 'FCMToken')
        extra_kwargs = {'password': {'write_only': True}}


class PasswordSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('password',)
        extra_kwargs = {'password': {'write_only': True}}
