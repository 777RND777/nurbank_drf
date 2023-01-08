from django.urls import path

from . import views

urlpatterns = [
    path('me/applications', views.ApplicationList.as_view()),
    path('me/active', views.ApplicationActive.as_view()),
    path('me/cancel', views.ApplicationCancel.as_view()),

    path('applications', views.AdminApplicationList.as_view()),
    path('applications/active', views.AdminActiveApplicationList.as_view()),
    path('applications/<int:pk>', views.AdminApplicationDetail.as_view()),
    path('applications/<int:pk>/approve', views.AdminApplicationApprove.as_view()),
    path('applications/<int:pk>/decline', views.AdminApplicationDecline.as_view()),

    path('users/<slug:slug>/applications', views.AdminUserApplicationList.as_view()),
    path('users/<slug:slug>/active', views.AdminUserActiveApplication.as_view()),
]
