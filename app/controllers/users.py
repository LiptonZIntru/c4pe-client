from django.http import HttpResponse, HttpResponseBadRequest
from django.shortcuts import render, redirect
import requests
import json


def index(request, id):
    user = json.loads(requests.get('http://77.244.251.110/api/users/' + id).text)
    return render(request, 'users/index.html', {'user': user})


def reviews(request, id):
    user = json.loads(requests.get('http://77.244.251.110/api/users/' + id).text)
    return render(request, 'users/reviews.html', {'user': user})


def login(request):
    if request.method == 'GET':
        return render(request, 'users/login.html')
    elif request.method == 'POST':
        data = {
            'username': request.POST.get('username'),
            'password': request.POST.get('password')
        }
        headers = {
            'content-type': 'application/json'
        }
        response = requests.post('http://77.244.251.110/api/users/login', data=json.dumps(data), headers=headers)
        print(json.loads(response.text)['token'])
        # pls nevypisuj ten token priste
        return HttpResponse('status code: ' + str(response.status_code) + '<br>token: ' + json.loads(response.text)['token'])


def register(request):
    if request.method == 'GET':
        return render(request, 'users/register.html')
    elif request.method == 'POST':
        data = {
            'username': request.POST.get('username'),
            'password': request.POST.get('password'),
            'firstName': request.POST.get('firstName'),
            'lastName': request.POST.get('lastName'),
            'description': request.POST.get('description'),
            'street': request.POST.get('street'),
            'city': request.POST.get('city'),
            'country': request.POST.get('country')
        }
        headers = {
            'content-type': 'application/json'
        }

        response = requests.post('http://77.244.251.110/api/users/register', data=json.dumps(data), headers=headers)
        if not response.status_code == 201:
            print(response.status_code)
            return HttpResponse(response.status_code)
        return HttpResponse('logged')
