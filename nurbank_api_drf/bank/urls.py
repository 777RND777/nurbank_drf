from django.urls import path

from . import views

urlpatterns = [
    path('register/', views.register_view),
    path('users/', views.user_list_view),
    path('users/<slug:slug>/', views.UserDetail.as_view()),
]
