from rest_framework.serializers import ModelSerializer

from .models import User


class UserOutputSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "first_name", "last_name", "username", "debt"]
