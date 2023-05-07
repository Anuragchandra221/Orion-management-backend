from rest_framework import serializers 

from main.models import Tasks, Project, Work

class TaskSerializer(serializers.ModelSerializer):
    works = serializers.StringRelatedField(many=True)
    class Meta:
        model = Tasks
        fields = ["title", "description", "due_date", "posted", "completed", "max_score", "score_obtained", "works"] 

class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = ["title", "description"]

class WorkSerializer(serializers.ModelSerializer):
    files = serializers.FileField()

    class Meta:
        model = Work
        fields = '__all__'   


