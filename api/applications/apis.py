from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.response import Response

from . import serializers, services
from .models import Application
from users import apis as user_apis


class ApplicationList(user_apis.AuthMixin):
    @staticmethod
    def post(request):
        if request.user.applications.filter(answer_date=None).first():
            return Response({'message': 'You already have active application.'}, status=status.HTTP_400_BAD_REQUEST)
        serializer = serializers.ApplicationCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(user=request.user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @staticmethod
    def get(request):
        applications = request.user.applications
        serializer = serializers.ApplicationSerializer(applications, many=True)
        return Response(serializer.data)


class ApplicationActive(user_apis.AuthMixin):
    @staticmethod
    def get(request):
        application = request.user.applications.filter(answer_date=None).first()
        if application is None:
            return Response({'message': 'You do not have active application.'}, status=status.HTTP_204_NO_CONTENT)
        serializer = serializers.ApplicationSerializer(application)
        return Response(serializer.data)


class ApplicationCancel(user_apis.AuthMixin):
    @staticmethod
    def post(request):
        application = request.user.applications.filter(answer_date=None).first()
        if application is None:
            return Response({'message': 'You do not have active application.'}, status=status.HTTP_204_NO_CONTENT)
        services.set_answer_date(application)
        serializer = serializers.ApplicationSerializer()
        serializer.instance = application
        return Response(serializer.data)


class AdminApplicationList(user_apis.AdminMixin):
    @staticmethod
    def post(request):
        serializer = serializers.AdminApplicationCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(approved=True, is_admin=True)
        services.change_user_debt(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @staticmethod
    def get(_):
        applications = Application.objects.all()
        serializer = serializers.AdminApplicationSerializer(applications, many=True)
        return Response(serializer.data)


class AdminActiveApplicationList(user_apis.AdminMixin):
    @staticmethod
    def get(_):
        applications = Application.objects.filter(answer_date=None)
        serializer = serializers.AdminApplicationSerializer(applications, many=True)
        return Response(serializer.data)


class AdminApplicationDetail(user_apis.AdminMixin):
    @staticmethod
    def get(_, pk):
        application = get_object_or_404(Application, pk=pk)
        serializer = serializers.AdminApplicationSerializer(application)
        return Response(serializer.data)

    @staticmethod
    def delete(_, pk):
        application = get_object_or_404(Application, pk=pk)
        application.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class AdminApplicationApprove(user_apis.AdminMixin):
    @staticmethod
    def post(_, pk):
        application = get_object_or_404(Application, pk=pk)
        if application.answer_date:
            return Response({'message': f'Application is not active.'},
                            status=status.HTTP_400_BAD_REQUEST)
        services.approve_application(application)
        serializer = serializers.AdminApplicationSerializer()
        serializer.instance = application
        services.change_user_debt(serializer.data)
        return Response(serializer.data)


class AdminApplicationDecline(user_apis.AdminMixin):
    @staticmethod
    def post(_, pk):
        application = get_object_or_404(Application, pk=pk)
        if application.answer_date:
            return Response({'message': f'Application is not active.'},
                            status=status.HTTP_400_BAD_REQUEST)
        services.set_answer_date(application)
        serializer = serializers.AdminApplicationSerializer()
        serializer.instance = application
        return Response(serializer.data)


class AdminUserApplicationList(user_apis.AdminMixin):
    @staticmethod
    def get(_, slug):
        applications = Application.objects.filter(user__slug=slug)
        serializer = serializers.AdminApplicationSerializer(applications, many=True)
        return Response(serializer.data)


class AdminUserActiveApplication(user_apis.AdminMixin):
    @staticmethod
    def get(_, slug):
        application = Application.objects.filter(user__slug=slug, answer_date=None).first()
        if application is None:
            return Response({'message': f'User {slug} does not have active application.'},
                            status=status.HTTP_204_NO_CONTENT)
        serializer = serializers.AdminApplicationSerializer(application)
        return Response(serializer.data)
