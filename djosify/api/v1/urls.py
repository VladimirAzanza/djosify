from django.urls import include, path
from rest_framework_simplejwt import views as JWTViews

from .views import CustomCreateUserViewSet

app_name = 'api_v1'

urlpatterns = [
    path('register/', CustomCreateUserViewSet.as_view({
        'post': 'create'
    }), name='register'),
    path('login/', JWTViews.TokenObtainPairView.as_view(), name='login'),
    path('', include('djoser.urls.jwt')),
]
