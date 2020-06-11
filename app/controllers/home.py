from django.http import HttpResponseNotFound
from django.shortcuts import render, HttpResponse
from django.views.defaults import page_not_found
import json
import requests
from django.conf import settings

# Create your views here.


def example(request):
    #  For testing
    return render(request, 'example.html')


def urls(request):
    return render(request, 'urls.html')


def index(request):
    response = json.loads(requests.get(settings.API_IP + '/api/stats').text)
    return render(request, 'home/index.html',
                  {
                      'places': response['amountPlaces'],
                      'users': response['amountUsers'],
                      'reviews': response['amountReviews']
                  })


def about(request):
    return render(request, 'home/about.html')


def test(request):
    response = json.loads(requests.get(settings.API_IP + '/api/stats').text)
    return render(request, 'karel/index.html',
                  {
                      'places': response['amountPlaces'],
                      'users': response['amountUsers'],
                      'reviews': response['amountReviews']
                  })