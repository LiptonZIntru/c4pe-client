from django.http import HttpResponse
from django.shortcuts import render, redirect
from .auth import get_user, authorized
from django.contrib import messages
from django.views.decorators.http import require_http_methods
import requests
import json
from datetime import datetime


def paginate(current, last):
    pages = {}
    pages['current'] = int(current)

    if last == 0:
        pages['content'] = [1, ]
    elif current == 1:
        pages['content'] = [1, 2, 3]
        pages['next'] = 2
    elif current == last:
        pages['content'] = [last - 2, last - 1, last]
        pages['previous'] = last - 1
    else:
        pages['content'] = [current - 1, current, current + 1]
        pages['next'] = current + 1
        pages['previous'] = current - 1

    if last == 1:
        pages['content'] = [1, ]
        if pages.get('next'):
            del (pages['next'])
    elif last == 2:
        pages['content'] = [1, 2]
    elif last == 3:
        pages['content'] = [1, 2, 3]
    return pages


def set_time(places):
    current_hour = int(datetime.now().hour)
    current_minute = int(datetime.now().minute)

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
                break
    return places


def get_url(request, url):
    name = request.GET.get('name')
    city = request.GET.get('city')
    isVerified = request.GET.get('isVerified')
    minRating = request.GET.get('minRating')
    maxRating = request.GET.get('maxRating')
    placeTypes = request.GET.get('placeType')
    isOpen = request.GET.get('isOpen')
    orderBy = request.GET.get('orderBy')

    if name:
        url = url + '&name=' + name
    if city:
        url = url + '&city=' + city
    if isVerified:
        url = url + '&=isVerified=' + isVerified
    if minRating:
        url = url + '&=minRating=' + minRating
    if maxRating:
        url = url + '&=maxRating=' + maxRating
    if isOpen:
        url = url + '&=isOpen=' + isOpen
    if orderBy:
        url = url + '&=orderBy=' + orderBy

    if placeTypes:
        for placeType in json.loads(placeTypes):
            url = url + '&placeType=' + str(placeType)

    return url
