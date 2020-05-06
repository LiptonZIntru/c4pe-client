from django.http import HttpResponseNotFound
from django.shortcuts import render, HttpResponse, redirect
from django.contrib import messages
from django.views.defaults import page_not_found
import json
import requests
from app.controllers.auth import get_user, authorized, is_admin


def index(request):
    if is_admin(request):
        return render(request, 'admin/home/index.html',
                      {
                          'currentUser': get_user(request)
                      })
    else:
        messages.error(request, 'Permission denied')
        return redirect('index')
