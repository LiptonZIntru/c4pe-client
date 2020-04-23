from django.shortcuts import render
import json
import requests


# Create your views here.


def example(request):
    return render(request, 'example.html')


def index(request):
    places = json.loads(requests.get('http://77.244.251.110/api/places').headers['X-pagination'])['TotalCount']
    users = len(json.loads(requests.get('http://77.244.251.110/api/users').text))
    reviews = 96
    return render(request, 'home/index.html', {'places': places, 'users': users, 'reviews': reviews})
