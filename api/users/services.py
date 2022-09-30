import dataclasses

from django.http import Http404
from django.utils.text import slugify

from .models import User


@dataclasses.dataclass
class UserDataClass:
    username: str
    password: str
    first_name: str = ""
    last_name: str = ""

    @classmethod
    def from_instance(cls, user: User) -> "UserDataClass":
        return cls(username=user.username,
                   password=user.password,
                   first_name=user.first_name,
                   last_name=user.last_name)


# TODO create your own UserManager
#  Also it helps to remove default value for slug field in User model.
def create_user(user_dc: UserDataClass) -> UserDataClass:
    user = User(username=user_dc.username,
                first_name=user_dc.first_name,
                last_name=user_dc.last_name)
    user.slug = slugify(user_dc.username)
    user.set_password(user_dc.password)
    user.save()
    return UserDataClass.from_instance(user)


def get_user_by_slug(slug):
    try:
        return User.objects.get(slug=slug)
    except User.DoesNotExist:
        raise Http404
