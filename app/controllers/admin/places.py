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
        size = "999999999"
        headers = {
            'content-type': 'application/json',
            'Authorization': 'Bearer ' + request.COOKIES['token']
        }
        places = json.loads(requests.get(settings.API_IP + '/api/places?PageSize=' + size + '&OrderBy=id',
                                         headers=headers).text)
        return render(request, 'admin/places/index.html',
                      {
                          'places': places
                      })
    else:
        messages.error(request, 'Permission denied')
        return redirect('index')


def create(request):
    if request.method == 'GET':
        types = json.loads(requests.get(settings.API_IP + '/api/placetypes').text)
        return render(request, 'admin/places/create.html',
                      {
                          'types': types
                      })
    elif request.method == 'POST':
        headers = {
            'content-type': 'application/json',
            'Authorization': 'Bearer ' + request.COOKIES['token']
        }
        data = {
            "street": request.POST.get("street"),
            "city": request.POST.get("city"),
            "zipCode": request.POST.get("zipCode"),  # TODO: not required
            "country": request.POST.get("country"),
            "name": request.POST.get("name"),
            "placeTypeID": int(request.POST.get("type"))
        }
        response = requests.post(settings.API_IP + '/api/places', data=json.dumps(data), headers=headers)
        if response.status_code == 201:
            messages.success(request, 'Place created')
            return redirect('admin places')
        else:
            messages.error(request, 'Unknown error. Please try again')
            return redirect('admin places create')


def delete(request, place_id):
    headers = {
        'content-type': 'application/json',
        'Authorization': 'Bearer ' + request.COOKIES['token']
    }
    response = requests.delete(settings.API_IP + '/api/places/' + place_id, headers=headers)
    if response.status_code == 204:
        messages.success(request, 'Place deleted')
    else:
        messages.error(request, 'Unknown error. Please try again')
    return redirect('admin places')


def edit(request, place_id):
    if request.method == 'GET':
        types = json.loads(requests.get(settings.API_IP + '/api/placetypes').text)
        place = json.loads(requests.get(settings.API_IP + '/api/places/' + place_id).text)
        return render(request, 'admin/places/edit.html',
                      {
                          'types': types,
                          'place': place
                      })
    elif request.method == 'POST':
        headers = {
            'content-type': 'application/json',
            'Authorization': 'Bearer ' + request.COOKIES['token']
        }
        data = {
            "street": request.POST.get("street"),
            "city": request.POST.get("city"),
            "zipCode": request.POST.get("zipCode"),
            "country": request.POST.get("country"),
            "name": request.POST.get("name"),
            "placeTypeID": int(request.POST.get("type"))
        }
        response = requests.put(settings.API_IP + '/api/places/' + place_id, data=json.dumps(data), headers=headers)
        if response.status_code == 204:
            messages.success(request, 'Place updated')
            return redirect('admin places')
        else:
            messages.error(request, 'Unknown error. Please try again')
            return redirect('admin place edit')


def reviews(request, place_id):
    if request.method == 'GET':
        reviews = json.loads(requests.get(settings.API_IP + '/api/places/' + place_id + '/reviews').text)
        place = json.loads(requests.get(settings.API_IP + '/api/places/' + place_id).text)
        return render(request, 'admin/places/reviews.html',
                      {
                          'reviews': reviews,
                          'place': place
                      })


def delete_review(request, place_id, review_id):
    if is_admin(request):
        headers = {
            'content-type': 'application/json',
            'Authorization': 'Bearer ' + request.COOKIES['token']
        }
        response = requests.delete(settings.API_IP + '/api/places/' + place_id + '/Reviews/' + review_id,
                                   headers=headers)
        if response.status_code == 204:
            messages.success(request, 'Review deleted')
        else:
            messages.error(request, 'Unknown error. Please try again')
        return redirect('admin places reviews', place_id=place_id)


def delete_avatar(request, id):
    # TODO: delete image of place
    return


def add_avatar(request, id):
    # TODO: add new image
    return

