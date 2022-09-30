from rest_framework.serializers import ModelSerializer

from .models import Application


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
            'request_date': {'read_only': True},
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
            'user': {'required': True},
        }
