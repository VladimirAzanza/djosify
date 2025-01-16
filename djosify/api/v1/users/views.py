from django.contrib.auth import get_user_model
from djoser.views import UserViewSet as DjoserUserViewSet
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework_simplejwt import views as JWTViews
from rest_framework_simplejwt.exceptions import TokenError as JWTTokenError
from rest_framework_simplejwt.serializers import TokenRefreshSerializer

from .exceptions import CustomInvalidTokenException
from users.models import UserRefreshToken

User = get_user_model()


class CustomCreateUserViewSet(DjoserUserViewSet):
    pass


class CustomProfileUserViewSet(DjoserUserViewSet):
    @action(methods=['get', 'put'], detail=False)
    def me(self, request, *args, **kwargs):
        return super().me(request, *args, **kwargs)

    @action(methods=['post'], detail=False)
    def logout(self, request, *args, **kwargs):
        refresh_token = request.data.get('refresh_token')
        if not refresh_token:
            return Response(
                {"refresh_token": "This field is required"},
                status=status.HTTP_400_BAD_REQUEST
            )
        try:
            user_refresh_token = UserRefreshToken.objects.get(
                refresh_token=refresh_token
            )
            user_refresh_token.delete()
            return Response(
                {"success": "User logged out."},
                status=status.HTTP_200_OK
            )
        except (UserRefreshToken.DoesNotExist, JWTTokenError, Exception):
            raise CustomInvalidTokenException()


class CustomTokenObtainPairView(JWTViews.TokenObtainPairView):
    def post(self, request, *args, **kwargs):
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
    def post(self, request, *args, **kwargs):
        if 'refresh_token' in request.data:
            request.data['refresh'] = request.data.pop('refresh_token')
        serializer = self.get_serializer(data=request.data)

        try:
            serializer.is_valid(raise_exception=True)
        except JWTTokenError:
            raise CustomInvalidTokenException()
        validated_data = serializer.validated_data
        new_refresh_token = validated_data.get('refresh')

        try:
            user_refresh_token = UserRefreshToken.objects.get(
                refresh_token=request.data['refresh']
            )
            user = user_refresh_token.user
        except UserRefreshToken.DoesNotExist:
            raise CustomInvalidTokenException()

        UserRefreshToken.objects.update_or_create(
            user=user,
            defaults={'refresh_token': new_refresh_token}
        )
        custom_response = {
            'access_token': validated_data.get('access'),
            'refresh_token': new_refresh_token,
        }
        return Response(custom_response, status=status.HTTP_200_OK)
