from django.contrib.auth import views as auth_views
from django.urls import path, re_path

from . import views

app_name = 'account'

urlpatterns = [
    path("", views.home, name="home"),
<<<<<<< HEAD
    path("availableTechs", views.availableTechs, name="availableTechs"),
=======
    path("registration/", views.registration_view.as_view(), name="user_registration"),
    path("login/", views.user_login, name="user_login"),
    path("availableTechs", views.availableTechs, name="availableTechs")
>>>>>>> 528aa387078ca6a132ffa581ee78b5c1a0a13164
]