from django.http import HttpResponse
from django.shortcuts import render
import requests
import json


def index(request, id):
    print(id)
    reviews = json.loads(requests.get('http://77.244.251.110/api/places/' + id + '/Reviews').text)
    return render(request, 'test/reviews/index.html', {'reviews': reviews})
