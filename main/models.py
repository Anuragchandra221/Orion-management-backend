from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager

# Create your models here.

class UserAccountManager(BaseUserManager):
    def create_user(self, email, name, account_type , gender, number, dob, register, password=None):
        if not email:
            raise ValueError("Users must have an email address")
        
        email = self.normalize_email(email)
        user = self.model(email=email,name=name, account_type=account_type, dob=dob, gender=gender, number=number, register=register)

        user.set_password(password)
        user.save()

        return user

    def create_superuser(self, email, name, account_type , gender, number, dob, register, password=None):
        if not email:
            raise ValueError("Users must have an email address")
        
        email = self.normalize_email(email)
        user = self.model(email=email,name=name, account_type=account_type, dob=dob, gender=gender, number=number, register=register)

        user.set_password(password)
        user.is_superuser = True
        user.save()

        return user



class UserAccount(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(max_length=255, unique=True)
    name = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=True)
    account_type = models.CharField(max_length=50)
    gender = models.CharField(max_length=8)
    dob = models.DateField( auto_now=False, auto_now_add=False)
    number = models.CharField( max_length=50, null=True)
    register = models.CharField(max_length=50, null=True)

    objects = UserAccountManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name','account_type','gender','dob','number','register']

    def __str__(self):
        return self.email