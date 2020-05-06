from django.http import HttpResponseNotFound
from django.shortcuts import render, HttpResponse
from django.views.defaults import page_not_found
import json
import requests
from app.controllers.auth import get_user, authorized


def index(request):
    size = "999999999"
    places = json.loads(requests.get('http://77.244.251.110/api/places?PageSize=' + size).text)
    return render(request, 'admin/places/index.html',
                  {
                      'places': places
                  })
