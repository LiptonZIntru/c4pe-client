from django.shortcuts import render, HttpResponse
import json
import requests
from .auth import validate


# Create your views here.


def example(request):
    #  For testing
    #  return render(request, 'example.html')
    return HttpResponse(str(request.session.get('isLogged')) + ", " + str(request.COOKIES['token']))


def urls(request):
    return render(request, 'urls.html')


def index(request):
    response = json.loads(requests.get('http://77.244.251.110/api/stats').text)
    return render(request, 'home/index.html',
                  {
                      'places': response['amountPlaces'],
                      'users': response['amountUsers'],
                      'reviews': response['amountReviews']
                  })


def about(request):
    return render(request, 'home/about.html')
