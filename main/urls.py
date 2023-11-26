from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("jdeval", views.jdeval, name="jdeval"),
    path("cvranker", views.cvranker, name="cvranker"),
    path("qualified", views.jdeval, name="jdeval")
]
