from django.http import HttpResponse
from django.shortcuts import render, redirect
from .auth import get_user, authorized
from django.contrib import messages
import requests
import json
from datetime import datetime


def index(request, id):
    place = json.loads(requests.get('http://77.244.251.110/api/places/' + id).text)
    reviews = json.loads(requests.get('http://77.244.251.110/api/places/' + id + '/Reviews').text)

    positive = 0
    negative = 0
    verified = 0

    positiveReviews = []
    negativeReviews = []
    verifiedReviews = []

    for review in reviews:
        if review['rating'] < 3:
            negative = negative + 1
            negativeReviews.append(review)
        elif review['rating'] > 2:
            positive = positive + 1
            positiveReviews.append(review)
        if review['user']['isVerified']:
            verified = verified + 1
            verifiedReviews.append(review)

    return render(request, 'reviews/index.html',
                  {
                      'place': place,
                      'reviews': reviews,
                      'positiveReviews': positiveReviews,
                      'negativeReviews': negativeReviews,
                      'verifiedReviews': verifiedReviews,
                      'positive': positive,
                      'negative': negative,
                      'verified': verified,
                      'currentUser': get_user(request)
                  })


def create(request, id):
    if request.method == 'GET':
        return render(request, 'reviews/create.html',
                      {
                          'currentUser': get_user(request)
                      })
    elif request.method == 'POST':
        data = {
            'rating': int(request.POST.get('newRating')),
            'text': str(request.POST.get('newReviewText'))
        }
        headers = {
            'content-type': 'application/json',
            'Authorization': 'Bearer ' + request.COOKIES['token']
        }
        response = requests.post('http://77.244.251.110/api/places/' + id + '/Reviews', data=json.dumps(data),
                                 headers=headers)
        if response.status_code == 201:
            messages.success(request, 'Review added')
            return redirect('reviews', id=id)
        else:
            messages.error(request, "You have already reviewed this place")
            return redirect('reviews', id=id)


def edit(request, place_id, id):
    if request.method == 'GET':
        review = json.loads(requests.get('http://77.244.251.110/api/places/' + place_id + '/Reviews/' + id).text)
        return render(request, 'reviews/edit.html',
                      {
                          'review': review,
                          'currentUser': get_user(request)
                      })
    elif request.method == 'POST':
        data = {
            'rating': int(request.POST.get('editRating')),
            'text': str(request.POST.get('editReviewText')),
        }
        headers = {
            'content-type': 'application/json',
            'Authorization': 'Bearer ' + request.COOKIES['token']
        }
        response = requests.put('http://77.244.251.110/api/places/' + place_id + '/Reviews/' + id, data=json.dumps(data), headers=headers)
        if response.status_code == 204:
            messages.success(request, 'Review updated')
            return redirect('reviews', id=place_id)
        else:
            messages.error(request, 'Unknown error. Please try again')
            return redirect('reviews', id=place_id)  # TODO: form validation error
