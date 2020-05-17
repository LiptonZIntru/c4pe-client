from django.http import HttpResponseNotFound
from django.shortcuts import render, HttpResponse, redirect
from django.contrib import messages
from django.views.defaults import page_not_found
import json
import requests
from app.controllers.auth import get_user, authorized, is_admin


def index(request):
    if is_admin(request):
        size = "999999999"
        headers = {
            'content-type': 'application/json',
            'Authorization': 'Bearer ' + request.COOKIES['token']
        }
        places = json.loads(requests.get('http://77.244.251.110/api/places?PageSize=' + size + '&OrderBy=id',
                                         headers=headers).text)
        return render(request, 'admin/places/index.html',
                      {
                          'places': places,
                          'currentUser': get_user(request),
                      })
    else:
        messages.error(request, 'Permission denied')
        return redirect('index')


def create(request):
    if request.method == 'GET':
        types = json.loads(requests.get('http://77.244.251.110/api/placetypes').text)
        return render(request, 'admin/places/create.html',
                      {
                          'types': types,
                          'currentUser': get_user(request),
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
        response = requests.post('http://77.244.251.110/api/places', data=json.dumps(data), headers=headers)
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
    response =requests.delete('http://77.244.251.110/api/places/' + place_id, headers=headers)
    print(response.status_code)
    if response.status_code == 204:
        messages.success(request, 'Place deleted')
    else:
        messages.error(request, 'Unknown error. Please try again')
    return redirect('admin places')


def edit(request, place_id):
    # TODO: edit existing place
    if request.method == 'GET':
        types = json.loads(requests.get('http://77.244.251.110/api/placetypes').text)
        place = json.loads(requests.get('http://77.244.251.110/api/places/' + place_id).text)
        return render(request, 'admin/places/edit.html',
                      {
                          'types': types,
                          'place': place,
                          'currentUser': get_user(request)
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
        response = requests.put('http://77.244.251.110/api/places/' + place_id, data=json.dumps(data), headers=headers)
        if response.status_code == 204:
            messages.success(request, 'Place updated')
            return redirect('admin places')
        else:
            messages.error(request, 'Unknown error. Please try again')
            return redirect('admin place edit')


def delete_avatar(request, id):
    # TODO: delete image of place
    return


def add_avatar(request, id):
    # TODO: add new image
    return


def add_owner(request, id):
    # TODO: add new owner
    return
