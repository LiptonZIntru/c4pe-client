from django.contrib import admin
from django.urls import path
from . import home, places, users, placetypes

urlpatterns = [
    path('', home.index, name='admin index'),
    path('places/', places.index, name='admin places'),
    path('places/<place_id>/delete', places.delete, name='admin places delete'),
    path('placetypes/', placetypes.index, name='admin placetypes'),
    path('users/', users.index, name='admin users'),
]