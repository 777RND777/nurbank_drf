from rest_framework.serializers import ModelSerializer

from .models import Application, User


class RegistrationSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ["first_name", "last_name", "username", "password"]
        extra_kwargs = {
            'username': {'required': True},
            'password': {'required': True, 'write_only': True}
        }


class UserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ["first_name", "last_name", "username", "debt"]


class UserChangeSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ["first_name", "last_name", "username", "debt"]
        extra_kwargs = {
            'username': {'read_only': True},
            'debt': {'read_only': True},
        }


class AdminUserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = "__all__"


class ApplicationSerializer(ModelSerializer):
    class Meta:
        model = Application
        fields = ["value", "request_date", "answer_date", "approved"]


class ApplicationCreateSerializer(ModelSerializer):
    class Meta:
        model = Application
        fields = ["value", "request_date"]
        extra_kwargs = {
            'value': {'required': True},
        }


class AdminApplicationSerializer(ModelSerializer):
    class Meta:
        model = Application
        fields = "__all__"


class AdminApplicationCreateSerializer(ModelSerializer):
    class Meta:
        model = Application
        fields = "__all__"
        extra_kwargs = {
            'value': {'required': True},
            'user_id': {'required': True},
        }
