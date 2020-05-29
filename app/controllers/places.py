from django.http import HttpResponse
from django.shortcuts import render, redirect
from .auth import get_user, authorized
from django.contrib import messages
from django.views.decorators.http import require_http_methods
from .filters import *
import requests
import json
from datetime import datetime
from django.conf import settings

# Create your views here.


def index(request):
    if request.method == "GET":
        places = ""
        current = 0
        last = 0
        page = request.GET.get('page')
        if page is None:
            page = '1'

        url = settings.API_IP + '/api/places?PageNumber=' + page

        url = get_url(request, url)

        response = requests.get(url)
        types = json.loads(requests.get(settings.API_IP + '/api/placetypes').text)
        try:
            places = json.loads(response.text)
            current = json.loads(response.headers['X-Pagination'])['CurrentPage']
            last = json.loads(response.headers['X-Pagination'])['TotalPages']
        except:
            pass

        places = set_time(places)  # opened until ...

        pages = paginate(current, last)

        return render(request, 'places/index.html',
                      {
                          'search': request.GET.get('name'),
                          'places': places,
                          'pages': pages,
                          'types': types
                      })


def profile(request, id):
    place = json.loads(requests.get(settings.API_IP + '/api/places/' + id).text)
    reviews = json.loads(requests.get(settings.API_IP + '/api/places/' + id + '/Reviews').text)

# SERAZENI PODLE NEJVICE LAJKOVANYCH
    def get_positive_reactions(review):
        return review.get('positiveReactions')

    reviews.sort(key=get_positive_reactions, reverse=True)
# KONEC SEKCE

    if len(reviews) > 5:
        reviews = reviews[len(reviews) - 6:len(reviews) - 1]

    return render(request, 'places/profile.html',
                  {
                      'place': place,
                      'reviews': reviews
                  })


def create(request):
    if request.method == 'GET':
        types = json.loads(requests.get(settings.API_IP + '/api/placetypes').text)
        return render(request, 'places/create.html',
                      {
                          'types': types
                      })
    elif request.method == 'POST':
        headers = {
            'content-type': 'application/json',
            'Authorization': 'Bearer ' + request.COOKIES['token']
        }
        data = {
            "street": request.POST.get("street"),
            "city": request.POST.get("city"),
            "zipCode": request.POST.get("zipCode"),  # TODO: not required
            "country": request.POST.get("country"),
            "name": request.POST.get("name"),
            "placeTypeID": int(request.POST.get("type"))
        }
        response = requests.post(settings.API_IP + '/api/places', data=json.dumps(data), headers=headers)

        '''if request.FILES.get('avatar'):
            avatar(request, id, 1)  # request.POST.get('image_id')'''

        if response.status_code == 201:
            if request.FILES.get('avatar'):
                avatar(request, json.loads(response.text)['id'], '1')
            messages.success(request, 'Place created')
            return redirect('places')
        else:
            messages.error(request, 'Unknown error. Please try again')
            return redirect('place create')


def edit(request, id):
    if request.method == 'GET':
        types = json.loads(requests.get(settings.API_IP + '/api/placetypes').text)
        place = json.loads(requests.get(settings.API_IP + '/api/places/' + id).text)
        return render(request, 'places/edit.html',
                      {
                          'types': types,
                          'place': place
                      })
    elif request.method == 'POST':
        headers = {
            'content-type': 'application/json',
            'Authorization': 'Bearer ' + request.COOKIES['token']
        }
        data = {
            "street": request.POST.get("street"),
            "city": request.POST.get("city"),
            "zipCode": request.POST.get("zipCode"),
            "country": request.POST.get("country"),
            "name": request.POST.get("name"),
            "placeTypeID": int(request.POST.get("type"))
        }
        response = requests.put(settings.API_IP + '/api/places/' + id, data=json.dumps(data), headers=headers)

        if request.FILES.get('avatar'):
            avatar(request, id, '1')  # request.POST.get('image_id')

        if response.status_code == 204:
            messages.success(request, 'Place updated')
            return redirect('places')
        else:
            messages.error(request, 'Unknown error. Please try again')
            return redirect('place edit')


@require_http_methods(["POST"])
def create_review(request, id):
    if request.method == 'POST':
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
            return redirect('place profile', id=id)
        else:
            messages.error(request, "You have already reviewed this place")
            return redirect('reviews', id=id)


# po dokonceni odstranit
def get_json_reviews(request, id, type):
    reviews = json.loads(requests.get(settings.API_IP + '/api/places/' + id + '/Reviews').text)
    response_reviews = []
    for review in reviews:
        if int(type) == 1:  # all
            return HttpResponse(json.dumps(reviews))
        elif int(type) == 2:  # positive
            if review['rating'] > 2:
                response_reviews.append(review)
        elif int(type) == 3:  # negative
            if review['rating'] < 3:
                response_reviews.append(review)
        elif int(type) == 4:  # verified
            if review['user']['isVerified']:
                response_reviews.append(review)
    return HttpResponse(json.dumps(response_reviews))  # REQUIRED TO BE HTTP RESPONSE


def avatar(request, place_id, id):
    if request.method == 'GET':
        '''images = json.loads(requests.get(settings.API_IP + '/api/places/' + place_id).text)['images']
        print(images)
        try:
            return render(request, 'places/image.html',
                          {
                              'image': images[int(id) - 1]
                          })
        except:'''
        return render(request, 'places/avatar.html')
    elif request.method == 'POST':
        avatar_file = request.FILES.get('avatar')
        file = open('app/static/upload/place.jpg', 'wb+')
        for chunk in avatar_file.chunks():
            file.write(chunk)
        headers = {
            'Authorization': 'Bearer ' + request.COOKIES['token']
        }
        data = {
            "image": open(r'app/static/upload/place.jpg', 'rb')
        }
        response = requests.post(settings.API_IP + '/api/places/' + place_id + '/images/' + id, files=data, headers=headers)
        if response.status_code == 200:
            messages.success(request, 'Avatar uploaded')
        else:
            messages.error(request, response.text)
        return redirect('place profile', id=place_id)


def delete_avatar(request, place_id, id):
    headers = {
        'Authorization': 'Bearer ' + request.COOKIES['token']
    }
    response = requests.delete(settings.API_IP + '/api/places/' + place_id + '/images/' + id, headers=headers)
    if response.status_code == 204:
        messages.success(request, 'Avatar deleted')
    else:
        messages.error(request, response.text)
    return redirect('place profile', id=place_id)
