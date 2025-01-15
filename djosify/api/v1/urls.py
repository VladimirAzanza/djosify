from django.urls import include, path

app_name = 'api_v1'

urlpatterns = [
    path('', include('djoser.urls')),
    path('', include('djoser.urls.jwt')),
]
