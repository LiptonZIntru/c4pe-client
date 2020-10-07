from django.http import HttpResponseNotFound
from django.shortcuts import render, HttpResponse, redirect
from django.contrib import messages
from django.views.defaults import page_not_found
import json
import requests
from app.controllers.auth import get_user, authorized, admin
from django.conf import settings


@admin
def index(request):
    """
    :param request:     Request object
    :return:            HTML page - admin dashboard
    """
    response = json.loads(requests.get(settings.API_IP + '/api/stats').text)
    return render(request, 'admin/home/index.html',
                  {
                      'places': response['amountPlaces'],
                      'users': response['amountUsers'],
                      'reviews': response['amountReviews']
                  })
