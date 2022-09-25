from django.urls import path

from . import views

urlpatterns = [
    path('me/', views.UserDetail.as_view()),
    path('me/applications/', views.ApplicationList.as_view()),
    path('me/pending/', views.get_pending_applications),

    path('register/', views.register_view),

    path('applications/', views.AdminApplicationList.as_view()),
    path('applications/pending/', views.admin_get_pending_applications),
    path('applications/<int:pk>/', views.AdminApplicationDetail.as_view()),

    path('users/', views.user_list_view),
    path('users/<slug:slug>/', views.AdminUserDetail.as_view()),
    path('users/<slug:slug>/applications/', views.user_application_list_view),
    path('users/<slug:slug>/pending/', views.get_user_pending_applications),
]
