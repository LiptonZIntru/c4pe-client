from django.http import HttpResponseNotFound
from django.shortcuts import render, HttpResponse
from django.views.defaults import page_not_found
import json
import requests
from django.conf import settings

def serve_images(request):
    """
        serve files over https
    """
    path = request.GET.get('name')
    url = settings.API_IP + '/' + path
    response = requests.get(url)
    return HttpResponse(response.content, content_type="image/png")