from django.contrib.auth import authenticate

from rest_framework import serializers

class FacebookTokenSerializer(serializers.Serializer):
    token = serializers.CharField(max_length=4096, required=True, trim_whitespace=True)
    FCMToken = serializers.CharField(max_length=300, required=True, trim_whitespace=True)

    def validate(self, attrs):
        token = attrs.get('token')
        FCMToken = attrs.get('FCMToken')

        if token:
            user = authenticate(request=self.context.get('request'), token=token, FCMToken=FCMToken)

            if not user:
                msg = 'Provided token didn\'t correspond to a facbook user with required permissions'
                raise serializers.ValidationError(msg, code='authorization')
        else:
            raise serializers.ValidationError('Must include "token".', code='authorization')

        attrs['user'] = user
        return attrs
