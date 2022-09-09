from django.contrib.auth import views as auth_views
from django.urls import path, re_path

from . import views

app_name = 'account'

urlpatterns = [
    path("", views.home, name="home"),
    re_path (r'^customerView/$', views.customerView, name='customerView'),
    path("registration/", views.registration_view.as_view(), name="user_registration"),
    path("login/", views.user_login, name="user_login"),
    path("availableTechs/", views.availableTechs, name="availableTechs")
]
