from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.text import slugify


class User(AbstractUser):
    slug = models.SlugField(max_length=150, default="admin")
    debt = models.IntegerField(default=0)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.username)
        self.password = make_password(self.password)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.username


class Application(models.Model):
    value = models.IntegerField()
    request_date = models.DateTimeField(auto_now_add=True)
    answer_date = models.DateTimeField(blank=True, null=True)
    approved = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="applications", null=True)

    def __str__(self):
        return str(self.id)

    class Meta:
        ordering = ["-pk"]
