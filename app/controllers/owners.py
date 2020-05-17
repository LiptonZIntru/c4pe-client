from django.http import HttpResponse
from django.shortcuts import render, redirect
from .auth import get_user, authorized
from django.contrib import messages
from django.views.decorators.http import require_http_methods
import requests
import json
from datetime import datetime


def index(request, place_id):
    place = json.loads(requests.get('http://77.244.251.110/api/places/' + place_id).text)
    owners_id = place['owners']
    owners = []
    for i in owners_id:
        owners.append(json.loads(requests.get('http://77.244.251.110/api/users/' + str(i['userID'])).text))
    return render(request, 'owners/index.html',
                  {
                      'owners': owners,
                      'currentUser': get_user(request),
                  })
