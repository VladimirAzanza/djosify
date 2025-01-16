from django.urls import include, path
from rest_framework.routers import DefaultRouter


from .views import (
    CustomCreateUserViewSet,
    CustomProfileUserViewSet,
    CustomTokenRefreshView,
    CustomTokenObtainPairView,
)

app_name = 'api_v1'

urlpatterns = [
    path('register/', CustomCreateUserViewSet.as_view({
        'post': 'create'
    }), name='register'),
    path('login/', CustomTokenObtainPairView.as_view(), name='login'),
    path('refresh/', CustomTokenRefreshView.as_view(), name='refresh'),
    path('me/', CustomProfileUserViewSet.as_view({
        'get': 'me'
    }), name='me'),
    path('', include('djoser.urls.jwt')),
]
