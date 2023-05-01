from django.contrib import admin
from .models import UserAccount, Project

# Register your models here.
admin.site.register(UserAccount)
admin.site.register(Project)