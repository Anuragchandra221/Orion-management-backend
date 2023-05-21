from rest_framework import serializers

from .models import UserAccount

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserAccount
        fields = ["name", "register", "email", "number"]

class UserSerializer2(serializers.ModelSerializer):
    class Meta:
        model = UserAccount
        fields = ["name", "register", "email", "number", "gender"]