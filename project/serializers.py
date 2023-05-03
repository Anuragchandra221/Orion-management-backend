from rest_framework import serializers

from main.models import Tasks, Project

class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tasks
        fields = ["title", "description", "due_date", "posted"]

class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = ["title", "description"]
