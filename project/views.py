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
from main.models import Project, Tasks, Work, OldProjects
from django.conf import settings
from django.core.files import File
from django.db.models import Q
import cloudinary
import cloudinary.api
from cloudinary import CloudinaryImage
from django.contrib.auth.hashers import make_password
from django.core.mail import send_mail
from datetime import datetime
from django.http import JsonResponse
from django.http import FileResponse
import os
from django.shortcuts import get_object_or_404
from .serializers import TaskSerializer, ProjectSerializer, WorkSerializer, ProjectSerializer2, OldProjectsSerializer, TaskSeializer2
from orion_backend.settings import  MEDIA_ROOT
import json    
from django.http import HttpResponse

import jwt as j

# Create your views here.

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def startProject(request):
    user = request.user
    
    if(user.account_type=="coordinator"):
        project = Project.objects.filter(title=request.data['title']).count()
        if(project>0):
            return Response({"err":"Project Already exists"})
        try:
            project = Project(title=request.data['title'], description=request.data['description'])
            project.save()
        except:
            return Response({"err":"2Something wrong happend"})
        project = Project.objects.get(title=request.data['title'])
        user = UserAccount.objects.get(email=request.data['guide'])
        user.project.add(project)
        user.save()
        if(request.data['student1']):
            user = UserAccount.objects.get(email=request.data['student1'])
            if(user.project.all().count()>1):
                return Response({"err":"The student is already in a project"})
            user.project.add(project)
            user.save()

        if(request.data['student2']):
            user = UserAccount.objects.get(email=request.data['student2'])
            if(user.project.all().count()>1):
                return Response({"err":"The student is already in a project"})
            user.project.add(project)
            user.save()

        if(request.data['student3']):
            user = UserAccount.objects.get(email=request.data['student3'])
            if(user.project.all().count()>1):
                return Response({"err":"The student is already in a project"})
            user.project.add(project)
            user.save()

        if(request.data['student4']):
            user = UserAccount.objects.get(email=request.data['student4'])
            if(user.project.all().count()>1):
                return Response({"err":"The student is already in a project"})
            user.project.add(project)
            user.save()
        return Response({"msg":"Project Added"})
    else:
        return Response({"err":"You don't have the permission"})

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def get_task(request):
    user = request.user
    project = Project.objects.get(title= request.data['project'])
    if (user in project.users.all() and user.account_type=="guide"):
        task = Tasks.objects.get(Q(title=request.data['task']) & Q(project=project))
        serializer = TaskSeializer2(task, many=False)
        return Response(serializer.data)
    else:
        return Response({"err":"You dont have permission"})

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def edit_task(request):
    user = request.user
    project = Project.objects.get(title= request.data['project_title'])
    if (user in project.users.all() and user.account_type=="guide"):
        description = request.data['description']
        due_date = request.data['due_date']
        task = Tasks.objects.get(Q(title=request.data['task']) & Q(project=project))
        task.title=request.data['task_title']
        task.description=description
        task.due_date=due_date
        task.save()
        return Response({"msg":"Edited"})
    else:
        return Response({"err":"You dont have permission"})


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
        try:
            project = Project.objects.get(title=request.data['project_title'])
            try:
                tasks = Tasks.objects.filter(project=project)
            except:
                return Response({"err":"No Tasks found"})
            serializer = ProjectSerializer2(project, many=True)
            return Response(serializer.data)
        except:
            return Response({[]})
    else:
        return Response({"err":"You don't have the permission"})

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def getProject(request):
    user = request.user
    print("HIHI")
    if(user.account_type=="guide" or user.account_type=="student"):
        try:
            project = user.project.all()

            print(project)
        except:
            return Response({"err":"No Project found"})
        serializer = ProjectSerializer2(project, many=True)
        print(serializer.data)
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

@permission_classes([IsAuthenticated])
@api_view(['POST'])
def upload_old_project(request):
    title = request.data['title']
    user = request.user
    if(user.account_type=="admin"):
        pro = Project.objects.filter(title=request.data['title']).count()
        if(pro>0):
            return Response({"err":"1Something wrong happend"})
        
        description = request.data['description']
        files = request.FILES['file']
        guide = request.data['guide']
        std1 = request.data['std1']
        std2 = request.data['std2']
        std3 = request.data['std3']
        std4 = request.data['std4']
        year = request.data['year']
        print(files)
        pro = OldProjects(title=title, description=description, files=files, guide=guide, std1=std1, std2=std2, std3=std3, std4=std4, year=year)
        try:
            pro.save()
            return Response({"msg":"Project added successfully"})
        except:
            return Response({"err": "Something wrong happend"})
    else:
        return Response({"err":"You don't have permission"})
    
