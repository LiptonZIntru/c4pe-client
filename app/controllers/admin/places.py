from django.http import HttpResponseNotFound
from django.shortcuts import render, HttpResponse, redirect
from django.contrib import messages
from django.views.defaults import page_not_found
import json
import requests
from app.controllers.auth import admin
from django.conf import settings


@admin
def index(request):
    """
    :param request:     Request object
    :return:            HTML page with all places
    """
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


@admin
def create(request):
    """
    :param request:     Request object
    :return:            Create new place and redirect to places
    """
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


@admin
def delete(request, place_id):
    """
    :param request:     Request object
    :param place_id:    ID of place
    :return:            Delete place and redirect to places
    """
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


@admin
def edit(request, place_id):
    """
    :param request:     Request object
    :param place_id:    ID of place
    :return:            Update place and redirect to places
    """
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


@admin
def reviews(request, place_id):
    """
    :param request:     Request object
    :param place_id:    ID of place
    :return:            HTML page with all reviews related to that place
    """
    if request.method == 'GET':
        reviews = json.loads(requests.get(settings.API_IP + '/api/places/' + place_id + '/reviews').text)
        place = json.loads(requests.get(settings.API_IP + '/api/places/' + place_id).text)
        return render(request, 'admin/places/reviews.html',
                      {
                          'reviews': reviews,
                          'place': place
                      })


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
    response = requests.delete(settings.API_IP + '/api/places/' + place_id + '/Reviews/' + review_id,
                               headers=headers)
    if response.status_code == 204:
        messages.success(request, 'Review deleted')
    else:
        messages.error(request, 'Unknown error. Please try again')
    return redirect('admin places reviews', place_id=place_id)


@admin
def delete_avatar(request, place_id, id):
    """
    :param request:     Request object
    :param place_id:    ID of place
    :param id:          ID of photo
    :return:            Delete photo of place and redirect to index
    """
    headers = {
        'Authorization': 'Bearer ' + request.COOKIES['token']
    }
    response = requests.delete(settings.API_IP + '/api/places/' + place_id + '/images/' + id, headers=headers)
    if response.status_code == 204:
        messages.success(request, 'Avatar deleted')
    else:
        messages.error(request, response.text)
    return redirect('admin places edit', place_id=place_id)

