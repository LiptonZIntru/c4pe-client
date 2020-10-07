from django.shortcuts import render, redirect
from django.contrib import messages
import json
import requests
from app.controllers.auth import admin
from django.conf import settings


@admin
def index(request):
    """
    :param request:     Request object
    :return:            HTML page with all users
    """
    users = json.loads(requests.get(settings.API_IP + '/api/users').text)
    return render(request, 'admin/users/index.html',
                  {
                      'users': users
                  })


@admin
def edit(request, id):
    """
    :param request:     Request object
    :param id:          ID of user
    :return:            Update user information and redirect to users
    """
    if request.method == 'GET':
        user = json.loads(requests.get(settings.API_IP + '/api/users/' + id).text)
        return render(request, 'admin/users/edit.html',
                      {
                          'user': user
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


@admin
def reviews(request, id):
    """
    :param request:     Request object
    :param id:          ID of user
    :return:            HTML page with all reviews written by user
    """
    reviews = json.loads(requests.get(settings.API_IP + '/api/users/' + id + '/reviews').text)
    user = json.loads(requests.get(settings.API_IP + '/api/users/' + id).text)
    return render(request, 'admin/users/reviews.html',
                  {
                      'user': user,
                      'reviews': reviews
                  })


@admin
def delete(request, id):
    """
    :param request:     Request object
    :param id:          ID of user
    :return:            Delete user and redirect to users
    """
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


@admin
def delete_avatar(request, id):
    """
    :param request:     Request object
    :param id:          ID of photo
    :return:            Delete photo and redirect to users
    """
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

@admin
def delete_review(request, place_id, review_id):
    """
    :param request:     Request object
    :param place_id:    ID of place
    :param review_id:   ID of review
    :return:            Delete review and redirect to all reviews
    """
    headers = {
        'content-type': 'application/json',
        'Authorization': 'Bearer ' + request.COOKIES['token']
    }
    review = json.loads(requests.get(settings.API_IP + '/api/places/' + place_id + '/Reviews/' + review_id,
                                     headers=headers).text)
    response = requests.delete(settings.API_IP + '/api/places/' + place_id + '/Reviews/' + review_id,
                               headers=headers)
    if response.status_code == 204:
        messages.success(request, 'Review deleted')
    else:
        messages.error(request, 'Unknown error. Please try again')
    return redirect('admin users reviews', id=review['user']['id'])
