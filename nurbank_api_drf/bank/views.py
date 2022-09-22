from django.http import Http404
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import User
from .serializers import (RegistrationSerializer,
                          UserAdminSerializer,
                          UserChangeSerializer, UserOutputSerializer)


@api_view(['POST'])
def register_view(request):
    serializer = RegistrationSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@permission_classes([IsAdminUser])
def user_list_view(request):
    user = User.objects.all().order_by('-date_joined')
    serializer = UserAdminSerializer(user, many=True)
    return Response(serializer.data)


class UserDetail(APIView):
    @staticmethod
    def get_object(pk):
        try:
            return User.objects.get(pk=pk)
        except User.DoesNotExist:
            raise Http404

    @permission_classes([IsAuthenticated])
    def get(self, request, pk):
        user = self.get_object(pk)
        if self.request.user.is_superuser:
            serializer = UserAdminSerializer(user)
        else:
            serializer = UserOutputSerializer(user)
        return Response(serializer.data)

    @permission_classes([IsAuthenticated])
    def put(self, request, pk):
        user = self.get_object(pk)
        if self.request.user.is_superuser:
            serializer = UserAdminSerializer(user, data=request.data)
        else:
            serializer = UserChangeSerializer(user, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @permission_classes([IsAdminUser])
    def delete(self, request, pk):
        user = self.get_object(pk)
        user.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
