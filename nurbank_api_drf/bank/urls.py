from django.urls import path

from . import views

urlpatterns = [
    path('me/', views.UserDetail.as_view()),
    path('me/applications/', views.ApplicationList.as_view()),

    path('register/', views.register_view),

    path('applications/', views.AdminApplicationList.as_view()),

    path('users/', views.user_list_view),
    path('users/<slug:slug>/', views.AdminUserDetail.as_view()),
    path('users/<slug:slug>/applications/', views.user_application_list_view),
]
