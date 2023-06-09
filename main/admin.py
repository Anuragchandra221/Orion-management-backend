from django.contrib import admin
from .models import UserAccount, Project, Tasks, Work, OldProjects, Mark

# Register your models here.
admin.site.register(UserAccount)
admin.site.register(Project)
admin.site.register(Tasks)
admin.site.register(Work)
admin.site.register(OldProjects)
admin.site.register(Mark)