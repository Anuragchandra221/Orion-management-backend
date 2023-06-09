from rest_framework import serializers

from .models import UserAccount, Mark

class MarkSerializer(serializers.ModelSerializer):
    class Meta:
        model = Mark
        fields = ['marks']

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserAccount
        fields = ["name", "register", "email", "number" ]

class UserSerializer2(serializers.ModelSerializer):
    class Meta:
        model = UserAccount
        fields = ["name", "register", "email", "number", "gender","account_type"]