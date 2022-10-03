from django.contrib.auth.models import AbstractUser, UserManager as Manager
from django.db import models
from django.utils.text import slugify


class UserManager(Manager):
    def create_user(self, username, password=None, **extra_fields):
        user = self.model(username=username, **extra_fields)
        user.slug = slugify(username)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        user = self.create_user(username=username, password=password, **extra_fields)
        return user


class User(AbstractUser):
    slug = models.SlugField(max_length=150)
    debt = models.IntegerField(default=0)

    objects = UserManager()

    def __str__(self):
        return self.username
