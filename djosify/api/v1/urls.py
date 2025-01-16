from django.urls import include, path

from api.v1.users.views import (
    CustomCreateUserViewSet,
    CustomLogoutView,
    CustomProfileUserViewSet,
    CustomTokenRefreshView,
    CustomTokenObtainPairView,
)

app_name = 'api_v1'

urlpatterns = [
    path('register/', CustomCreateUserViewSet.as_view({
        'post': 'create'
    }), name='register'),
    path('me/', CustomProfileUserViewSet.as_view({
        'get': 'me',
        'put': 'me'
    }), name='me'),
    path('login/', CustomTokenObtainPairView.as_view(), name='login'),
    path('refresh/', CustomTokenRefreshView.as_view(), name='refresh'),
    path('logout/', CustomLogoutView.as_view({
        'delete': 'destroy'
    }), name='logout'),
]
