from rest_framework.serializers import ModelSerializer

from .models import User


class RegistrationSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'password']
        extra_kwargs = {
            'username': {'required': True},
            'password': {'required': True, 'write_only': True}
        }


class UserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'debt']


class UserChangeSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'debt']
        extra_kwargs = {
            'username': {'read_only': True},
            'debt': {'read_only': True},
        }


class AdminUserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'
        extra_kwargs = {
            'username': {'read_only': True},
            'password': {'read_only': True},
        }
