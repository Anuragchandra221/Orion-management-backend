from django.shortcuts import render
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, permission_classes
from main.models import UserAccount
from rest_framework.response import Response
from main.serializers import UserSerializer,UserSerializer2
from django.db.models import Count
from main.models import Project, Tasks, Work
from django.conf import settings
from django.db.models import Q
from django.contrib.auth.hashers import make_password
from django.core.mail import send_mail
from .serializers import TaskSerializer, ProjectSerializer, WorkSerializer
import jwt as j
# Create your views here.

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def startProject(request):
    user = request.user
    if(user.account_type=="coordinator"):
        project = Project.objects.filter(title=request.data['title']).count()
        if(project>0):
            return Response({"err":"1Something wrong happend"})
        try:
            project = Project(title=request.data['title'], description=request.data['description'])
            project.save()
        except:
            return Response({"err":"2Something wrong happend"})
        project = Project.objects.get(title=request.data['title'])
        user = UserAccount.objects.get(email=request.data['guide'])
        user.project = project
        user.save()
        if(request.data['student1']):
            user = UserAccount.objects.get(email=request.data['student1'])
            user.project = project
            user.save()

        if(request.data['student2']):
            user = UserAccount.objects.get(email=request.data['student2'])
            user.project = project
            user.save()

        if(request.data['student3']):
            user = UserAccount.objects.get(email=request.data['student3'])
            user.project = project
            user.save()

        if(request.data['student4']):
            user = UserAccount.objects.get(email=request.data['student4'])
            user.project = project
            user.save()
        return Response({"msg":"Project Added"})
    else:
        return Response({"err":"You don't have the permission"})

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def createTask(request):
    user = request.user 
    if(user.account_type=="guide"):
        project = Project.objects.get(title=request.data['project_title'])
        task = Tasks.objects.filter(project=project)
        task_title = request.data['task_title']
        for i in task:
            if(i.title == task_title):
                return Response({"err":"A task with similar name already exists.."})

        description = request.data['description']
        due_date = request.data['due_date']
        task = Tasks(title=task_title, description=description, due_date=due_date, project=project)
        try:
            task.save()
            return Response({"msg":"Task added successfully"})
        except:
            return Response({"err":"Something went wrong"})
    else:
        return Response({"err":"You don't have the permission"})

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def showTask(request):
    user = request.user
    if(user.account_type=="guide"):
        project = Project.objects.get(title=request.data['project_title'])
        try:
            tasks = Tasks.objects.filter(project=project)
        except:
            return Response({"err":"No Tasks found"})
        serializer = TaskSerializer(tasks, many=True)
        return Response(serializer.data)
    else:
        return Response({"err":"You don't have the permission"})

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def getProject(request):
    user = request.user
    if(user.account_type=="guide"):
        try:
            project = user.project
        except:
            return Response({"err":"No Project found"})
        serializer = ProjectSerializer(project, many=False)
        return Response(serializer.data)
    else:
        return Response({"err":"You don't have the permission"})

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def uploadWork(request):
    user = request.user
    project = Project.objects.get(title= request.data['project'])
    if (user in project.users.all()):
        files = request.FILES['file']
        try:
            task = Tasks.objects.get(Q(project=project) & Q(title=request.data['task']))
            work = Work(files=files, task=task)
            task.completed = True
            task.save()
            work.save()
            print("hey")
            return Response({"msg": "work added successfully"})
        except:
            return Response({"err": "No such task in that project"})
    else:
        return Response({"err":"You dont have the permission"})

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def getWork(request):
    user = request.user
    project = Project.objects.get(title= request.data['project'])
    if (user in project.users.all()):
        try:
            task = Tasks.objects.get(Q(project=project) & Q(title=request.data['task']))
            work = Work.objects.filter(task=task)
            serializer = WorkSerializer(work, many=True)
            print("hey")
            return Response(serializer.data)
        except:
            return Response({"err": "No such task in that project"})
    else:
        return Response({"err":"You dont have the permission"})

