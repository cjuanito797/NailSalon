from django.contrib.auth import views
from django.urls import path

from . import views

app_name = 'manager'

urlpatterns = [
    path('', views.home, name="home"),
    path('attendance/', views.attendance, name="attendance"),
]
