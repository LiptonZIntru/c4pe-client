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
from django.urls import path
from .controllers import home, places, reviews, users

urlpatterns = [
    # path('', home.index),
    path('example/', home.example),

    path('users/login/', users.login, name='login'),
    path('users/register/', users.register, name='register'),

    path('places/', places.index, name='places'),
    path('places/create/', places.create, name='places.create'),
    path('places/<id>/', places.profile, name='place'),
    path('places/<id>/edit/', places.edit, name='places.edit'),


    path('places/<id>/reviews/', reviews.index, name='reviews'),
]
