from rest_framework.serializers import ModelSerializer

from .models import Application, User


class RegistrationSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ["first_name", "last_name", "username", "password"]
        extra_kwargs = {'password': {'write_only': True}}


class UserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ["first_name", "last_name", "username", "debt"]


class UserChangeSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ["first_name", "last_name"]


class AdminUserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = "__all__"


class ApplicationSerializer(ModelSerializer):
    class Meta:
        model = Application
        fields = ["id", "value", "request_date", "answer_date", "approved"]


class ApplicationCreateSerializer(ModelSerializer):
    class Meta:
        model = Application
        fields = ["value"]


class AdminApplicationSerializer(ModelSerializer):
    class Meta:
        model = Application
        fields = "__all__"


class AdminApplicationCreateSerializer(ModelSerializer):
    class Meta:
        model = Application
        fields = "__all__"
