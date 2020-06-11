from django.http import HttpResponse
from django.shortcuts import render, redirect
from .auth import authorized, get_user, login_required
from django.contrib import messages
from django.views.decorators.http import require_http_methods
import requests
import json
from datetime import datetime
from django.conf import settings


@login_required
def index(request, place_id):
    place = json.loads(requests.get(settings.API_IP + '/api/places/' + place_id).text)
    owners_id = place['owners']
    owners = []
    for i in owners_id:
        owners.append(json.loads(requests.get(settings.API_IP + '/api/users/' + str(i['userID'])).text))
    return render(request, 'owners/index.html',
                  {
                      'place': place,
                      'owners': owners
                  })


@login_required
@require_http_methods(['POST'])
def create(request, place_id):
    username = request.POST.get('username')
    headers = {
        'content-type': 'application/json',
        'Authorization': 'Bearer ' + request.COOKIES['token']
    }
    data = {
        'username': username
    }

    response = requests.post(settings.API_IP + '/api/places/' + place_id + '/owner', data=json.dumps(data), headers=headers)
    if response.status_code == 200:
        messages.success(request, 'Owner added')
    else:
        messages.error(request, response.text)
    return redirect('owners', place_id=place_id)


@login_required
@require_http_methods(['POST'])
def delete(request, place_id, user_id):
    headers = {
        'content-type': 'application/json',
        'Authorization': 'Bearer ' + request.COOKIES['token']
    }
    response = requests.delete(settings.API_IP + '/api/places/' + place_id + '/owner/' + user_id, headers=headers)
    print(response.text)
    if response.status_code == 200:
        messages.success(request, 'Owner removed')
    else:
        messages.error(request, response.text)
    return redirect('owners', place_id=place_id)
