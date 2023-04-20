
from django.urls import path
from . import views
from .views import RegisterAPI

app_name = 'authentication'


urlpatterns = [
    path('api/register/', RegisterAPI.as_view(), name='register'),
]