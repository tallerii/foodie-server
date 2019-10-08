from rest_framework import serializers
from .models import User


class PrivateUserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('id', 'username', 'avatar', 'first_name', 'last_name', 'email',
                  'phone_number', 'is_premium', 'is_delivery', 'reputation',
                  'lat', 'lon', 'location_last_updated')
        read_only_fields = ('username', 'is_premium', 'reputation', 'location_last_updated')


class PublicUserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('id', 'username', 'avatar', 'first_name', 'last_name', 'is_premium',
                  'is_delivery', 'reputation', 'lat', 'lon', 'location_last_updated')


class CreateUserSerializer(serializers.ModelSerializer):

    def create(self, validated_data):
        # call create_user on user object. Without this
        # the password will be stored in plain text.
        user = User.objects.create_user(**validated_data)
        return user

    class Meta:
        model = User
        fields = ('id', 'username', 'password', 'avatar', 'first_name', 'last_name', 'email',
                  'phone_number')
        extra_kwargs = {'password': {'write_only': True}}

class PasswordSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('password',)
        extra_kwargs = {'password': {'write_only': True}}

