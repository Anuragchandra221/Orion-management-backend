from django.shortcuts import render
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, permission_classes
from main.models import UserAccount
from rest_framework.response import Response
from main.serializers import UserSerializer,UserSerializer2
from django.db.models import Count
from django.core.mail import send_mail
from main.models import Project, Tasks, Work
from django.conf import settings
from django.db.models import Q
from django.contrib.auth.hashers import make_password
from django.core.mail import send_mail
from datetime import datetime
from django.http import FileResponse
from django.shortcuts import get_object_or_404
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
        if(Tasks.objects.filter(Q(title=request.data['task_title']) & Q(project=project)).exists()):
            return Response({"err":"A task with similar name already exists.."})
        else:
            users = project.users.all()
            for i in users:
                subject = "You have a new Task"
                my_datetime = datetime.strptime(request.data['due_date'][:-1], '%Y-%m-%dT%H:%M')
                new_date = datetime.fromisoformat(my_datetime.strftime('%Y-%m-%d %H:%M'))
                message = f"Hi {i.name}, New Assignment {request.data['task_title']} \n {request.data['description']}  \n Due date: {new_date}"
                send_mail(subject, message, settings.EMAIL_HOST_USER, [i.email])
            description = request.data['description']
            due_date = request.data['due_date']
            task = Tasks(title=request.data['task_title'], description=description, due_date=due_date, project=project)
            try:
                task.save()
                return Response({"msg":"Task added successfully"})
            except:
                return Response({"err":"Something went wrong"})
            return Response({"msg":"Task created successfully"})
    else:
        return Response({"err":"You don't have the permission"})

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def showTask(request):
    user = request.user
    if(user.account_type=="guide" or user.account_type=="student"):
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
    if(user.account_type=="guide" or user.account_type=="student"):
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
        print(files)
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
            return Response(serializer.data)
        except:
            return Response({"err": "No such task in that project"})
    else:
        return Response({"err":"You dont have the permission"})


@api_view(['POST'])
def get_pdf(request):
    task = Tasks.objects.get(Q(project=request.data['project']) & Q(title=request.data['task']))
    work = Work.objects.filter(task=task)
    file = get_object_or_404(work.files)
    response = FileResponse(file, content_type=file.content_type)
    response['Content-Disposition'] = f'inline; filename="{file.name}"'
    return response

