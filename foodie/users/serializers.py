from rest_framework import serializers
from rest_framework_gis.serializers import GeoFeatureModelSerializer

from .models import User


class PrivateUserSerializer(GeoFeatureModelSerializer):

    class Meta:
        model = User
        geo_field = 'last_location'

        fields = ('id', 'username', 'avatar', 'first_name', 'last_name', 'email', 'balance',
                  'phone_number', 'is_premium', 'is_delivery', 'reputation',
                  'location_last_updated', 'FCMToken')
        read_only_fields = ('username', 'is_premium', 'reputation', 'balance', 'location_last_updated')


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


class PasswordResetSerializer(serializers.Serializer):
    recuperation_token = serializers.CharField()
    password = serializers.CharField()

    def validate(self, attrs):
        recuperation_token = attrs.get('recuperation_token')

        try:
            user = User.objects.get(recuperation_token=recuperation_token)
        except User.DoesNotExist:
            raise serializers.ValidationError('Invalid recuperation token.')

        attrs['user'] = user
        return attrs


class PasswordRecuperationSerializer(serializers.Serializer):
    email = serializers.EmailField()

    def validate(self, attrs):
        email = attrs.get('email')

        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            raise serializers.ValidationError('User with the provided email does not exist.')

        attrs['user'] = user
        return attrs
