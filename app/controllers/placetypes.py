from django.http import HttpResponse
from django.shortcuts import render, redirect
from .auth import get_user, authorized
import requests
import json


def index(request):
    placetype = json.loads(requests.get('http://77.244.251.110/api/placetypes').text)
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
        response = requests.post('http://77.244.251.110/api/placetypes', data=json.dumps(data), headers=headers)
        if response.status_code == 201:
            return redirect('placetypes')  # TODO: place type added
        else:
            return render(request, 'placetypes/create.html',  # TODO: form validation error
                          {
                              'currentUser': get_user(request)
                          })


def edit(request, id):
    """
        TODO: admin route
    """
    if request.method == 'GET':
        placetype = json.loads(requests.get('http://77.244.251.110/api/placetypes/' + id).text)
        return render(request, 'placetypes/edit.html',
                      {
                          'placetype': placetype,
                          'currentUser': get_user(request)
                      })
    elif request.method == 'POST':
        data = {
            'id': int(id),
            'name': request.POST.get('name')
        }
        headers = {
            'content-type': 'application/json',
            'Authorization': 'Bearer ' + request.COOKIES['token']
        }
        response = requests.put('http://77.244.251.110/api/placetypes/' + id, data=json.dumps(data), headers=headers)
        if response.status_code == 201:
            return redirect('placetypes')  # TODO: place type saved
        else:
            return render(request, 'placetypes/edit.html',  # TODO: form validation error
                          {
                              'currentUser': get_user(request)
                          })
