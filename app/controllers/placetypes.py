from django.http import HttpResponse
from django.shortcuts import render, redirect
import requests
import json

token = 'eyJhbGciOiJIUzUxMiIsInR5cCI6IkpXVCJ9.eyJuYW1laWQiOiI3IiwidW5pcXVlX25hbWUiOiJ2aWxpIiwibmJmIjoxNTg3MTMwMzc4LCJleHAiOjE1ODcyMTY3NzgsImlhdCI6MTU4NzEzMDM3OH0.ker5TIH4LwAMK5qNnrDSKb3eS05PuUads0UjD0t74HU2kYV53LOdVFIqHtNlbrlMfvk3swkDfp3LycIhQ_JQcg'


def index(request):
    placetype = json.loads(requests.get('http://77.244.251.110/api/placetypes').text)
    return render(request, 'placetypes/index.html', {'placetypes': placetype})


def create(request):
    if request.method == 'GET':
        return render(request, 'placetypes/create.html')
    elif request.method == 'POST':
        data = {
            'name': request.POST.get('name')
        }
        headers = {
            'content-type': 'application/json',
            'Authorization': 'Bearer ' + token
        }
        response = requests.post('http://77.244.251.110/api/placetypes', data=json.dumps(data), headers=headers)
        return HttpResponse('status code: ' + str(response.status_code))


def edit(request, id):
    if request.method == 'GET':
        placetype = json.loads(requests.get('http://77.244.251.110/api/placetypes/' + id).text)
        return render(request, 'placetypes/edit.html', {'placetype': placetype})
    elif request.method == 'POST':
        data = {
            'id': int(id),
            'name': request.POST.get('name')
        }
        headers = {
            'content-type': 'application/json',
            'Authorization': 'Bearer ' + token
        }
        response = requests.put('http://77.244.251.110/api/placetypes/' + id, data=json.dumps(data), headers=headers)
        return HttpResponse('status code: ' + str(response.status_code))
