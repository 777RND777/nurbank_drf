from django.contrib.auth.decorators import login_required
from django.http import Http404
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import User
from .serializers import (UserAdminSerializer,
                          UserChangeSerializer, UserCreateSerializer, UserOutputSerializer)


class UserList(APIView):
    @staticmethod
    # admin stuff
    def get(request):
        user = User.objects.all().order_by('-date_joined')
        serializer = UserAdminSerializer(user, many=True)
        return Response(serializer.data)

    @staticmethod
    def post(request):
        serializer = UserCreateSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserDetail(APIView):
    @staticmethod
    def get_object(pk):
        try:
            return User.objects.get(pk=pk)
        except User.DoesNotExist:
            raise Http404

    # admin stuff. separate user detail
    def get(self, request, pk):
        user = self.get_object(pk)
        serializer = UserAdminSerializer(user)
        return Response(serializer.data)

    # TODO after auth
    # def put(self, request, pk):
    #     user = self.get_object(pk)
    #     if self.request.user.is_superuser:
    #         serializer = UserAdminSerializer(user, data=request.data)
    #     else:
    #         serializer = UserChangeSerializer(user, data=request.data)
    #     if serializer.is_valid():
    #         serializer.save()
    #         return Response(serializer.data)
    #     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # admin stuff
    def delete(self, request, pk):
        user = self.get_object(pk)
        user.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
