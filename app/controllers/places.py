from django.http import HttpResponse
from django.shortcuts import render, redirect
from .auth import get_user, authorized, login_required
from django.contrib import messages
from django.views.decorators.http import require_http_methods
from .filters import *
import requests
import json
from datetime import datetime
from django.conf import settings

# Create your views here.


def index(request):
    """
    :param request:     Request object
    :return:            HTML page with 10 places
    """
    if request.method == "GET":
        search_string = request.GET.get('name')
        places = ""
        current = 0
        last = 0
        page = request.GET.get('page')
        if page is None:
            page = '1'

        url = settings.API_IP + '/api/places?PageNumber=' + page

        url = get_url(request, url)

        frontend_url = get_frontend_url(request)

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
                          'search': search_string,
                          'places': places,
                          'pages': pages,
                          'types': types,
                          'url': frontend_url
                      })


def profile(request, id):
    """
    :param request:     Request object
    :param id:          ID of place
    :return:            HTML page with single place
    """
    place = json.loads(requests.get(settings.API_IP + '/api/places/' + id).text)
    reviews = json.loads(requests.get(settings.API_IP + '/api/places/' + id + '/Reviews').text)

    # Sort by most liked
    def get_positive_reactions(review):
        return review.get('positiveReactions')

    try:
        reviews.sort(key=get_positive_reactions, reverse=True)
    except:
        messages.error(request, 'Place does not exist')
        return redirect('places')

    if len(reviews) > 5:
        reviews = reviews[len(reviews) - 6:len(reviews) - 1]

    return render(request, 'places/profile.html',
                  {
                      'place': place,
                      'reviews': reviews
                  })


@login_required
def create(request):
    """
    :param request:     Request object
    :return:            Create new place and redirect to index
    """
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


@login_required
def edit(request, id):
    """
    :param request:     Request object
    :param id:          ID of place
    :return:            Update place and redirect to index
    """
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
        else:
            messages.error(request, 'Unknown error. Please try again')
        return redirect('place profile', id=id)


@login_required
@require_http_methods(["POST"])
def create_review(request, id):
    """
    :param request:     Request object
    :param id:          ID of place
    :return:            Create review and redirect to reviews
    """
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


'''
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
'''

@login_required
def avatar(request, place_id, id):
    """
    :param request:     Request object
    :param place_id:    Place ID
    :param id:          Photo ID
    :return:            Add photo and redirect to single place
    """
    if request.method == 'POST':
        avatar_file = request.FILES.get('avatar')
        file = open(settings.ABSOLUTE_PATH + 'app/static/upload/place.jpg', 'wb+')
        for chunk in avatar_file.chunks():
            file.write(chunk)
        headers = {
            'Authorization': 'Bearer ' + request.COOKIES['token']
        }
        data = {
            "image": open(settings.ABSOLUTE_PATH + r'app/static/upload/place.jpg', 'rb')
        }
        response = requests.post(settings.API_IP + '/api/places/' + place_id + '/images/' + id, files=data, headers=headers)
        if response.status_code == 200:
            messages.success(request, 'Avatar uploaded')
        else:
            messages.error(request, 'Image is too large, maximum size is 2.5 MB')
        return redirect('place profile', id=place_id)


@login_required
def delete_avatar(request, place_id, id):
    """
    :param request:     Request object
    :param place_id:    ID of place
    :param id:   ID of review
    :return:            Delete review and redirect to all reviews
    """
    headers = {
        'Authorization': 'Bearer ' + request.COOKIES['token']
    }
    response = requests.delete(settings.API_IP + '/api/places/' + place_id + '/images/' + id, headers=headers)
    if response.status_code == 204:
        messages.success(request, 'Avatar deleted')
    else:
        messages.error(request, response.text)
    return redirect('place profile', id=place_id)


@login_required
def delete(request, id):
    """
    :param request:     Request object
    :param id:    ID of place
    :return:            Delete place and redirect to index
    """
    headers = {
        'Authorization': 'Bearer ' + request.COOKIES['token']
    }
    response = requests.delete(settings.API_IP + '/api/places/' + id, headers=headers)
    if response.status_code == 200:
        messages.success(request, 'Place deleted')
    else:
        messages.error(request, 'Unknown error. Please try again')
    return redirect('place profile', id=id)
