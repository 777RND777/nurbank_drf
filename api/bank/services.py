import datetime

from django.conf import settings
from django.http import Http404
import jwt

from .models import Application, User


def get_user_by_slug(slug):
    try:
        return User.objects.get(slug=slug)
    except User.DoesNotExist:
        raise Http404


def get_application_by_pk(pk):
    try:
        return Application.objects.get(pk=pk)
    except Application.DoesNotExist:
        raise Http404


def create_token(user_id: int) -> str:
    payload = dict(
        id=user_id,
        exp=datetime.datetime.utcnow() + datetime.timedelta(hours=24),
        iat=datetime.datetime.utcnow(),
    )
    token = jwt.encode(payload, settings.JWT_SECRET, algorithm="HS256")
    return token
