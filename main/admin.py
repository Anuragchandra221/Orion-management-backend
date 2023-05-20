from django.contrib import admin
from .models import UserAccount, Project, Tasks, Work, OldProjects

# Register your models here.
admin.site.register(UserAccount)
admin.site.register(Project)
admin.site.register(Tasks)
admin.site.register(Work)
admin.site.register(OldProjects)