from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import User
from .serializers import UserCreateSerializer, UserOutputSerializer


class UserView(APIView):
    @staticmethod
    def get(request):
        user = User.objects.all().order_by('-date_joined')
        serializer = UserOutputSerializer(user, many=True)
        return Response(serializer.data)

    @staticmethod
    def post(request):
        serializer = UserCreateSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
