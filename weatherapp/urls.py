import imp
from django.contrib import admin
from django.urls import path
from weatherapp import views

urlpatterns = [
    path("",views.secondfunction),
    path("first",views.firstfunction),
]