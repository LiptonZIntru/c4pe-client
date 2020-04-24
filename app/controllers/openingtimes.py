from django.http import HttpResponse
from django.shortcuts import render, redirect
import requests
import json
from datetime import datetime

token = 'eyJhbGciOiJIUzUxMiIsInR5cCI6IkpXVCJ9.eyJuYW1laWQiOiI3IiwidW5pcXVlX25hbWUiOiJ2aWxpIiwibmJmIjoxNTg3MTMwMzc4LCJleHAiOjE1ODcyMTY3NzgsImlhdCI6MTU4NzEzMDM3OH0.ker5TIH4LwAMK5qNnrDSKb3eS05PuUads0UjD0t74HU2kYV53LOdVFIqHtNlbrlMfvk3swkDfp3LycIhQ_JQcg'


def index(request, place_id):
    openingTimes = json.loads(requests.get('http://77.244.251.110/api/places/' + place_id + '/openingTimes').text)
    return render(request, 'openingtimes/index.html', {'openingTimes': openingTimes})


def create(request, place_id):
    if request.method == 'GET':
        return render(request, 'openingtimes/create.html')

    elif request.method == 'POST':
        open_min = int(request.POST.get("openMinutes"))
        open_hour = int(request.POST.get("openHour"))
        close_min = int(request.POST.get("closeMinutes"))
        close_hour = int(request.POST.get("closeHour"))

        open_time = str(open_hour) + ':' + str(open_min) + ':00'
        print(open_time)
        close_time = str(close_hour) + ':' + str(close_min) + ':00'
        print(close_time)
        headers = {
            'content-type': 'application/json',
            'Authorization': 'Bearer ' + token
        }
        data = {
            "day": int(request.POST.get("day")),
            "open": open_time,
            "close": close_time,
        }
        response = requests.post('http://77.244.251.110/api/places/' + place_id + '/openingTimes',
                                 data=json.dumps(data), headers=headers)
        print(data)
        return HttpResponse('status code: ' + str(response.status_code))


def edit(request, place_id):
    if request.method == 'GET':
        openingTimes = json.loads(requests.get('http://77.244.251.110/api/places/' + place_id + '/openingTimes').text)
        return render(request, 'openingtimes/edit.html', {'openingTimes': openingTimes})

    elif request.method == 'POST':
        open_time = request.POST.get("openHour") + ':' + request.POST.get("openMinutes") + ':00'
        close_time = request.POST.get("closeHour") + ':' + request.POST.get("closeMinutes") + ':00'

        id = request.POST.get("id")

        headers = {
            'content-type': 'application/json',
            'Authorization': 'Bearer ' + token
        }
        data = {
            "day": int(request.POST.get("day")),
            "open": open_time,
            "close": close_time,
        }
        response = requests.put('http://77.244.251.110/api/places/' + place_id + '/openingTimes/' + id, data=json.dumps(data), headers=headers)
        return HttpResponse('status code: ' + str(response.status_code))
