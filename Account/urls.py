from django.contrib.auth import views as auth_views
from django.urls import path, re_path

from . import views

app_name = 'account'

urlpatterns = [
    path("", views.home, name="home"),
    path("login/", views.user_login, name="user_login")
]