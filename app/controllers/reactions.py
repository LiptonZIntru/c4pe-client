from django.http import HttpResponse
from django.shortcuts import render, redirect
from .auth import get_user, authorized
from django.contrib import messages
from django.views.decorators.http import require_http_methods
import requests
import json
from datetime import datetime


@require_http_methods(['POST'])
def create(request, place_id, review_id):
    headers = {
        'content-type': 'application/json',
        'Authorization': 'Bearer ' + request.COOKIES['token']
    }
    data = {
        "isHelpful": True
    }
    response = requests.post('http://77.244.251.110/api/places/' + place_id + '/reviews/' + review_id + '/reaction',
                  data=data, headers=headers)
    if response.status_code == 200:
        return "true"
    return HttpResponse(status=400)


@require_http_methods(['POST'])
def delete(request, place_id, review_id):
    headers = {
        'content-type': 'application/json',
        'Authorization': 'Bearer ' + request.COOKIES['token']
    }
    response = requests.delete('http://77.244.251.110/api/places/' + place_id + '/reviews/' + review_id + '/reaction',
                               headers=headers)
    if response.status_code == 200:
        return "true"
    return HttpResponse(status=400)
