from django.urls import path

from . import views

urlpatterns = [
    path('me/', views.UserDetail.as_view()),
    path('me/applications/', views.ApplicationList.as_view()),
    path('me/pending/', views.PendingList.as_view()),

    path('register/', views.register_view),
    path('login/', views.login_view),

    path('applications/', views.AdminApplicationList.as_view()),
    path('applications/pending/', views.AdminPendingList.as_view()),
    path('applications/<int:pk>/', views.AdminApplicationDetail.as_view()),

    path('users/', views.AdminUserList.as_view()),
    path('users/<slug:slug>/', views.AdminUserDetail.as_view()),
    path('users/<slug:slug>/applications/', views.AdminUserApplicationList.as_view()),
    path('users/<slug:slug>/pending/', views.AdminUserPendingList.as_view()),
]
