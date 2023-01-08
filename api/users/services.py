from .models import User


def create_user(data):
    user = User.objects.create_user(**data)
    return user
