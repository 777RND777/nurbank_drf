from rest_framework.permissions import IsAdminUser
from rest_framework.viewsets import ModelViewSet

from .models import User
from .serializers import UserOutputSerializer


class UserViewSet(ModelViewSet):
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserOutputSerializer
    permission_classes = [IsAdminUser]
