from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView

from . import apis

urlpatterns = [
    path('me/', apis.UserDetail.as_view()),
    path('me/applications/', apis.ApplicationList.as_view()),
    path('me/active/', apis.ApplicationActive.as_view()),
    path('me/cancel/', apis.ApplicationCancel.as_view()),

    path('register/', apis.register_view),
    path('token/', TokenObtainPairView.as_view()),

    path('applications/', apis.AdminApplicationList.as_view()),
    path('applications/active/', apis.AdminActiveApplicationList.as_view()),
    path('applications/<int:pk>/', apis.AdminApplicationDetail.as_view()),
    path('applications/<int:pk>/approve/', apis.AdminApplicationApprove.as_view()),
    path('applications/<int:pk>/decline/', apis.AdminApplicationDecline.as_view()),

    path('users/', apis.AdminUserList.as_view()),
    path('users/<slug:slug>/', apis.AdminUserDetail.as_view()),
    path('users/<slug:slug>/applications/', apis.AdminUserApplicationList.as_view()),
    path('users/<slug:slug>/active/', apis.AdminUserActiveApplication.as_view()),
]
