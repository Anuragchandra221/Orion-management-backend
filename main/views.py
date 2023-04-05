from django.shortcuts import render
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, permission_classes
from .models import UserAccount
from rest_framework.response import Response
from .serializers import UserSerializer
from django.db.models import Count
from django.conf import settings
from django.contrib.auth.hashers import make_password
from django.core.mail import send_mail

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
def getUser(request):
    users = UserAccount.objects.values('account_type').annotate(count=Count('account_type')).order_by()
    print(users)
    serializer = UserSerializer(users, many=True)

    return Response({
        "admin":users
    })

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
            email=request.data['email'], name=request.data['name'], password=password, account_type="coordinator", dob=request.data['dob'], gender=request.data['gender'],number=request.data['number']
        )
        try:    
            subject = "Congratulation on being the coordinator"
            message = f'Hi {name}, you are now a coordinator in the ORION MANAGEMENT SYSTEM...'
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
    
