from django.shortcuts import render
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, permission_classes
from .models import UserAccount
from rest_framework.response import Response
from .serializers import UserSerializer,UserSerializer2
from django.db.models import Count
from django.db.models import Q
from django.conf import settings
from django.contrib.auth.hashers import make_password
from django.core.mail import send_mail
import jwt as j

class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        # Add custom claims
        token['name'] = user.name
        token['email'] = user.email
        token['account_type'] = user.account_type
        # ...

        return token

class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer

# Create your views here.
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_count(request):
    users = UserAccount.objects.values('account_type').annotate(count=Count('account_type')).order_by()
    print(users)
    serializer = UserSerializer(users, many=True)

    return Response({
        "admin":users
    })

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def getCoordinator(request):
    coordinator = UserAccount.objects.filter(account_type="coordinator")
    serializer = UserSerializer(coordinator, many=True)

    return Response(serializer.data)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def getGuide(request):
    guide = UserAccount.objects.filter(account_type="guide")
    serializer = UserSerializer(guide, many=True)

    return Response(serializer.data)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def getStudent(request):
    usr = request.user
    if(usr.account_type=="guide"):
        project = usr.project.all()
        print(project)
        std = UserAccount.objects.filter(Q(project__in=project) & Q(account_type="student"))
        serializer = UserSerializer(std, many=True)
        return Response(serializer.data)
    else:
        guide = UserAccount.objects.filter(account_type="student")
        serializer = UserSerializer(guide, many=True)
        return Response(serializer.data)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def getUser(request):

    user = UserAccount.objects.filter(email=request.data['email'])
    serializer = UserSerializer2(user, many=True)
    print(serializer.data)

    return Response(serializer.data)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_coordinator(request):
    user = request.user
    if(user.account_type=="admin"):
        email = request.data['email']
        name = request.data['name']
        usr = UserAccount.objects.filter(email=email).count()
        if (usr>=1):
            return Response({"err":"Coordinator already exists"})
        password = make_password(request.data['password'])
        user = UserAccount(
            email=request.data['email'], name=request.data['name'], password=password, account_type="coordinator", gender=request.data['gender'],number=request.data['number'], register=request.data['register']
        )
        try:    
            subject = "Congratulation on being the coordinator"
            password = request.data['password']
            message = f'Hi {name}, you are now a coordinator in the ORION MANAGEMENT SYSTEM...\nSign In with the following credentials\nUsername: {email}\nPassword: {password}'
            send_mail(subject, message, settings.EMAIL_HOST_USER, [email])
            try:
                user.save()
                return Response({"msg":"coordinator added successfully"})
            except:
                return Response({"err":"Mail not sent"})
        except:
            return Response({"err":"Invalid data"})
    else:
        return Response({"err":"You dont have the permission"})

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_guide(request):
    user = request.user
    if(user.account_type=="coordinator"):
        email = request.data['email']
        name = request.data['name']
        usr = UserAccount.objects.filter(email=email).count()
        if (usr>=1):
            return Response({"err":"Guide already exists"})
        password = make_password(request.data['password'])
        user = UserAccount(
            email=request.data['email'], name=request.data['name'], password=password, account_type="guide", gender=request.data['gender'],number=request.data['number'], register=request.data['register']
        )
        try:    
            subject = "Congratulation on being the guide"
            password = request.data['password']
            message = f'Hi {name}, you are now a guide in the ORION MANAGEMENT SYSTEM...\nSign In with the following credentials\nUsername: {email}\nPassword: {password}'
            send_mail(subject, message, settings.EMAIL_HOST_USER, [email])
            try:
                user.save()
                return Response({"msg":"guide added successfully"})
            except:
                return Response({"err":"Mail not sent"})
        except:
            return Response({"err":"Invalid data"})
    else:
        return Response({"err":"You dont have the permission"})

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_student(request):
    user = request.user
    if(user.account_type=="coordinator"):
        email = request.data['email']
        name = request.data['name']
        usr = UserAccount.objects.filter(email=email).count()
        if (usr>=1):
            return Response({"err":"Student already exists"})
        password = make_password(request.data['password'])
        user = UserAccount(
            email=request.data['email'], name=request.data['name'], password=password, account_type="student", gender=request.data['gender'],number=request.data['number'], register=request.data['register']
        )
        try:    
            subject = "Congratulation on being the Student"
            password = request.data['password']
            message = f'Hi {name}, you are now a Student in the ORION MANAGEMENT SYSTEM...\nSign In with the following credentials\nUsername: {email}\nPassword: {password}'
            send_mail(subject, message, settings.EMAIL_HOST_USER, [email])
            try:
                user.save()
                return Response({"msg":"student added successfully"})
            except:
                return Response({"err":"Mail not sent"})
        except:
            return Response({"err":"Invalid data"})
    else:
        return Response({"err":"You dont have the permission"})

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def edit(request):
    user = request.user
    if(user.account_type=="admin"):
        print(request.data, user.account_type)
        print("admin")
        UserAccount.objects.filter(email=request.data['email']).update(email=request.data['email'], name=request.data['name'], gender=request.data['gender'],number=request.data['number'], register=request.data['register'])
        # try:
        # except Exception as e:
        #     print(e)
        return Response({"msg":"updated successfully"})
    else:
        return Response({"err":"you dont have the permission"})

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def edit_guide(request):
    user = request.user
    if(user.account_type=="coordinator"):
        UserAccount.objects.filter(email=request.data['email']).update(email=request.data['email'], name=request.data['name'], gender=request.data['gender'],number=request.data['number'], register=request.data['register'])
        return Response({"msg":"updated successfully"})
    else:
        return Response({"err":"you dont have the permission"})




@api_view(['POST'])
def reset_password_confirm(request):
    email = request.data['email']
    usr = UserAccount.objects.filter(email=email).count()
    if (usr<1):
        return Response({"err":"Email doesnt exists"})
    encoded = j.encode({"email": email}, "secret", algorithm="HS256")
    link = f"https://orionmanagement.netlify.app/forgot_password/{encoded}"
    subject = "Reset your password"
    message = f'Hi , Reset your password at {link}'
    send_mail(subject, message, settings.EMAIL_HOST_USER, [email])
    return Response({"msg":"You have a mail"})

@api_view(['POST'])
def reset_password(request):
    email = request.data['email']
    usr = UserAccount.objects.filter(email=email).count()
    if (usr<1):
        return Response({"err":"Email doesnt exists"})
    password = make_password(request.data['password'])
    UserAccount.objects.filter(email=email).update(password=password)
    return Response({"msg":"Password changed successfully"})
