from rest_framework import serializers 
import cloudinary
import cloudinary.api
from main.models import Tasks, Project, Work, OldProjects
from main.serializers import UserSerializer2

class TaskSerializer(serializers.ModelSerializer):
    works = serializers.StringRelatedField(many=True)
    class Meta:
        model = Tasks
        fields = ["title", "description", "due_date", "posted", "completed", "max_score", "score_obtained", "works"] 

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
    class Meta:
        model = Project
        fields = ["title", "description", "users"]

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




