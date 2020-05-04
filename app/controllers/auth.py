import requests
import json


def authorized(token):
    """
        This function takes authorization token and authorized it
        :param token:   Token that user gets if he log in
        :return:        Status code of request (200 - OK, 401 - unauthorized
    """
    headers = {
        "Authorization": "Bearer " + token
    }
    response = requests.get('http://77.244.251.110/api/users/me', headers=headers)
    return response.status_code


def get_user(request):
    if request.COOKIES.get('token'):
        headers = {
            "Authorization": "Bearer " + request.COOKIES['token']
        }
        return json.loads(requests.get('http://77.244.251.110/api/users/me', headers=headers).text)
    return None
