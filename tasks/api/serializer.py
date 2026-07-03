from .models import Project
from rest_framework import serializers


class ProjectSerilizers(serializers.Serializer):
    id = serializers.IntegerField(read_only = True)
    name = serializers.CharField(max_length=100)
    description = serializers.CharField()  

    