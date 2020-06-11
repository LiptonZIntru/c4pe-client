from django.http import HttpResponseNotFound
from django.shortcuts import render, HttpResponse, redirect
from django.views.defaults import page_not_found
from django.contrib import messages
import json
import requests
from app.controllers.auth import admin
from django.conf import settings


@admin
def index(request):
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
