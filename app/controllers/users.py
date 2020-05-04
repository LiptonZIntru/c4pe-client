from django.http import HttpResponse, HttpResponseBadRequest
from django.shortcuts import render, redirect
from django.views.decorators.http import require_http_methods
import requests
import json
from .auth import validate


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
        api_response = requests.post('http://77.244.251.110/api/users/login', data=json.dumps(data), headers=headers)

        api_response_content = json.loads(api_response.text)
        if api_response.status_code == 200:
            response = HttpResponse('logged')
            # response = render(request, 'users/login.html')
            response.set_cookie('token', api_response_content['token'])  # with user is logged
            request.session['isLogged'] = 1
        else:
            response = render(request, 'users/login.html')  # wrong credentials
        return response


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
            return render(request, 'users/register.html')
        return render(request, 'users/login.html')


def logout(request):
    del(request.session['isLogged'])
    del(request.session['token'])
    return render(request, 'home/index.html')