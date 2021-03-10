from django.urls import path, include
from .controllers import home, places, reviews, users, openingtimes, reactions, owners, images

"""
User routes
"""

urlpatterns = [
    path('admin/', include('app.controllers.admin.urls')),

    path('', home.index, name='index'),
    path('about/', home.about, name='about'),
    path('images/', images.serve_images),

    path('users/login/', users.login, name='login'),
    path('users/register/', users.register, name='register'),
    path('users/logout/', users.logout, name='logout'),
    path('users/<id>/image/', users.avatar, name='user avatar'),
    path('users/<id>/image/delete/', users.delete_avatar, name='user avatar delete'),
    path('users/<id>/', users.profile, name='user profile'),
    path('users/<id>/edit', users.edit, name='user edit'),
    path('users/<id>/reviews/', users.reviews, name='user reviews'),


    path('places/', places.index, name='places'),

    path('places/create/', places.create, name='place create'),
    path('places/<id>/', places.profile, name='place profile'),
    path('places/<id>/delete/', places.delete),
    path('places/<id>/edit/', places.edit, name='place edit'),
    path('places/<id>/createreview/', places.create_review, name='places create review'),


    path('places/<id>/reviews/', reviews.index, name='reviews'),
    path('places/<id>/reviews/create/', reviews.create, name='reviews create'),
    path('places/<place_id>/reviews/<id>/edit/', reviews.edit, name='reviews edit'),
    path('places/<place_id>/images/<id>/', places.avatar, name='places image upload'),
    path('places/<place_id>/images/<id>/delete/', places.delete_avatar, name='places image delete'),
    path('places/<place_id>/reviews/<review_id>/like/', reactions.like, name='reaction create'),
    path('places/<place_id>/reviews/<review_id>/dislike/', reactions.dislike, name='reaction delete'),


    path('places/<place_id>/owners/', owners.index, name='owners'),
    path('places/<place_id>/owners/create/', owners.create, name='owners create'),
    path('places/<place_id>/owners/<user_id>/delete/', owners.delete, name='owners delete'),


    path('places/<place_id>/openingtimes/', openingtimes.index, name='openingtimes'),
    path('places/<place_id>/openingtimes/create/', openingtimes.create, name='openingtimes create'),
    path('places/<place_id>/openingtimes/edit/', openingtimes.edit, name='openingtimes edit'),
    path('places/<place_id>/openingtimes/<times_id>/delete/', openingtimes.delete, name='openingtimes delete')
]
