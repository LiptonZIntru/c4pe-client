from django.http import HttpResponse
from django.shortcuts import render, redirect
from .auth import get_user, authorized, login_required
from django.contrib import messages
from django.views.decorators.http import require_http_methods
import requests
import json
from django.conf import settings


@login_required
def like(request, place_id, review_id):
    headers = {
        'content-type': 'application/json',
        'Authorization': 'Bearer ' + request.COOKIES['token']
    }
    data = {
        "isHelpful": True
    }
    reacted = json.loads(requests.get(
        settings.API_IP + '/api/places/' + place_id + '/reviews/' + review_id + '/reaction',
        headers=headers).text)

    try:
        if reacted['isHelpful']:
            response = requests.delete(
                settings.API_IP + '/api/places/' + place_id + '/reviews/' + review_id + '/reaction', headers=headers)
            if response.status_code == 204:
                reactions = json.loads(
                    requests.get(settings.API_IP + '/api/places/' + place_id + '/reviews/' + review_id,
                                 headers=headers).text)
                return HttpResponse(json.dumps(
                    {
                        'success': 'deleted',
                        'positiveReactions': reactions['positiveReactions'],
                        'negativeReactions': reactions['negativeReactions']
                    })
                )
    except:
        pass

    response = requests.post(settings.API_IP + '/api/places/' + place_id + '/reviews/' + review_id + '/reaction',
                             data=json.dumps(data), headers=headers)
    if response.status_code == 200:
        reactions = json.loads(requests.get(settings.API_IP + '/api/places/' + place_id + '/reviews/' + review_id,
                                            headers=headers).text)
        return HttpResponse(json.dumps(
            {
                'success': 'liked',
                'positiveReactions': reactions['positiveReactions'],
                'negativeReactions': reactions['negativeReactions']
            })
        )
    return HttpResponse(status=400)


@login_required
def dislike(request, place_id, review_id):
    headers = {
        'content-type': 'application/json',
        'Authorization': 'Bearer ' + request.COOKIES['token']
    }
    data = {
        "isHelpful": False
    }
    reacted = json.loads(requests.get(
        settings.API_IP + '/api/places/' + place_id + '/reviews/' + review_id + '/reaction',
        headers=headers).text)

    try:
        if not reacted['isHelpful']:
            response = requests.delete(
                settings.API_IP + '/api/places/' + place_id + '/reviews/' + review_id + '/reaction', headers=headers)
            if response.status_code == 204:
                reactions = json.loads(
                    requests.get(settings.API_IP + '/api/places/' + place_id + '/reviews/' + review_id,
                                 headers=headers).text)
                return HttpResponse(json.dumps(
                    {
                        'success': 'deleted',
                        'positiveReactions': reactions['positiveReactions'],
                        'negativeReactions': reactions['negativeReactions']
                    })
                )
    except:
        pass

    response = requests.post(settings.API_IP + '/api/places/' + place_id + '/reviews/' + review_id + '/reaction',
                             data=json.dumps(data), headers=headers)
    if response.status_code == 200:
        reactions = json.loads(requests.get(settings.API_IP + '/api/places/' + place_id + '/reviews/' + review_id,
                                            headers=headers).text)
        return HttpResponse(json.dumps(
            {
                'success': 'disliked',
                'positiveReactions': reactions['positiveReactions'],
                'negativeReactions': reactions['negativeReactions']
            })
        )
    return HttpResponse(status=400)
