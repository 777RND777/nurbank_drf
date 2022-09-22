from django.urls import path

from . import views

urlpatterns = [
    path('users/', views.UserViewSet.as_view({'get': 'list'})),
]
