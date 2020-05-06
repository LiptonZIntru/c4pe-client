from django.http import HttpResponseNotFound
from django.shortcuts import render, HttpResponse, redirect
from django.views.defaults import page_not_found
from django.contrib import messages
import json
import requests
from app.controllers.auth import get_user, authorized, is_admin


def index(request):
    if is_admin(request):
        placeTypes = json.loads(requests.get('http://77.244.251.110/api/placetypes').text)
        return render(request, 'admin/placetypes/index.html',
                      {
                          'places': placeTypes,
                          'currentUser': get_user(request),
                      })
    else:
        messages.error(request, 'Permission denied')
        return redirect('index')
