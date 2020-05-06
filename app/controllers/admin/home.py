from django.http import HttpResponseNotFound
from django.shortcuts import render, HttpResponse
from django.views.defaults import page_not_found
import json
import requests
from app.controllers.auth import get_user, authorized


def index(request):
    return render(request, 'admin/home/index.html')
