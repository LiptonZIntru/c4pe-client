from django.http import HttpResponse
from django.shortcuts import render
import requests
import json
from datetime import datetime

token = 'eyJhbGciOiJIUzUxMiIsInR5cCI6IkpXVCJ9.eyJuYW1laWQiOiI3IiwidW5pcXVlX25hbWUiOiJ2aWxpIiwibmJmIjoxNTg3MTMwMzc4LCJleHAiOjE1ODcyMTY3NzgsImlhdCI6MTU4NzEzMDM3OH0.ker5TIH4LwAMK5qNnrDSKb3eS05PuUads0UjD0t74HU2kYV53LOdVFIqHtNlbrlMfvk3swkDfp3LycIhQ_JQcg'


def index(request, id):
    place = json.loads(requests.get('http://77.244.251.110/api/places/' + id).text)
    reviews = json.loads(requests.get('http://77.244.251.110/api/places/' + id + '/Reviews').text)

    positive = 0
    negative = 0
    verified = 0
    for review in reviews:
        if review['rating'] < 3:
            negative = negative + 1
        elif review['rating'] > 2:
            positive = positive + 1
        if review['user']['isVerified']:
            verified = verified + 1
    return render(request, 'reviews/index.html', {'place': place, 'reviews': reviews, 'positive': positive, 'negative': negative, 'verified': verified})

def create(request, id):
    if request.method == 'GET':
        return render(request, 'reviews/create.html')
    elif request.method == 'POST':
        time = str(datetime.now())
        time = time[0:10] + 'T' + time[11:23]
        data = {
            'userID': int(request.POST.get('user')),
            'rating': int(request.POST.get('rating')),
            'text': str(request.POST.get('text')),
            'time': time
        }
        headers = {
            'content-type': 'application/json',
            'Authorization': 'Bearer ' + token
        }
        response = requests.post('http://77.244.251.110/api/places/' + id + '/Reviews', data=json.dumps(data),
                                 headers=headers)
        return HttpResponse('status code: ' + str(response.status_code) + '<br>Message: ' + response.text)


def edit(request, place_id, id):
    if request.method == 'GET':
        review = json.loads(requests.get('http://77.244.251.110/api/places/' + place_id + '/Reviews/' + id).text)
        return render(request, 'reviews/edit.html', {'review': review})
    elif request.method == 'POST':
        time = str(datetime.now())
        time = time[0:10] + 'T' + time[11:23]
        data = {
            'userID': int(request.POST.get('user')),
            'rating': int(request.POST.get('rating')),
            'text': str(request.POST.get('text')),
            'time': time
        }
        headers = {
            'content-type': 'application/json',
            'Authorization': 'Bearer ' + token
        }
        response = requests.put('http://77.244.251.110/api/places/' + place_id + '/Reviews/' + id, data=json.dumps(data), headers=headers)
        return HttpResponse('status code: ' + str(response.status_code) + '<br>Message: ' + response.text)
