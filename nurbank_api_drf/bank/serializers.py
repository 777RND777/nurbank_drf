from rest_framework.serializers import ModelSerializer

from .models import User


class UserCreateSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ["first_name", "last_name", "username", "password"]


class UserOutputSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ["first_name", "last_name", "username", "debt"]


class UserChangeSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ["first_name", "last_name", "password"]


class UserAdminSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = "__all__"
