from rest_framework import serializers
from userprojectapp.models import User, Projects, Tasks, Comments


class UserSerializer(serializers.ModelSerializer):
    pk = serializers.IntegerField()

    class Meta:
        model = User
        fields = "__all__"
        
class ProjectSerializer(serializers.ModelSerializer):
    pk = serializers.IntegerField()
    project_owner = UserSerializer()
    class Meta:
        model = Projects
        fields = "__all__"
        
class TasksSerializer(serializers.ModelSerializer):
    pk = serializers.IntegerField()
    project = ProjectSerializer()
    assigned_to=UserSerializer()
    
    class Meta:
        model = Tasks
        fields = "__all__"
        
class CommentsSerializer(serializers.ModelSerializer):
    pk = serializers.IntegerField()
    user = UserSerializer()
    task = TasksSerializer()
    
    class Meta:
        model = Comments
        fields ="__all__"
    