@permission_classes([IsAuthenticated])
@api_view(['GET'])
def get_old_project_by_year(request):
    usr = request.user
    if(usr.account_type=="admin" or usr.account_type=="coordinator"):
        year = request.GET['year']
        pro = OldProjects.objects.filter(year=year)
        serializer = OldProjectsSerializer(pro, many=True)
        return Response(serializer.data)
    else:
        return Response({"err":"You don't have permission"})

@permission_classes([IsAuthenticated])
@api_view(['GET'])
def search_old_project(request):
    q = request.GET['q']
    print(q)
    pro = OldProjects.objects.filter(Q(title__icontains=q)|Q(description__icontains=q))
    serializer = OldProjectsSerializer(pro, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def get_old_project(request):
    q = request.GET['q']
    print(q)
    pro = OldProjects.objects.get(title=q)
    print(pro)
    try:
        serializer = OldProjectsSerializer(pro, many=False)
        return Response(serializer.data)
    except:
        print("No data exist")
        return Response({"err": "No data"})

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

# @permission_classes([IsAuthenticated])
@api_view(['POST'])
def get_pdf(request):
    user = request.user or None
    #user in project.users.all() or (user.account_type=="admin" or user.account_type=='coordinator') or
    project = Project.objects.get(title= request.data['project'])
    if (1):
        task = Tasks.objects.get(Q(project=project) & Q(title=request.data['task']))
        work = Work.objects.get(Q(task=task) & Q(files=request.data['file']))

        cloudinary.config(
        cloud_name="ddhojwrtd",
        api_key="395671819399414",
        api_secret="LCEBoX70PRhDKLeUSvrxnskzfJc"
        )

        # print(work.id)
        # file = get_object_or_404(Work, id=work.id)
        # print(file)
        response = cloudinary.api.resource(work.files.name) 
        metadata = dict(response)  
        url = metadata['url']
        string = json.dumps({"file":url})
        js = json.loads(string)  
        print(js)   
        
        return Response({"file":url}, content_type="application/json")
 

    else:    
        return Response({"err":"You dont have permission"})

@api_view(['POST'])
def get_old_pdf(request):
    q = request.data['q']
    pro = OldProjects.objects.get(title=q)
    cloudinary.config(
    cloud_name="ddhojwrtd",
    api_key="395671819399414",
    api_secret="LCEBoX70PRhDKLeUSvrxnskzfJc"
    )

    # print(work.id)
    # file = get_object_or_404(Work, id=work.id)
    # print(file)
    print(pro.files.name)   
    response = cloudinary.api.resource(pro.files.name) 
    metadata = dict(response)  
    url = metadata['url']
    string = json.dumps({"file":url})
    js = json.loads(string)  
    print(js)   
    
    return Response({"file":url}, content_type="application/json")

@permission_classes([IsAuthenticated])   
@api_view(['POST'])
def give_marks(request):
    user = request.user
    project = Project.objects.get(title= request.data['project'])
    if (user in project.users.all() and user.account_type=="guide"):
        task = Tasks.objects.get(Q(project=project) & Q(title=request.data['task']))
        task.score_obtained = request.data['score']
        task.save()
        return Response({"msg":"Score updated"})

    else:
        return Response({"err":"You dont have permission"})

@permission_classes([IsAuthenticated])
@api_view(['POST'])
def view_projects(request):
    user = request.user
    if(user.account_type=="admin" or user.account_type=="coordinator"):
        project = Project.objects.get(title=request.data['title'])
        serializer = ProjectSerializer2(project, many=False)
        return Response(serializer.data)
    else:
        return Response({"err":"You don't have permission"})

@permission_classes([IsAuthenticated])
@api_view(['GET'])
def get_project_names(request):
    user = request.user
    if(user.account_type=="admin" or user.account_type=="coordinator"):
        project = Project.objects.all()
        serializer = ProjectSerializer(project, many=True)
        return Response(serializer.data)
    else:
        return Response({"err":"You don't have permission"})
