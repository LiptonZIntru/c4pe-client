from django.http import HttpResponse, HttpResponseBadRequest
from django.shortcuts import render, redirect
from django.views.decorators.http import require_http_methods
from django.contrib import messages
import requests
import json
from .auth import authorized, get_user
from django.conf import settings


def profile(request, id):
    headers = {
        'Authorization': 'Bearer ' + str(request.COOKIES.get('token'))
    }
    user = json.loads(requests.get(settings.API_IP + '/api/users/' + id).text)

    if request.COOKIES.get('token'):
        me = json.loads(requests.get(settings.API_IP + '/api/users/me', headers=headers).text)
        if user['id'] == me['id']:
            user = me

    reviews = json.loads(requests.get(settings.API_IP + '/api/users/' + id + '/reviews').text)
    best = ""
    if reviews:
        best = reviews[0]
        for review in reviews:
            if review['positiveReactions'] > best['positiveReactions']:
                best = review
    return render(request, 'users/index.html',
                  {
                      'user': user,
                      'review': best
                  })


def reviews(request, id):
    reviews = json.loads(requests.get(settings.API_IP + '/api/users/' + id + '/reviews').text)
    user = json.loads(requests.get(settings.API_IP + '/api/users/' + id).text)

# SERAZENI PODLE NEJVICE LAJKOVANYCH
    def get_positive_reactions(review):
        return review.get('positiveReactions')

    reviews.sort(key=get_positive_reactions, reverse=True)
# KONEC SEKCE

    return render(request, 'users/reviews.html',
                  {
                      'user': user,
                      'reviews': reviews
                  })


def edit(request, id):
    if request.method == 'GET':
        user = json.loads(requests.get(settings.API_IP + '/api/users/' + id).text)
        return render(request, 'users/edit.html',
                      {
                          'user': user,
                      })
    elif request.method == 'POST':
        data = {
            'username': request.POST.get('username'),
            'password': request.POST.get('password'),
            'firstName': request.POST.get('firstName'),
            'lastName': request.POST.get('lastName'),
            'description': request.POST.get('description'),
            'street': request.POST.get('street'),
            'city': request.POST.get('city'),
            'zipCode': request.POST.get('zipCode'),
            'country': request.POST.get('country')
        }
        headers = {
            'content-type': 'application/json',
            'Authorization': 'Bearer ' + request.COOKIES['token']
        }
        response = requests.put(settings.API_IP + '/api/users/me', data=json.dumps(data), headers=headers)

        if request.FILES.get('avatar'):
            avatar(request, id)

        if response.status_code == 204:
            messages.success(request, 'Profile updated')
            return redirect('user profile', id=id)
        else:
            messages.error(request, 'Unknown error. Please try again')
            return redirect('user profile', id=id)  # TODO: form validation error


# @require_http_methods('POST')

def avatar(request, id):
    if request.method == 'GET':
        return render(request, 'users/avatar.html')
    elif request.method == 'POST':
        avatar_file = request.FILES.get('avatar')
        file = open('app/static/upload/image.jpg', 'wb+')
        for chunk in avatar_file.chunks():
            file.write(chunk)
        headers = {
            'Authorization': 'Bearer ' + request.COOKIES['token']
        }
        data = {
            "image": open(r'app/static/upload/image.jpg', 'rb')
        }
        response = requests.post(settings.API_IP + '/api/users/me/avatar', files=data, headers=headers)
        if response.status_code == 200:
            messages.success(request, 'Avatar uploaded')
        else:
            messages.error(request, response.text)
        return redirect('user profile', id=id)


def delete_avatar(request, id):
    headers = {
        'Authorization': 'Bearer ' + request.COOKIES['token']
    }
    response = requests.delete(settings.API_IP + '/api/users/me/avatar', headers=headers)
    if response.status_code == 200:
        messages.success(request, 'Avatar deleted')
    else:
        messages.error(request, response.text)
    return redirect('user profile', id=id)


def login(request):
    if request.method == 'GET':
        if authorized(request.COOKIES.get('token')) == 200:
            return redirect('places')
        else:
            return render(request, 'users/login.html')
    elif request.method == 'POST':
        data = {
            'username': request.POST.get('username'),
            'password': request.POST.get('password')
        }
        headers = {
            'content-type': 'application/json'
        }
        api_response = requests.post(settings.API_IP + '/api/users/login', data=json.dumps(data), headers=headers)

        api_response_content = json.loads(api_response.text)
        if api_response.status_code == 200:
            response = redirect('places')
            messages.success(request, 'Welcome back!')
            response.set_cookie('token', api_response_content['token'])  # user is logged
            request.session['isLogged'] = 1
        else:
            messages.error(request, 'Wrong credentials!')
            response = render(request, 'users/login.html')
        return response


def register(request):
    if request.method == 'GET':
        if authorized(request.COOKIES.get('token')) == 200:
            return redirect('places')
        else:
            return render(request, 'users/register.html')
    elif request.method == 'POST':
        data = {
            'username': request.POST.get('username'),
            'password': request.POST.get('password'),
            'firstName': request.POST.get('firstName'),
            'lastName': request.POST.get('lastName'),
            'description': request.POST.get('description'),
            "street": request.POST.get('street'),
            "city": request.POST.get('city'),
            "zipCode": request.POST.get('zipCode'),
            'country': request.POST.get('country')
        }
        headers = {
            'content-type': 'application/json'
        }

        response = requests.post(settings.API_IP + '/api/users/register', data=json.dumps(data), headers=headers)
        if not response.status_code == 201:
            messages.error(request, response.text)
            return redirect('register')  # TODO: message - return response content
        messages.success(request, 'Registration was successful! Please login here')
        return redirect('login')


def logout(request):
    response = redirect('index')
    if request.session.get('isLogged'):
        del (request.session['isLogged'])
    if request.COOKIES.get('token'):
        response.delete_cookie('token')
    messages.success(request, 'You have been logged out')
    return response
