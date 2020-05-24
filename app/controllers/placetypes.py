from django.http import HttpResponse
from django.shortcuts import render, redirect
from .auth import get_user, authorized
from django.contrib import messages
import requests
import json
from django.conf import settings


def index(request):
    placetype = json.loads(requests.get(settings.API_IP + '/api/placetypes').text)
    return render(request, 'placetypes/index.html',
                  {
                      'placetypes': placetype,
                      'currentUser': get_user(request)
                  })


def create(request):
    """
        TODO: admin route
    """
    if request.method == 'GET':
        return render(request, 'placetypes/create.html',
                      {
                          'currentUser': get_user(request)
                      })
    elif request.method == 'POST':
        data = {
            'name': request.POST.get('name')
        }
        headers = {
            'content-type': 'application/json',
            'Authorization': 'Bearer ' + request.COOKIES['token']
        }
        response = requests.post(settings.API_IP + '/api/placetypes', data=json.dumps(data), headers=headers)
        if response.status_code == 201:
            messages.success(request, 'Place type added')
            return redirect('placetypes')
        else:
            messages.error(request, 'Unknown error. Please try again')
            return render(request, 'placetypes/create.html',  # TODO: form validation error
                          {
                              'currentUser': get_user(request)
                          })


def edit(request, id):
    """
        TODO: admin route
    """
    if request.method == 'GET':
        placetype = json.loads(requests.get(settings.API_IP + '/api/placetypes/' + id).text)
        return render(request, 'placetypes/edit.html',
                      {
                          'placetype': placetype,
                          'currentUser': get_user(request)
                      })
    elif request.method == 'POST':
        data = {
            'name': request.POST.get('name')
        }
        headers = {
            'content-type': 'application/json',
            'Authorization': 'Bearer ' + request.COOKIES['token']
        }
        response = requests.put(settings.API_IP + '/api/placetypes/' + id, data=json.dumps(data), headers=headers)
        if response.status_code == 204:
            messages.success(request, 'Place type updated')
            return redirect('placetypes')
        else:
            messages.error(request, 'Unknown error. Please try again')
            return render(request, 'placetypes/edit.html',  # TODO: form validation error
                          {
                              'currentUser': get_user(request)
                          })
