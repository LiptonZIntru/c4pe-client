from django.http import HttpResponseNotFound
from django.shortcuts import render, HttpResponse, redirect
from django.contrib import messages
from django.views.defaults import page_not_found
import json
import requests
from app.controllers.auth import get_user, authorized, is_admin
from django.conf import settings


def index(request):
    if is_admin(request):
        users = json.loads(requests.get(settings.API_IP + '/api/users').text)
        return render(request, 'admin/users/index.html',
                      {
                          'users': users
                      })
    else:
        messages.error(request, 'Permission denied')
        return redirect('index')


def edit(request, id):
    if request.method == 'GET':
        user = json.loads(requests.get(settings.API_IP + '/api/users/' + id).text)
        userReviews = json.loads(requests.get(settings.API_IP + '/api/users/' + id + '/reviews').text)
        return render(request, 'admin/users/edit.html',
                      {
                          'user': user,
                          'userReviews': userReviews
                      })
    elif request.method == 'POST':
        headers = {
            'content-type': 'application/json',
            'Authorization': 'Bearer ' + request.COOKIES['token']
        }
        data = {
            "username": request.POST.get("username"),
            "firstName": request.POST.get("firstName"),
            "lastName": request.POST.get("lastName"),
            "description": request.POST.get("description"),
            "country": request.POST.get("country"),
            "isVerified": bool(request.POST.get("isVerified"))
        }
        response = requests.put(settings.API_IP + '/api/users/' + id, data=json.dumps(data), headers=headers)
        if response.status_code == 204:
            messages.success(request, 'User profile updated')
            return redirect('admin users')
        else:
            messages.error(request, 'Unknown error. Please try again')
            return redirect('admin users edit', id=id)
    return


def reviews(request, id):
    if is_admin(request):
        reviews = json.loads(requests.get(settings.API_IP + '/api/users/' + id + '/reviews').text)
        user = json.loads(requests.get(settings.API_IP + '/api/users/' + id).text)
        return render(request, 'admin/users/reviews.html',
                      {
                          'user': user,
                          'reviews': reviews
                      })
    else:
        messages.error(request, 'Permission denied')
        return redirect('index')


def delete(request, id):
    headers = {
        'content-type': 'application/json',
        'Authorization': 'Bearer ' + request.COOKIES['token']
    }
    response = requests.delete(settings.API_IP + '/api/users/' + id, headers=headers)
    if response.status_code == 204:
        messages.success(request, 'User deleted')
    else:
        messages.error(request, 'Unknown error. Please try again')
    return redirect('admin users')


def delete_avatar(request, id):
    headers = {
        'content-type': 'application/json',
        'Authorization': 'Bearer ' + request.COOKIES['token']
    }
    data = {
        "avatarURI": ""
    }
    response = requests.put(settings.API_IP + '/api/users/' + id, data=json.dumps(data), headers=headers)
    if response.status_code == 204:
        messages.success(request, 'User avatar deleted')
        return redirect('admin users edit', id=id)
    else:
        messages.error(request, 'Unknown error. Please try again.')
        return redirect('admin users edit', id=id)
