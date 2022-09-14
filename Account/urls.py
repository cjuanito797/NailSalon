from django.contrib.auth import views as auth_views
from django.urls import path, re_path

from . import views

app_name = 'account'

urlpatterns = [
    re_path (r'^customerView/$', views.customerView, name='customerView'),
    path("", views.home, name="home"),
    path("login/", auth_views.LoginView.as_view(), name="user_login"),
    path("availableTechs/", views.availableTechs, name="availableTechs"),
    path("registration/", views.registration_view.as_view(), name="user_registration"),
    path("contactUs/", views.contactUs, name='contactUs'),
    path("gallery/", views.gallery, name='gallery'),
]
