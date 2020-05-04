import requests


def validate(token):
    """
        This function takes authorization token and validate it
        :param token:   Token that user gets if he log in
        :return:        Status code of request (200 - OK, 401 - unauthorized
    """
    headers = {
        "Authorization": "Bearer " + token
    }
    response = requests.get('http://77.244.251.110/api/users/me', headers=headers)
    return response.status_code
