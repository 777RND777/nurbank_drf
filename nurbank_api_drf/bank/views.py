from django.http import Http404
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Application, User
from .serializers import (RegistrationSerializer,
                          UserAdminSerializer,
                          UserChangeSerializer, UserSerializer,
                          ApplicationCreateSerializer, ApplicationSerializer)


@api_view(['POST'])
def register_view(request):
    serializer = RegistrationSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserDetail(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        serializer = UserSerializer(self.request.user)
        return Response(serializer.data)

    def patch(self, request):
        serializer = UserChangeSerializer(self.request.user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ApplicationList(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = ApplicationCreateSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=self.request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request):
        applications = self.request.user.applications
        serializer = ApplicationSerializer(applications, many=True)
        return Response(serializer.data)


class AdminApplicationList(APIView):
    permission_classes = [IsAdminUser]

    @staticmethod
    def get(request):
        applications = Application.objects.all()
        serializer = ApplicationSerializer(applications, many=True)
        return Response(serializer.data)


@api_view(['GET'])
@permission_classes([IsAdminUser])
def user_list_view(request):
    user = User.objects.all().order_by('-date_joined')
    serializer = UserAdminSerializer(user, many=True)
    return Response(serializer.data)


class AdminUserMixin(APIView):
    permission_classes = [IsAdminUser]

    @staticmethod
    def get_object(slug):
        try:
            return User.objects.get(slug=slug)
        except User.DoesNotExist:
            raise Http404


class AdminUserDetail(AdminUserMixin):
    def get(self, request, slug):
        user = self.get_object(slug)
        serializer = UserAdminSerializer(user)
        return Response(serializer.data)

    def patch(self, request, slug):
        user = self.get_object(slug)
        serializer = UserAdminSerializer(user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, slug):
        user = self.get_object(slug)
        user.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def user_application_list_view(request, slug):
    applications = Application.objects.filter(user__slug=slug)
    serializer = ApplicationSerializer(applications, many=True)
    return Response(serializer.data)
