from django.http import HttpResponseNotFound
from django.shortcuts import render, HttpResponse
from django.views.defaults import page_not_found
import json
import requests
from django.conf import settings


def index(request):
    """
    :param request:
    :return: HTML page available on "/"
    """
    response = json.loads(requests.get(settings.API_IP + '/api/stats').text)
    return render(request, 'home/index.html',
                  {
                      'places': response['amountPlaces'],
                      'users': response['amountUsers'],
                      'reviews': response['amountReviews']
                  })


def about(request):
    """
    :param request:
    :return: HTML page available on "/about"
    """
    return render(request, 'home/about.html')
