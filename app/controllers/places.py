from django.http import HttpResponse
from django.shortcuts import render, redirect
import requests
import json
from datetime import datetime

# Create your views here.


token = 'eyJhbGciOiJIUzUxMiIsInR5cCI6IkpXVCJ9.eyJuYW1laWQiOiI3IiwidW5pcXVlX25hbWUiOiJ2aWxpIiwibmJmIjoxNTg3MTMwMzc4LCJleHAiOjE1ODcyMTY3NzgsImlhdCI6MTU4NzEzMDM3OH0.ker5TIH4LwAMK5qNnrDSKb3eS05PuUads0UjD0t74HU2kYV53LOdVFIqHtNlbrlMfvk3swkDfp3LycIhQ_JQcg'


def index(request):
    page = request.GET.get('page')
    if page is None:
        page = '1'
    response = requests.get('http://77.244.251.110/api/places?PageNumber=' + page)
    places = json.loads(response.text)
    current = json.loads(response.headers['X-Pagination'])['CurrentPage']
    last = json.loads(response.headers['X-Pagination'])['TotalPages']
    pages = {}
    pages['current'] = int(current)

    #  dodelat, place['open'] vraci cas, do ktereho je otevreno
    '''for place in places:
        for open in place['openingTimes']:
            if int(open['day']) == int(datetime.today().weekday()) and int(open['open']) :
                place['open']'''

    if current == 1:
        pages['content'] = [1, 2, 3]
        pages['first'] = True
    elif current == last:
        pages['content'] = [last - 2, last - 1, last]
        pages['last'] = True
    else:
        pages['content'] = [current - 1, current, current + 1]

    return render(request, 'places/index.html', {'places': places, 'pages': pages})


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


