from django.contrib.auth import get_user_model
from djoser.views import UserViewSet as DjoserUserViewSet
from rest_framework import status
from rest_framework_simplejwt import views as JWTViews

from users.models import UserRefreshToken

User = get_user_model()

class CustomCreateUserViewSet(DjoserUserViewSet):
    pass


class CustomTokenObtainPairView(JWTViews.TokenObtainPairView):
    # update nombres tokens"
    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        if response.status_code == status.HTTP_200_OK:
            refresh_token = response.data.get('refresh')
            user = User.objects.get(email=request.data.get('email'))
            UserRefreshToken.objects.update_or_create(
                user=user,
                defaults={'refresh_token': refresh_token}
            )
        return response
