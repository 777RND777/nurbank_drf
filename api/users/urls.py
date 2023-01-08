from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView

from . import views

urlpatterns = [
    path('register', views.register_view),
    path('token', TokenObtainPairView.as_view()),

    path('me', views.UserDetail.as_view()),

    path('users', views.AdminUserList.as_view()),
    path('users/<slug:slug>', views.AdminUserDetail.as_view()),
]
