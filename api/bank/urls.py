from django.urls import path

from . import apis

urlpatterns = [
    path('me/', apis.UserDetail.as_view()),
    path('me/applications/', apis.ApplicationList.as_view()),
    path('me/pending/', apis.PendingList.as_view()),

    path('register/', apis.register_view),
    path('login/', apis.login_view),

    path('applications/', apis.AdminApplicationList.as_view()),
    path('applications/pending/', apis.AdminPendingList.as_view()),
    path('applications/<int:pk>/', apis.AdminApplicationDetail.as_view()),

    path('users/', apis.AdminUserList.as_view()),
    path('users/<slug:slug>/', apis.AdminUserDetail.as_view()),
    path('users/<slug:slug>/applications/', apis.AdminUserApplicationList.as_view()),
    path('users/<slug:slug>/pending/', apis.AdminUserPendingList.as_view()),
]
