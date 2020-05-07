from django.http import HttpResponseNotFound
from django.shortcuts import render, HttpResponse, redirect
from django.contrib import messages
from django.views.defaults import page_not_found
import json
import requests
from app.controllers.auth import get_user, authorized, is_admin


def index(request):
    response = json.loads(requests.get('http://77.244.251.110/api/stats').text)
    if is_admin(request):
        return render(request, 'admin/home/index.html',
                      {
                          'places': response['amountPlaces'],
                          'users': response['amountUsers'],
                          'reviews': response['amountReviews'],
                          'currentUser': get_user(request)
                      })
    else:
        messages.error(request, 'Permission denied')
        return redirect('index')
