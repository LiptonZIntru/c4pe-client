from django.contrib import admin
from django.urls import path
from . import home, places, users, placetypes

urlpatterns = [
    path('', home.index, name='admin index'),
    path('places/', places.index, name='admin places'),
    path('places/create/', places.create, name='admin places create'),
    path('places/<place_id>/edit/', places.edit, name='admin places edit'),
    path('places/<place_id>/delete/', places.delete, name='admin places delete'),

    path('placetypes/', placetypes.index, name='admin placetypes'),
    path('placetypes/create/', placetypes.create, name='admin placetypes create'),
    path('placetypes/<id>/edit/', placetypes.edit, name='admin placetypes edit'),
    path('placetypes/<id>/delete/', placetypes.delete, name='admin placetypes delete'),

    path('users/', users.index, name='admin users'),
    path('users/<id>/edit/', users.edit, name='admin users edit'),
    path('users/<id>/reviews/', users.reviews, name='admin users reviews'),
    path('users/<id>/delete/', users.delete, name='admin users delete'),
]