from django.urls import path
from . import views

app_name = 'database'

urlpatterns = [
    path('', views.index, name='index')
]