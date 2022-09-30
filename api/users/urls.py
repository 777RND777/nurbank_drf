from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView

from . import apis

urlpatterns = [
    path('register/', apis.register_view),
    path('token/', TokenObtainPairView.as_view()),

    path('me/', apis.UserDetail.as_view()),

    path('users/', apis.AdminUserList.as_view()),
    path('users/<slug:slug>/', apis.AdminUserDetail.as_view()),
]
