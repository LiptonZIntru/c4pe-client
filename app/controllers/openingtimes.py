from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib import messages
import requests
import json
from datetime import datetime
from .auth import authorized, get_user, login_required
from django.conf import settings


def index(request, place_id):
    """
    :param request:     Request object
    :param place_id:    ID of place
    :return:            HTML page where you can see opening times of place based of it's ID
    """
    openingTimes = json.loads(requests.get(settings.API_IP + '/api/places/' + place_id + '/openingTimes').text)
    return render(request, 'openingtimes/index.html',
                  {
                      'openingTimes': openingTimes
                  })


@login_required
def create(request, place_id):
    """
    :param request:     Request object
    :param place_id:    ID of place
    :return:            Create new opening time and redirect to places
    """
    if request.method == 'POST':
        open_min = request.POST.get("openMinutes")
        open_hour = request.POST.get("openHour")
        close_min = request.POST.get("closeMinutes")
        close_hour = request.POST.get("closeHour")

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
            return redirect('openingtimes edit', place_id=place_id)
        else:
            messages.error(request, 'Unknown error. Please try again')
            return redirect('openingtimes edit', place_id=place_id)


@login_required
def edit(request, place_id):
    """
    :param request:     Request object
    :param place_id:    ID of place
    :return:            Update opening times and redirect to places
    """
    if request.method == 'GET':
        openingTimes = json.loads(requests.get(settings.API_IP + '/api/places/' + place_id + '/openingTimes').text)
        place = json.loads(requests.get(settings.API_IP + '/api/places/' + place_id).text)
        return render(request, 'openingtimes/edit.html',
                      {
                          'times': openingTimes,
                          'place': place
                      })

    elif request.method == 'POST':
        open_time = request.POST.get("openHour") + ':' + request.POST.get("openMinutes") + ':00'
        close_time = request.POST.get("closeHour") + ':' + request.POST.get("closeMinutes") + ':00'

        id = request.POST.get("time_id")  # get from hidden input

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
            return redirect('openingtimes edit', place_id=place_id)
        else:
            messages.error(request, 'Unknown error. Please try again')
            return redirect('openingtimes edit', place_id=place_id)


@login_required
def delete(request, place_id, times_id):
    """
    :param request:     Request object
    :param place_id:    ID of place
    :param times_id:    ID of opening time
    :return:            Delete opening time and redirect to index
    """
    headers = {
        'content-type': 'application/json',
        'Authorization': 'Bearer ' + request.COOKIES['token']
    }
    response = requests.delete(settings.API_IP + '/api/places/' + place_id + '/OpeningTimes/' + times_id,
                               headers=headers)
    if response.status_code == 204:
        messages.success(request, 'Opening times deleted')
    else:
        messages.error(request, 'Unknown error. Please try again')
    return redirect('openingtimes edit', place_id=place_id)

