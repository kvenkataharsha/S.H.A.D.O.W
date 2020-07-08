from django.urls import path
from . import views

urlpatterns = [
    path('api1', views.api, name='api'),
]