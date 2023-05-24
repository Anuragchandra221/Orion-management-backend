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
    path('get-old-pdf/', views.get_old_pdf),
    path('give-marks/', views.give_marks),
    path('view-projects/', views.view_projects),
    path('view-project-names/', views.get_project_names),
    path('upload-old-project/', views.upload_old_project),
    path('search-old-project/', views.search_old_project),
    path('get-old-project/', views.get_old_project),
    path('retrieve-task/', views.get_task),
    path('edit-task/', views.edit_task),
    path('get-old-project-by-year/', views.get_old_project_by_year),
]

