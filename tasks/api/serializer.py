from .models import Project
from rest_framework import serializers
from .models import Task


class ProjectSerilizers(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = '__all__' 

    def validate_name(self, value):
        if not value or value.strip() == "":
            raise serializers.ValidationError(
                "Name can't be empty."
            )
        return value    

class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = "__all__"
    pass