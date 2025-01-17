from rest_framework.exceptions import ValidationError
from users.models import UserRefreshToken

from .exceptions import CustomInvalidTokenException


def get_user_refresh_token(refresh_token):
    """Retrieves a UserRefreshToken instance using the provided refresh token.

    Arguments:
        refresh_token(str): The refresh token to search it in the database.

    Returns:
        UserRefreshToken: UserRefreshToken instance
    """
    return UserRefreshToken.objects.get(
        refresh_token=refresh_token
    )


def validate_jwt_token(serializer):
    """Validates the JWT token using the provided serializer

    Arguments:
        serializer (Serializer): The serializer to validate the JWT token.

    Raises:
        CustomInvalidTokenException: If the JWT token is invalid.

    Returns:
        str: The new refresh token if validation is successful.
    """
    try:
        serializer.is_valid(raise_exception=True)
        return serializer.validated_data.get('refresh')
    except ValidationError:
        raise CustomInvalidTokenException()


def validate_refresh_token_in_db(refresh_token):
    """Validates whether the provided refresh token exists in the database.

    Arguments:
        refresh_token (str): The refresh token to check in the database.

    Raises:
        CustomInvalidTokenException: If the refresh token does not exist in
        the database.

    Returns:
        UserRefreshToken: The matching UserRefreshToken instance.
    """
    try:
        user_refresh_token = get_user_refresh_token(refresh_token)
        return user_refresh_token
    except UserRefreshToken.DoesNotExist:
        raise CustomInvalidTokenException()
