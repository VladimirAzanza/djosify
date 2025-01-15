from django.urls import include, path

from .views import CustomCreateUserViewSet

app_name = 'api_v1'

urlpatterns = [
    path('register/', CustomCreateUserViewSet.as_view({
        'post': 'create'
    }), name='register'),
    path('', include('djoser.urls.jwt')),
]
