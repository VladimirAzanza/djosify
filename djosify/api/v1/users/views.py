from django.contrib.auth import get_user_model
from djoser.views import UserViewSet as DjoserUserViewSet
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework_simplejwt import views as JWTViews
from rest_framework_simplejwt.exceptions import TokenError as JWTTokenError

from .exceptions import CustomInvalidTokenException
from .utils import (
    get_user_refresh_token,
    validate_jwt_token,
    validate_refresh_token_in_db
)
from djosify.constants import (
    NO_REFRESH_TOKEN_RESPONSE,
    SUCCESS_LOGOUT_RESPONSE
)
from users.models import UserRefreshToken

User = get_user_model()


class CustomCreateUserViewSet(DjoserUserViewSet):
    """Viewset for users creation, extending from Djoser's UserViewSet."""
    pass


class CustomProfileUserViewSet(DjoserUserViewSet):
    """Custom viewset for managing the me/ and logout/ endpoint."""

    @action(methods=['get', 'put'], detail=False)
    def me(self, request, *args, **kwargs):
        """Retrieve or update the logged-in user's profile."""
        return super().me(request, *args, **kwargs)

    @action(methods=['post'], detail=False)
    def logout(self, request, *args, **kwargs):
        """Log out the user by deleting their refresh token."""
        refresh_token = request.data.get('refresh_token')
        if not refresh_token:
            return Response(
                NO_REFRESH_TOKEN_RESPONSE, status=status.HTTP_400_BAD_REQUEST
            )
        try:
            user_refresh_token = get_user_refresh_token(refresh_token)
            user_refresh_token.delete()
            return Response(
                SUCCESS_LOGOUT_RESPONSE, status=status.HTTP_200_OK
            )
        except (UserRefreshToken.DoesNotExist, JWTTokenError, Exception):
            raise CustomInvalidTokenException()


class CustomTokenObtainPairView(JWTViews.TokenObtainPairView):
    """Custom view for obtaining access and refresh JSon Web Tokens."""

    def post(self, request, *args, **kwargs):
        """Override the default 'post' method to add refresh token storage.

        - Stores the refresh token in the 'UserRefreshToken' model upon
        successful login.
        - Returns the 'access_token' and 'refresh_token' to the client.
        """
        response = super().post(request, *args, **kwargs)
        if response.status_code == status.HTTP_200_OK:
            refresh_token = response.data.get('refresh')
            user = User.objects.get(email=request.data.get('email'))
            UserRefreshToken.objects.update_or_create(
                user=user,
                defaults={'refresh_token': refresh_token}
            )
            response.data['refresh_token'] = response.data.pop('refresh')
            response.data['access_token'] = response.data.pop('access')
        return response


class CustomTokenRefreshView(JWTViews.TokenRefreshView):
    """Custom view for refreshing JWT tokens."""

    def post(self, request, *args, **kwargs):
        """Override the default 'post' method to add token validation and
        handling.

        - Accepts a 'refresh_token' in the request body.
        - Validates the refresh token with the JWT serializer and the database.
        - Returns a new 'access_token' and 'refresh_token'.
        """
        if 'refresh_token' in request.data:
            request.data['refresh'] = request.data.pop('refresh_token')
        serializer = self.get_serializer(data=request.data)
        new_refresh_token = validate_jwt_token(serializer)
        refresh_token_in_db = validate_refresh_token_in_db(
                request.data['refresh']
            )
        user = refresh_token_in_db.user
        UserRefreshToken.objects.update_or_create(
            user=user,
            defaults={'refresh_token': new_refresh_token}
        )
        custom_response = {
            'access_token': serializer.validated_data.get('access'),
            'refresh_token': new_refresh_token,
        }
        return Response(custom_response, status=status.HTTP_200_OK)
