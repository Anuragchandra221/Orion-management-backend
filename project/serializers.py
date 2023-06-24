from rest_framework import serializers 
import cloudinary
import cloudinary.api
from main.models import Tasks, Project, Work, OldProjects, Mark, UserAccount
from django.db.models import Q
from main.serializers import UserSerializer2, UserSerializer


class MarkSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    class Meta:
        model = Mark
        fields = ["user", "marks"]

class TaskSerializer(serializers.ModelSerializer):
    works = serializers.StringRelatedField(many=True)
    marks = serializers.SerializerMethodField() 
    class Meta:
        model = Tasks
        fields = ["title", "description", "due_date", "posted", "completed", "max_score", "works", "marks"] 
    def get_marks(self, obj):
        proj = obj.project
        task_ids = obj.id
        user_ids = proj.users.values_list("id", flat=True)
        marks = Mark.objects.filter(Q(assignment=task_ids) & Q(user__in=user_ids))
        mark_serializer = MarkSerializer(marks, many=True)
        return mark_serializer.data
    

class TaskSeializer2(serializers.ModelSerializer):
    class Meta:
        model = Tasks
        fields = "__all__"

class OldProjectsSerializer(serializers.ModelSerializer):
    class Meta:
        model = OldProjects
        fields = "__all__"



class ProjectSerializer(serializers.ModelSerializer):
    users = UserSerializer2(many=True, read_only=True)
    tasks = TaskSerializer(many=True, read_only=True)
    class Meta:
        model = Project
        fields = ["title", "description", "users", "tasks"]

class ProjectSerializer2(serializers.ModelSerializer):
    users = UserSerializer2(many=True, read_only=True)
    tasks = TaskSerializer(many=True, read_only=True)
    
    class Meta:
        model = Project
        fields = ["title", "description", "tasks", "users"]
    


class WorkSerializer(serializers.ModelSerializer):
    files = serializers.FileField()

    class Meta:
        model = Work
        fields = '__all__'   

    def to_representation(self, instance):
        representation = super().to_representation(instance)

        # Fetch the metadata for the image
        metadata = cloudinary.api.resource(instance.files.public_id)

        # Access the image's MIME type
        filename = metadata["filename"]
        extension = metadata['format']

        # Set the MIME type in the representation
        representation['filename'] = filename
        representation['extension'] = extension

        return representation




