from django.http import HttpResponseNotFound
from django.shortcuts import render, HttpResponse, redirect
from django.contrib import messages
from django.views.defaults import page_not_found
import json
import requests
from app.controllers.auth import get_user, authorized, is_admin
from django.conf import settings


def index(request, place_id):
    if request.method == 'GET':
        place = json.loads(requests.get(settings.API_IP + '/api/places/' + place_id).text)
        owners_id = place['owners']
        owners = []
        for i in owners_id:
            owners.append(json.loads(requests.get(settings.API_IP + '/api/users/' + str(i['userID'])).text))
        return render(request, 'admin/places/owners.html',
                      {
                          'place': place,
                          'owners': owners
                      })


def add_owner(request, place_id):
    if request.method == 'POST':
        username = request.POST.get('username')
        headers = {
            'content-type': 'application/json',
            'Authorization': 'Bearer ' + request.COOKIES['token']
        }
        data = {
            'username': username
        }

        response = requests.post(settings.API_IP + '/api/places/' + place_id + '/owner', data=json.dumps(data),
                                 headers=headers)
        if response.status_code == 200:
            messages.success(request, 'Owner added')
        else:
            messages.error(request, response.text)
        return redirect('admin owners', place_id=place_id)


def delete_owner(request, place_id, user_id):
    if request.method == 'POST':
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
        return redirect('admin owners', place_id=place_id)