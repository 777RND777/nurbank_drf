from django.contrib.auth import authenticate
from rest_framework import exceptions, response, status
from rest_framework.decorators import api_view
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from . import serializers, services
from .authentication import CustomUserAuthentication
from .models import Application, User


@api_view(['POST'])
def register_view(request):
    serializer = serializers.RegistrationSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)

    data = serializer.validated_data
    serializer.instance = services.create_user(user_dc=data)
    return Response(serializer.data, status=status.HTTP_201_CREATED)


@api_view(['POST'])
def login_view(request):
    username = request.data.get("username")
    password = request.data.get("password")
    user = authenticate(username=username, password=password)
    if user is None:
        raise exceptions.AuthenticationFailed("Invalid Credentials")

    token = services.create_token(user_id=user.id)
    resp = response.Response()
    resp.set_cookie(key="jwt", value=token, httponly=True)
    resp.data = {"token": token}
    return resp


class AuthMixin(APIView):
    authentication_classes = (CustomUserAuthentication,)
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


class ApplicationList(AuthMixin):
    def post(self, request):
        serializer = serializers.ApplicationCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        if self.request.user.applications.filter(answer_date=None).first():
            return Response({"message": "You already have active application."}, status=status.HTTP_400_BAD_REQUEST)
        serializer.save(user=self.request.user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def get(self, request):
        applications = self.request.user.applications
        serializer = serializers.ApplicationSerializer(applications, many=True)
        return Response(serializer.data)


class ApplicationActive(AuthMixin):
    def get(self, request):
        application = self.request.user.applications.filter(answer_date=None).first()
        if application is None:
            return Response({"message": "You do not have active application."}, status=status.HTTP_204_NO_CONTENT)
        serializer = serializers.ApplicationSerializer(application)
        return Response(serializer.data)


class ApplicationCancel(AuthMixin):
    def post(self, request):
        application = self.request.user.applications.filter(answer_date=None).first()
        if application is None:
            return Response({"message": "You do not have active application."}, status=status.HTTP_204_NO_CONTENT)
        services.set_answer_date(application)
        serializer = serializers.ApplicationSerializer()
        serializer.instance = application
        return Response(serializer.data)


class AdminMixin(APIView):
    authentication_classes = (CustomUserAuthentication,)
    permission_classes = (IsAdminUser,)


class AdminApplicationList(AdminMixin):
    @staticmethod
    def post(request):
        serializer = serializers.AdminApplicationCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(approved=True, is_admin=True)
        services.change_user_debt(serializer.validated_data)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @staticmethod
    def get(request):
        applications = Application.objects.all()
        serializer = serializers.AdminApplicationSerializer(applications, many=True)
        return Response(serializer.data)


class AdminActiveApplicationList(AdminMixin):
    @staticmethod
    def get(request):
        applications = Application.objects.filter(answer_date=None)
        serializer = serializers.ApplicationSerializer(applications, many=True)
        return Response(serializer.data)


class AdminApplicationDetail(AdminMixin):
    @staticmethod
    def get(request, pk):
        application = services.get_application_by_pk(pk)
        serializer = serializers.AdminApplicationSerializer(application)
        return Response(serializer.data)

    @staticmethod
    def delete(request, pk):
        application = services.get_application_by_pk(pk)
        application.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


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


class AdminUserApplicationList(AdminMixin):
    @staticmethod
    def get(request, slug):
        applications = services.get_user_by_slug(slug).applications
        serializer = serializers.ApplicationSerializer(applications, many=True)
        return Response(serializer.data)


class AdminUserActiveApplication(AdminMixin):
    @staticmethod
    def get(request, slug):
        applications = services.get_user_by_slug(slug).applications.filter(answer_date=None)
        serializer = serializers.ApplicationSerializer(applications, many=True)
        return Response(serializer.data)
