from django.http import HttpResponse
from django.shortcuts import render, redirect
from .auth import get_user, authorized
from django.contrib import messages
from django.views.decorators.http import require_http_methods
import requests
import json


def like(request, place_id, review_id):
    headers = {
        'content-type': 'application/json',
        'Authorization': 'Bearer ' + request.COOKIES['token']
    }
    data = {
        "isHelpful": True
    }
    reacted = json.loads(requests.get(
        'http://77.244.251.110/api/places/' + place_id + '/reviews/' + review_id + '/reaction',
        headers=headers).text)
    try:
        if reacted['isHelpful']:
            response = requests.delete(
                'http://77.244.251.110/api/places/' + place_id + '/reviews/' + review_id + '/reaction', headers=headers)
            print(response.status_code)
            if response.status_code == 204:
                return HttpResponse("deleted")
    except:
        pass
    response = requests.post('http://77.244.251.110/api/places/' + place_id + '/reviews/' + review_id + '/reaction',
                             data=json.dumps(data), headers=headers)
    if response.status_code == 200:
        return HttpResponse("liked")
    return HttpResponse(status=400)


def dislike(request, place_id, review_id):
    headers = {
        'content-type': 'application/json',
        'Authorization': 'Bearer ' + request.COOKIES['token']
    }
    data = {
        "isHelpful": False
    }
    reacted = json.loads(requests.get(
        'http://77.244.251.110/api/places/' + place_id + '/reviews/' + review_id + '/reaction',
        headers=headers).text)
    try:
        if not reacted['isHelpful']:
            response = requests.delete(
                'http://77.244.251.110/api/places/' + place_id + '/reviews/' + review_id + '/reaction', headers=headers)
            if response.status_code == 204:
                return HttpResponse("deleted")
    except:
        pass
    response = requests.post('http://77.244.251.110/api/places/' + place_id + '/reviews/' + review_id + '/reaction',
                             data=json.dumps(data), headers=headers)
    if response.status_code == 200:
        return HttpResponse("disliked")
    return HttpResponse(status=400)
