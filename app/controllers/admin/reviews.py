from django.http import HttpResponseNotFound
from django.shortcuts import render, HttpResponse, redirect
from django.contrib import messages
from django.views.defaults import page_not_found
import json
import requests
from app.controllers.auth import admin
from django.conf import settings


@admin
def delete(request, id):
    # TODO: delete review
    return
