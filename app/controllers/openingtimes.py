from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib import messages
import requests
import json
from datetime import datetime
from .auth import authorized, get_user


def index(request, place_id):
    openingTimes = json.loads(requests.get('http://77.244.251.110/api/places/' + place_id + '/openingTimes').text)
    return render(request, 'openingtimes/index.html',
                  {
                      'openingTimes': openingTimes,
                      'currentUser': get_user(request)
                  })


def create(request, place_id):
    if request.method == 'GET':
        return render(request, 'openingtimes/create.html',
                      {
                          'currentUser': get_user(request)
                      })

    elif request.method == 'POST':
        open_min = int(request.POST.get("openMinutes"))
        open_hour = int(request.POST.get("openHour"))
        close_min = int(request.POST.get("closeMinutes"))
        close_hour = int(request.POST.get("closeHour"))

        open_time = str(open_hour) + ':' + str(open_min) + ':00'
        close_time = str(close_hour) + ':' + str(close_min) + ':00'

        headers = {
            'content-type': 'application/json',
            'Authorization': 'Bearer ' + request.COOKIES['token']
        }
        data = {
            "day": int(request.POST.get("day")),
            "open": open_time,
            "close": close_time,
        }
        response = requests.post('http://77.244.251.110/api/places/' + place_id + '/openingTimes',
                                 data=json.dumps(data),
                                 headers=headers)
        if response.status_code == 201:
            messages.success(request, 'Opening time added')
            return redirect('places')
        else:
            messages.error(request, 'Unknown error. Please try again')
            return render(request, 'openingtimes/create.html',  # TODO: form validation error
                          {
                              'currentUser': get_user(request)
                          })


def edit(request, place_id):
    if request.method == 'GET':
        openingTimes = json.loads(requests.get('http://77.244.251.110/api/places/' + place_id + '/openingTimes').text)
        return render(request, 'openingtimes/edit.html',
                      {
                          'openingTimes': openingTimes,
                          'currentUser': get_user(request)
                      })

    elif request.method == 'POST':
        open_time = request.POST.get("openHour") + ':' + request.POST.get("openMinutes") + ':00'
        close_time = request.POST.get("closeHour") + ':' + request.POST.get("closeMinutes") + ':00'

        id = request.POST.get("id")  # get from hidden input

        headers = {
            'content-type': 'application/json',
            'Authorization': 'Bearer ' + request.COOKIES['token']
        }
        data = {
            "day": int(request.POST.get("day")),
            "open": open_time,
            "close": close_time,
        }
        response = requests.put('http://77.244.251.110/api/places/' + place_id + '/openingTimes/' + id,
                                data=json.dumps(data),
                                headers=headers)
        if response.status_code == 201:
            messages.success(request, 'Opening times updated')
            return redirect('places')
        else:
            messages.error(request, 'Unknown error. Please try again')
            return render(request, 'openingtimes/edit.html',  # TODO: form validation error
                          {
                              'currentUser': get_user(request)
                          })
