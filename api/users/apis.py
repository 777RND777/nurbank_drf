from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from . import serializers, services
from .models import User


@api_view(['POST'])
def register_view(request):
    serializer = serializers.RegistrationSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)

    data = serializer.validated_data
    serializer.instance = services.create_user(user_dc=data)
    return Response(serializer.data, status=status.HTTP_201_CREATED)


class AuthMixin(APIView):
    permission_classes = (IsAuthenticated,)


class UserDetail(AuthMixin):
    def get(self, request):
        serializer = serializers.UserSerializer(self.request.user)
        return Response(serializer.data)

    def patch(self, request):
        serializer = serializers.UserChangeSerializer(self.request.user, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)


class AdminMixin(APIView):
    permission_classes = (IsAdminUser,)


class AdminUserList(AdminMixin):
    @staticmethod
    def get(request):
        user = User.objects.all().order_by('-date_joined')
        serializer = serializers.AdminUserSerializer(user, many=True)
        return Response(serializer.data)


class AdminUserDetail(AdminMixin):
    @staticmethod
    def get(request, slug):
        user = services.get_user_by_slug(slug)
        serializer = serializers.AdminUserSerializer(user)
        return Response(serializer.data)

    @staticmethod
    def patch(request, slug):
        user = services.get_user_by_slug(slug)
        serializer = serializers.AdminUserSerializer(user, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    @staticmethod
    def delete(request, slug):
        user = services.get_user_by_slug(slug)
        user.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
