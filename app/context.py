from .controllers.auth import get_user
from django.conf import settings

# These functions are called every time template is rendered


def user(request):
    """
    :param request:     Request object
    :return:            Append to response user object
    """
    return {'currentUser': get_user(request)}


def api_url(request):
    """
    :param request:     Request object
    :return:            Append to response URL API
    """
    return {'API_IP': settings.API_IP}
