from .controllers.auth import get_user
from django.conf import settings


def user(request):
    return {'currentUser': get_user(request)}


def api_url(request):
    return {'API_IP': settings.API_IP}
