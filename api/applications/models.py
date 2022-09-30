from django.conf import settings
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models

from users.models import User


class Application(models.Model):
    value = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(settings.MAX_APPLICATION_VALUE)])
    request_date = models.DateTimeField(auto_now_add=True)
    answer_date = models.DateTimeField(blank=True, null=True)
    approved = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="applications")

    def __str__(self):
        return str(self.id)

    class Meta:
        ordering = ["-pk"]
