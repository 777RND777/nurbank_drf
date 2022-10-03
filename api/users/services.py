from django.http import Http404

from .models import User


def create_user(data):
    user = User.objects.create_user(**data)
    return user


def get_user_by_slug(slug):
    try:
        return User.objects.get(slug=slug)
    except User.DoesNotExist:
        raise Http404
