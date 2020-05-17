"""c4pe URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path ,include
from .controllers import home, places, reviews, users, placetypes, openingtimes, reactions

urlpatterns = [
    path('admin/', include('app.controllers.admin.urls')),

    path('example/', home.example),
    path('urls/', home.urls),
    path('test/', home.test),

    path('', home.index, name='index'),
    path('about/', home.about, name='about'),

    path('users/login/', users.login, name='login'),
    path('users/register/', users.register, name='register'),
    path('users/logout/', users.logout, name='logout'),
    path('users/avatar/', users.avatar, name='user avatar'),
    path('users/<id>/', users.profile, name='user profile'),
    path('users/<id>/edit', users.edit, name='user edit'),
    path('users/<id>/reviews/', users.reviews, name='user reviews'),


    path('places/', places.index, name='places'),
    path('places/create/', places.create, name='place create '),
    path('places/<id>/', places.profile, name='place profile'),
    path('places/<id>/edit/', places.edit, name='place edit'),
    path('places/<id>/createreview/', places.create_review, name='places create review'),


    path('places/<id>/reviews/', reviews.index, name='reviews'),
    path('places/<id>/reviews/create/', reviews.create, name='reviews create'),
    path('places/<place_id>/reviews/<id>/edit/', reviews.edit, name='reviews edit'),
    path('places/<place_id>/reviews/<review_id>/like', reactions.create, name='reaction create'),
    path('places/<place_id>/reviews/<review_id>/dislike', reactions.delete, name='reaction delete'),


    # get positive/negative/all reviews in json
    path('places/<id>/reviews/type/<type>/', places.get_json_reviews, name='reviews specific type'),


    path('placetypes/', placetypes.index, name='placetypes'),
    path('placetypes/create/', placetypes.create, name='placetype create'),
    path('placetypes/<id>/edit/', placetypes.edit, name='placetype edit'),


    path('places/<place_id>/openingtimes/', openingtimes.index, name='openingtimes'),
    path('places/<place_id>/openingtimes/create/', openingtimes.create, name='openingtimes create'),
    path('places/<place_id>/openingtimes/edit/', openingtimes.edit, name='openingtimes edit'),
]
