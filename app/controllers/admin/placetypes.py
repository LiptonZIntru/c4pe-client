from django.shortcuts import render, redirect
from django.contrib import messages
import json
import requests
from app.controllers.auth import admin
from django.conf import settings


@admin
def index(request):
    """
    :param request:     Request object
    :return:            HTML page with placetypes
    """
    if request.method == 'GET':
        placeTypes = json.loads(requests.get(settings.API_IP + '/api/placetypes').text)
        return render(request, 'admin/placetypes/index.html',
                      {
                          'placeTypes': placeTypes
                      })
    elif request.method == 'POST':
        headers = {
            'content-type': 'application/json',
            'Authorization': 'Bearer ' + request.COOKIES['token']
        }
        data = {
            "name": request.POST.get('name')
        }
        response = requests.post(settings.API_IP + '/api/placetypes', data=json.dumps(data), headers=headers)
        if response.status_code == 201:
            messages.success(request, 'Place type created')
            return redirect('admin placetypes')
        else:
            messages.error(request, 'Unknown error. Please try again.')
            return redirect('admin placetypes')


@admin
def edit(request, id):
    """
    :param request:     Request object
    :param id:          ID of placetype
    :return:            Update placetype and redirect to placetypes
    """
    if request.method == 'GET':
        placeType = json.loads(requests.get(settings.API_IP + '/api/placetypes/' + id).text)
        return render(request, 'admin/placetypes/edit.html',
                      {
                          'placeType': placeType
                      })
    elif request.method == 'POST':
        headers = {
            'content-type': 'application/json',
            'Authorization': 'Bearer ' + request.COOKIES['token']
        }
        data = {
            "name": request.POST.get("name"),
        }
        response = requests.put(settings.API_IP + '/api/placetypes/' + id, data=json.dumps(data), headers=headers)
        if response.status_code == 204:
            messages.success(request, 'Place type updated')
            return redirect('admin placetypes')
        else:
            messages.error(request, 'Unknown error. Please try again')
            return redirect('admin placetypes edit')


@admin
def delete(request, id):
    """
    :param request:     Request object
    :param id:          ID of placetype
    :return:            Delete placetype and redirect to placetypes
    """
    headers = {
        'content-type': 'application/json',
        'Authorization': 'Bearer ' + request.COOKIES['token']
    }
    response = requests.delete(settings.API_IP + '/api/placetypes/' + id, headers=headers)
    if response.status_code == 204:
        messages.success(request, 'Place type deleted')
    else:
        messages.error(request, 'Unknown error. Please try again')
    return redirect('admin placetypes')
