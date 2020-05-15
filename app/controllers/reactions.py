from django.http import HttpResponse
from django.shortcuts import render, redirect
from .auth import get_user, authorized
from django.contrib import messages
from django.views.decorators.http import require_http_methods
import requests
import json
from datetime import datetime


def create(request):

    return "true"


def delete(request):
    return "true"
