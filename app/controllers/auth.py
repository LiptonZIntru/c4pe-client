from django.shortcuts import render, redirect
from django.contrib import messages
import requests
import json
from datetime import datetime
from django.conf import settings


def authorized(token):
    """
        This function takes authorization token and authorized it
        :param token:   Token that user gets if he log in
        :return:        Status code of request (200 - OK, 401 - unauthorized)
    """
    if token:
        headers = {
            "Authorization": "Bearer " + token
        }
        response = requests.get(settings.API_IP + '/api/users/me', headers=headers)
        return response.status_code
    return 401


def get_user(request):
    """
        This function takes request
        :param request:     Request variable in route
        :return:            User object or None if user is not logged
    """
    if request.COOKIES.get('token'):
        headers = {
            "Authorization": "Bearer " + request.COOKIES['token']
        }
        return json.loads(requests.get(settings.API_IP + '/api/users/me', headers=headers).text)
    return None


def is_admin(request):
    """
        This function takes request
        :param request:     Request variable in route
        :return:            True if user is admin, otherwise False
    """
    if request.COOKIES.get('token'):
        headers = {
            "Authorization": "Bearer " + request.COOKIES['token']
        }
        role = json.loads(requests.get(settings.API_IP + '/api/users/me', headers=headers).text)['role']
        if role == 'Admin':
            return True
    return False


def login_required(func):
    """
        Wrapper function ensures that user is authenticated
        :param func:        Function to wrap
        :return:            Base function
    """
    def wrapper_func(request, *args, **kwargs):
        if not request.COOKIES.get('token'):
            messages.error(request, 'You need to login to perform this action')
            return redirect('login')
        return func(request, *args, **kwargs)
    return wrapper_func


def admin(func):
    """
        Wrapper function ensures that user is administrator
        :param func:        Function to wrap
        :return:            Base function
    """
    def wrapper_func(request, *args, **kwargs):
        if request.COOKIES.get('token'):
            headers = {
                "Authorization": "Bearer " + request.COOKIES['token']
            }
            role = json.loads(requests.get(settings.API_IP + '/api/users/me', headers=headers).text)['role']
            if role == 'Admin':
                return func(request, *args, **kwargs)
        messages.error(request, 'Permission denied')
        return redirect('login')
    return wrapper_func
