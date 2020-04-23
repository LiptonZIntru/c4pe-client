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

    current_hour = int(datetime.now().hour)
    current_minute = int(datetime.now().minute)

    #  print(open['open'][3:5])

    #  dodelat, place['open'] vraci cas, do ktereho je otevreno
    for place in places:
        for time in place['openingTimes']:
            place['open'] = {}
            open_minute = int(time['open'][3:5])
            open_hour = int(time['open'][0:2])
            close_minute = int(time['close'][3:5])
            close_hour = int(time['close'][0:2])

            if int(time['day']) == int(datetime.today().weekday()):
                if open_hour < current_hour < close_hour:
                    place['open']['state'] = 1
                    if 0 <= close_hour - current_hour < 2:
                        place['open']['state'] = 2
                        place['open']['time'] = time['close'][0:5]
                elif open_hour == current_hour:
                    if open_minute < current_minute:
                        place['open']['state'] = 1
                        if 0 <= close_hour - current_hour < 2:
                            place['open']['state'] = 2
                            place['open']['time'] = time['close'][0:5]
                    else:
                        place['open']['state'] = 4
                        if 0 <= open_hour - current_hour < 2:
                            place['open']['state'] = 3
                            place['open']['time'] = time['open'][0:5]
                elif close_hour == current_hour:
                    if close_minute > current_minute:
                        place['open']['state'] = 1
                        if 0 <= close_hour - current_hour < 2:
                            place['open']['state'] = 2
                            place['open']['time'] = time['close'][0:5]
                    else:
                        place['open']['state'] = 4
                        if 0 <= open_hour - current_hour < 2:
                            place['open']['state'] = 3
                            place['open']['time'] = time['open'][0:5]
                elif open_hour > current_hour or close_hour < current_hour:
                    place['open']['state'] = 4
                    if 0 <= open_hour - current_hour < 2:
                        place['open']['state'] = 3
                        place['open']['time'] = time['open'][0:5]

    #  pagination
    if current == 1:
        pages['content'] = [1, 2, 3]
        pages['first'] = True
    elif current == last:
        pages['content'] = [last - 2, last - 1, last]
        pages['last'] = True
    else:
        pages['content'] = [current - 1, current, current + 1]
    #  pagination

    return render(request, 'places/index.html', {'places': places, 'pages': pages})


def profile(request, id):
    place = json.loads(requests.get('http://77.244.251.110/api/places/' + id).text)
    reviews = json.loads(requests.get('http://77.244.251.110/api/places/' + id + '/Reviews').text)

    positive = 0
    negative = 0
    for review in reviews:
        if review['rating'] < 4:
            negative = negative + 1
        else:
            positive = positive + 1
    return render(request, 'places/profile.html', {'place': place, 'reviews': reviews, 'positive': positive, 'negative': negative})


def create(request):
    if request.method == 'GET':
        types = json.loads(requests.get('http://77.244.251.110/api/placetypes').text)
        return render(request, 'places/create.html', {'types': types})
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
        return render(request, 'places/edit.html', {'types': types, 'place': place})
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
        status = requests.put('http://77.244.251.110/api/places/' + id, data=json.dumps(data), headers=headers)
        print(status.status_code)
        return HttpResponse("status code: " + str(status.status_code))
