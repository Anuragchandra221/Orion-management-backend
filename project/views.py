from django.shortcuts import render
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, permission_classes
from main.models import UserAccount
from rest_framework.response import Response
from main.serializers import UserSerializer,UserSerializer2
from django.db.models import Count
from main.models import Project
from django.conf import settings
from django.contrib.auth.hashers import make_password
from django.core.mail import send_mail
import jwt as j
# Create your views here.

@api_view(['POST'])
# @permission_classes([IsAuthenticated])
def startProject(request):
    project = Project.objects.filter(title=request.data['title']).count()
    if(project>1):
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