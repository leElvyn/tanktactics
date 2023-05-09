from django.urls import path
from auth import views
import auth

urlpatterns = [
    path('users/me', views.get_self),
    path("debug/autologin", views.autologin)
]