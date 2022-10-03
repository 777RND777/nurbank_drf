from rest_framework import status
from rest_framework.response import Response

from . import serializers, services
from .models import Application
from users import apis as user_apis, services as user_services


class ApplicationList(user_apis.AuthMixin):
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


class ApplicationActive(user_apis.AuthMixin):
    def get(self, request):
        application = self.request.user.applications.filter(answer_date=None).first()
        if application is None:
            return Response({"message": "You do not have active application."}, status=status.HTTP_204_NO_CONTENT)
        serializer = serializers.ApplicationSerializer(application)
        return Response(serializer.data)


class ApplicationCancel(user_apis.AuthMixin):
    def post(self, request):
        application = self.request.user.applications.filter(answer_date=None).first()
        if application is None:
            return Response({"message": "You do not have active application."}, status=status.HTTP_204_NO_CONTENT)
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
    def get(request):
        applications = Application.objects.all()
        serializer = serializers.AdminApplicationSerializer(applications, many=True)
        return Response(serializer.data)


class AdminActiveApplicationList(user_apis.AdminMixin):
    @staticmethod
    def get(request):
        applications = Application.objects.filter(answer_date=None)
        serializer = serializers.AdminApplicationSerializer(applications, many=True)
        return Response(serializer.data)


class AdminApplicationDetail(user_apis.AdminMixin):
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


class AdminApplicationApprove(user_apis.AdminMixin):
    @staticmethod
    def post(request, pk):
        application = services.get_application_by_pk(pk)
        if application.answer_date:
            return Response({"message": f"Application is not active."},
                            status=status.HTTP_400_BAD_REQUEST)
        services.approve_application(application)
        serializer = serializers.AdminApplicationSerializer()
        serializer.instance = application
        services.change_user_debt(serializer.data)
        return Response(serializer.data)


class AdminApplicationDecline(user_apis.AdminMixin):
    @staticmethod
    def post(request, pk):
        application = services.get_application_by_pk(pk)
        if application.answer_date:
            return Response({"message": f"Application is not active."},
                            status=status.HTTP_400_BAD_REQUEST)
        services.set_answer_date(application)
        serializer = serializers.AdminApplicationSerializer()
        serializer.instance = application
        return Response(serializer.data)


class AdminUserApplicationList(user_apis.AdminMixin):
    @staticmethod
    def get(request, slug):
        applications = user_services.get_user_by_slug(slug).applications
        serializer = serializers.AdminApplicationSerializer(applications, many=True)
        return Response(serializer.data)


class AdminUserActiveApplication(user_apis.AdminMixin):
    @staticmethod
    def get(request, slug):
        application = user_services.get_user_by_slug(slug).applications.filter(answer_date=None).first()
        if application is None:
            return Response({"message": f"User {slug} does not have active application."},
                            status=status.HTTP_204_NO_CONTENT)
        serializer = serializers.AdminApplicationSerializer(application)
        return Response(serializer.data)
