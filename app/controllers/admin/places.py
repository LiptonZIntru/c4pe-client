from django.http import HttpResponseNotFound
from django.shortcuts import render, HttpResponse, redirect
from django.contrib import messages
from django.views.defaults import page_not_found
import json
import requests
from app.controllers.auth import get_user, authorized, is_admin


def index(request):
    if is_admin(request):
        size = "999999999"
        places = json.loads(requests.get('http://77.244.251.110/api/places?PageSize=' + size).text)
        return render(request, 'admin/places/index.html',
                      {
                          'places': places,
                          'currentUser': get_user(request),
                      })
    else:
        messages.error(request, 'Permission denied')
        return redirect('index')


def create(request):
    # TODO: create new place
    return


def edit(request, id):
    # TODO: edit existing place
    return


def delete_avatar(request, id):
    # TODO: delete image of place
    return


def add_avatar(request, id):
    # TODO: add new image
    return


def add_owner(request, id):
    # TODO: add new owner
    return
