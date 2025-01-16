from rest_framework.exceptions import ValidationError
from users.models import UserRefreshToken

from .exceptions import CustomInvalidTokenException


def get_user_refresh_token(refresh_token):
    return UserRefreshToken.objects.get(
        refresh_token=refresh_token
    )


def validate_jwt_token(serializer):
    try:
        serializer.is_valid(raise_exception=True)
        return serializer.validated_data.get('refresh')
    except ValidationError:
        raise CustomInvalidTokenException()


def validate_refresh_token_in_db(refresh_token):
    try:
        user_refresh_token = get_user_refresh_token(refresh_token)
        return user_refresh_token
    except UserRefreshToken.DoesNotExist:
        raise CustomInvalidTokenException()
