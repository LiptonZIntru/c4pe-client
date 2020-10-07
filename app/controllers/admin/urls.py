from django.urls import path
from . import home, places, users, placetypes, owners, openingtimes

"""
Admin routes
"""

urlpatterns = [
    path('', home.index, name='admin index'),
    path('places/', places.index, name='admin places'),
    path('places/create/', places.create, name='admin places create'),
    path('places/<place_id>/edit/', places.edit, name='admin places edit'),
    path('places/<place_id>/delete/', places.delete, name='admin places delete'),
    path('places/<place_id>/reviews/', places.reviews, name='admin places reviews'),
    path('places/<place_id>/reviews/<review_id>/delete/', places.delete_review, name='admin places reviews delete'),
    path('places/<place_id>/openingtimes/', openingtimes.index, name='admin openingtimes'),
    path('places/<place_id>/openingtimes/create/', openingtimes.create, name='admin openingtimes create'),
    path('places/<place_id>/openingtimes/edit/', openingtimes.edit, name='admin openingtimes edit'),
    path('places/<place_id>/openingtimes/<times_id>/delete/', openingtimes.delete, name='admin openingtimes delete'),
    path('places/<place_id>/owners/', owners.index, name='admin owners'),
    path('places/<place_id>/owners/create/', owners.add_owner, name='admin owners create'),
    path('places/<place_id>/owners/<user_id>/delete/', owners.delete_owner, name='admin owners delete'),
    path('places/<place_id>/images/<id>/delete', places.delete_avatar),

    path('placetypes/', placetypes.index, name='admin placetypes'),
    path('placetypes/<id>/edit/', placetypes.edit, name='admin placetypes edit'),
    path('placetypes/<id>/delete/', placetypes.delete, name='admin placetypes delete'),

    path('users/', users.index, name='admin users'),
    path('users/<id>/edit/', users.edit, name='admin users edit'),
    path('users/<id>/avatar/delete', users.delete_avatar, name='admin users avatar delete'),
    path('users/<id>/reviews/', users.reviews, name='admin users reviews'),
    path('users/<place_id>/reviews/<review_id>/delete/', users.delete_review, name='admin users reviews delete'),
    path('users/<id>/delete/', users.delete, name='admin users delete'),
]