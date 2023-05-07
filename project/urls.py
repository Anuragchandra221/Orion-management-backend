from django.contrib import admin
from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('start/', views.startProject),
    path('create-task/', views.createTask),
    path('get-task/', views.showTask),
    path('upload-work/', views.uploadWork),
    path('get-work/', views.getWork),
    path('get-project/', views.getProject),
    path('get-pdf/', views.get_pdf),
    path('give-marks/', views.give_marks),
]

