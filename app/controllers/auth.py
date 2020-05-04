import requests


def validate(token):
    headers = {
        "Authorization": "Bearer " + token
    }
    response = requests.get('http://77.244.251.110/api/users/me', headers=headers)
    return response.status_code
