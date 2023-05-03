from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('start/', views.startProject),
    path('create-task/', views.createTask),
    path('get-task/', views.showTask),
    path('get-project/', views.getProject),
]
