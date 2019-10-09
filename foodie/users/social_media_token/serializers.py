from rest_framework import serializers

class FacebookTokenSerializer(serializers.Serializer):
    token = serializers.CharField(max_length=4096, required=True, trim_whitespace=True)
