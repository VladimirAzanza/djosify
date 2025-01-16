from djoser.serializers import UserSerializer
from rest_framework import serializers


class CustomUserSerializer(UserSerializer):
    class Meta(UserSerializer.Meta):
        fields = (
            'id',
            'username',
            'email',
        )
