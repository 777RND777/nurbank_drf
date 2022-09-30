from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    slug = models.SlugField(max_length=150, default="admin")
    debt = models.IntegerField(default=0)

    def __str__(self):
        return self.username
