from django.http import HttpResponseNotFound
from django.shortcuts import render, HttpResponse, redirect
from django.contrib import messages
from django.views.defaults import page_not_found
import json
import requests
from app.controllers.auth import get_user, authorized, is_admin


def index(request):
    if is_admin(request):
        users = json.loads(requests.get('http://77.244.251.110/api/users').text)
        return render(request, 'admin/users/index.html',
                      {
                          'users': users,
                          'currentUser': get_user(request),
                      })
    else:
        messages.error(request, 'Permission denied')
        return redirect('index')


def edit(request, id):
    if request.method == 'GET':
        user = json.loads(requests.get('http://77.244.251.110/api/users/' + id).text)
        userReviews = json.loads(requests.get('http://77.244.251.110/api/users/' + id + '/reviews').text)
        return render(request, 'admin/users/edit.html',
                      {
                          'user': user,
                          'userReviews': userReviews,
                          'currentUser': get_user(request)
                      })
    elif request.method == 'POST':
        headers = {
            'content-type': 'application/json',
            'Authorization': 'Bearer ' + request.COOKIES['token']
        }
        data = {
            "firstName": request.POST.get("firstName"),
            "lastName": request.POST.get("lastName"),
            "description": request.POST.get("description"),
            "street": request.POST.get("street"),
            "city": request.POST.get("city"),
            "zipCode": request.POST.get("zipCode"),
            "country": request.POST.get("country")
        }
        response = requests.put('http://77.244.251.110/api/users/' + id, data=json.dumps(data), headers=headers)
        if response.status_code == 204:
            messages.success(request, 'User profile updated')
            return redirect('admin users')
        else:
            messages.error(request, 'Unknown error. Please try again')
            return redirect('admin users edit')
    return


def delete(request, id):
    headers = {
        'content-type': 'application/json',
        'Authorization': 'Bearer ' + request.COOKIES['token']
    }
    response = requests.delete('http://77.244.251.110/api/users/' + id, headers=headers)
    if response.status_code == 204:
        messages.success(request, 'User deleted')
    else:
        messages.error(request, 'Unknown error. Please try again')
    return redirect('admin users')


def delete_avatar(request, id):
    # TODO: delete user's avatar
    return
