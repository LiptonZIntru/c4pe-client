from django.shortcuts import render, redirect
from django.contrib import messages
import json
import requests
from django.conf import settings
from app.controllers.auth import admin


@admin
def index(request, place_id):
    """
    :param request:     Request object
    :param place_id:    ID of place
    :return:            HTML page with owners
    """
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


@admin
def add_owner(request, place_id):
    """
    :param request:         Request object
    :param place_id:        ID of place
    :return:                Add new owner and redirect to owners
    """
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


@admin
def delete_owner(request, place_id, user_id):
    """
    :param request:         Request object
    :param place_id:        ID of place
    :param user_id:         Owner ID
    :return:                Remove owner and redirect to owners
    """
    if request.method == 'POST':
        headers = {
            'content-type': 'application/json',
            'Authorization': 'Bearer ' + request.COOKIES['token']
        }
        response = requests.delete(settings.API_IP + '/api/places/' + place_id + '/owner/' + user_id, headers=headers)
        if response.status_code == 200:
            messages.success(request, 'Owner removed')
        else:
            messages.error(request, response.text)
        return redirect('admin owners', place_id=place_id)
