from .models import Project
from rest_framework import serializers


class ProjectSerilizers(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = '__all__' 

    def validate_name(self, data):
        if not data or data.strip()== "":
            raise serializers.ValidationError({"description": "Can't set the name empty"})
        pass