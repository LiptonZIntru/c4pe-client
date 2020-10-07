from django.http import HttpResponse
from django.shortcuts import render, redirect
from .auth import get_user, authorized, login_required
from django.contrib import messages
import requests
import json
from datetime import datetime
from django.conf import settings


def index(request, id):
    """
    :param request:     Request object
    :param id:          ID of place
    :return:            HTML page with all reviews related to this place
    """
    place = json.loads(requests.get(settings.API_IP + '/api/places/' + id).text)
    reviews = json.loads(requests.get(settings.API_IP + '/api/places/' + id + '/Reviews').text)

    positiveReviews = []
    negativeReviews = []
    verifiedReviews = []

    for review in reviews:
        if review['rating'] < 3:
            negativeReviews.append(review)
        elif review['rating'] > 2:
            positiveReviews.append(review)
        if review['user']['isVerified']:
            verifiedReviews.append(review)

    # sort by most liked
    def get_positive_reactions(this_review):
        return this_review.get('positiveReactions')

    reviews.sort(key=get_positive_reactions, reverse=True)
    positiveReviews.sort(key=get_positive_reactions, reverse=True)
    negativeReviews.sort(key=get_positive_reactions, reverse=True)
    verifiedReviews.sort(key=get_positive_reactions, reverse=True)

    return render(request, 'reviews/index.html',
                  {
                      'place': place,
                      'reviews': reviews,
                      'positiveReviews': positiveReviews,
                      'negativeReviews': negativeReviews,
                      'verifiedReviews': verifiedReviews,
                      'positive': len(positiveReviews),
                      'negative': len(negativeReviews),
                      'verified': len(verifiedReviews)
                  })


@login_required
def create(request, id):
    """
    :param request:     Request object
    :param id:          ID of place
    :return:            Add new review and redirect to places
    """
    if request.method == 'GET':
        return render(request, 'reviews/create.html')
    elif request.method == 'POST':
        data = {
            'rating': int(request.POST.get('newRating')),
            'text': str(request.POST.get('newReviewText'))
        }
        headers = {
            'content-type': 'application/json',
            'Authorization': 'Bearer ' + request.COOKIES['token']
        }
        response = requests.post(settings.API_IP + '/api/places/' + id + '/Reviews', data=json.dumps(data),
                                 headers=headers)
        if response.status_code == 201:
            messages.success(request, 'Review added')
            return redirect('reviews', id=id)
        else:
            messages.error(request, "You have already reviewed this place")
            return redirect('reviews', id=id)


@login_required
def edit(request, place_id, id):
    """
    :param request:     Request object
    :param place_id:    ID of place
    :param id:          ID of review
    :return:            Update review and redirect to places
    """
    if request.method == 'GET':
        review = json.loads(requests.get(settings.API_IP + '/api/places/' + place_id + '/Reviews/' + id).text)
        return render(request, 'reviews/edit.html',
                      {
                          'review': review
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
        response = requests.put(settings.API_IP + '/api/places/' + place_id + '/Reviews/' + id, data=json.dumps(data), headers=headers)
        if response.status_code == 204:
            messages.success(request, 'Review updated')
            return redirect('reviews', id=place_id)
        else:
            messages.error(request, 'Unknown error. Please try again')
            return redirect('reviews', id=place_id)
