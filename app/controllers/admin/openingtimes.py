from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib import messages
import requests
import json
from datetime import datetime
from app.controllers.auth import authorized, get_user
from django.conf import settings


def create(request, place_id):
    if request.method == 'GET':
        return render(request, 'admin/openingtimes/create.html')

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
        response = requests.post(settings.API_IP + '/api/places/' + place_id + '/openingTimes',
                                 data=json.dumps(data),
                                 headers=headers)
        if response.status_code == 201:
            messages.success(request, 'Opening time added')
            return redirect('admin places opening_times')
        else:
            messages.error(request, 'Unknown error. Please try again')
            return render(request, 'admin/openingtimes/create.html')  # TODO: form validation error


def edit(request, place_id):
    if request.method == 'GET':
        openingTimes = json.loads(requests.get(settings.API_IP + '/api/places/' + place_id + '/openingTimes').text)
        place = json.loads(requests.get(settings.API_IP + '/api/places/' + place_id).text)
        return render(request, 'admin/openingtimes/edit.html',
                      {
                          'times': openingTimes,
                          'place': place
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
        response = requests.put(settings.API_IP + '/api/places/' + place_id + '/openingTimes/' + id,
                                data=json.dumps(data),
                                headers=headers)
        if response.status_code == 204:
            messages.success(request, 'Opening times updated')
            return redirect('admin places')
        else:
            messages.error(request, 'Unknown error. Please try again')
            return render(request, 'admin/openingtimes/edit.html')  # TODO: form validation error