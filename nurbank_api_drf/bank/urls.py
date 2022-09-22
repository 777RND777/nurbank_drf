from django.urls import path

from . import views

urlpatterns = [
    path('register/', views.register_view),
    path('users/', views.user_list_view),
    path('users/<int:pk>/', views.UserDetail.as_view()),
]
