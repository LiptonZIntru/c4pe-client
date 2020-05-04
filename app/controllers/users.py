from django.http import HttpResponse, HttpResponseBadRequest
from django.shortcuts import render, redirect
from django.views.decorators.http import require_http_methods
import requests
import json
from .auth import authorized, get_user


def profile(request, id):
    user = json.loads(requests.get('http://77.244.251.110/api/users/' + id).text)
    return render(request, 'users/index.html',
                  {
                      'user': user,
                      'currentUser': get_user(request)
                  })


def reviews(request, id):
    reviews = json.loads(requests.get('http://77.244.251.110/api/users/' + id + '/reviews').text)
    return render(request, 'users/reviews.html',
                  {
                      'reviews': reviews,
                      'currentUser': get_user(request)  # TODO: vykreslovani reviews
                  })


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
            response = redirect('places')  # TODO: welcome message
            # response = render(request, 'users/login.html')
            response.set_cookie('token', api_response_content['token'])  # user is logged
            request.session['isLogged'] = 1
        else:
            response = render(request, 'users/login.html')  # TODO: message - wrong credentials
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
            return redirect('register')  # TODO: message - return response content
        return redirect('login')  # TODO: message - Registration successful! Please login


def logout(request):
    response = redirect('index')
    if request.session.get('isLogged'):
        del (request.session['isLogged'])
    if request.COOKIES.get('token'):
        response.delete_cookie('token')
    return response  # TODO: message - You have been logged out
