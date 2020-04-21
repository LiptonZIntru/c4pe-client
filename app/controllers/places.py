from django.http import HttpResponse
from django.shortcuts import render, redirect
import requests
import json

# Create your views here.


token = 'eyJhbGciOiJIUzUxMiIsInR5cCI6IkpXVCJ9.eyJuYW1laWQiOiI3IiwidW5pcXVlX25hbWUiOiJ2aWxpIiwibmJmIjoxNTg3MTMwMzc4LCJleHAiOjE1ODcyMTY3NzgsImlhdCI6MTU4NzEzMDM3OH0.ker5TIH4LwAMK5qNnrDSKb3eS05PuUads0UjD0t74HU2kYV53LOdVFIqHtNlbrlMfvk3swkDfp3LycIhQ_JQcg'

def index(request):
    places = json.loads(requests.get('http://77.244.251.110/api/places').text)
    return render(request, 'places/index.html', {'places': places})


def profile(request, id):
    place = json.loads(requests.get('http://77.244.251.110/api/places/' + id).text)
    reviews = json.loads(requests.get('http://77.244.251.110/api/places/' + id + '/Reviews').text)
    return render(request, 'test/places/profile.html', {'place': place, 'reviews': reviews})


def create(request):
    if request.method == 'GET':
        types = json.loads(requests.get('http://77.244.251.110/api/placetypes').text)
        return render(request, 'test/places/create.html', {'types': types})
    elif request.method == 'POST':
        headers = {
            'content-type': 'application/json',
            'Authorization': 'Bearer ' + token
        }
        data = {
            "street": request.POST.get("street"),
            "city": request.POST.get("city"),
            "zipCode": request.POST.get("zipCode"),
            "country": request.POST.get("country"),
            "name": request.POST.get("name"),
            "placeTypeID": int(request.POST.get("type"))
        }
        status = requests.post('http://77.244.251.110/api/places', data=json.dumps(data), headers=headers)
        print(status.status_code)
        return HttpResponse("status code: " + str(status.status_code))


def edit(request, id):
    if request.method == 'GET':
        types = json.loads(requests.get('http://77.244.251.110/api/placetypes').text)
        place = json.loads(requests.get('http://77.244.251.110/api/places/' + id).text)
        return render(request, 'test/places/edit.html', {'types': types, 'place': place})
    elif request.method == 'POST':
        headers = {
            'content-type': 'application/json',
            'Authorization': 'Bearer ' + token
        }
        data = {
            "street": request.POST.get("street"),
            "city": request.POST.get("city"),
            "zipCode": request.POST.get("zipCode"),
            "country": request.POST.get("country"),
            "name": request.POST.get("name"),
            "placeTypeID": int(request.POST.get("type"))
        }
        status = requests.post('http://77.244.251.110/api/places', data=json.dumps(data), headers=headers)
        print(status.status_code)
        return HttpResponse("status code: " + str(status.status_code))


