from django.http import HttpResponseNotFound
from django.shortcuts import render, HttpResponse
from django.views.defaults import page_not_found
import json
import requests
from .auth import get_user


# Create your views here.


def example(request):
    #  For testing
    return render(request, 'example.html')


def urls(request):
    return render(request, 'urls.html',
                  {
                      'currentUser': get_user(request)
                  })


def index(request):
    response = json.loads(requests.get('http://77.244.251.110/api/stats').text)
    return render(request, 'home/index.html',
                  {
                      'places': response['amountPlaces'],
                      'users': response['amountUsers'],
                      'reviews': response['amountReviews'],
                      'currentUser': get_user(request)
                  })


def about(request):
    return render(request, 'home/about.html',
                  {
                      'currentUser': get_user(request)
                  })
