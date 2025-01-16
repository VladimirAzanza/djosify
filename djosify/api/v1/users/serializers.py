from djoser.serializers import UserSerializer


class CustomUserSerializer(UserSerializer):
    class Meta(UserSerializer.Meta):
        fields = (
            'id',
            'username',
            'email',
        )
