from rest_framework import serializers
from ..models import WorkspaceFile

class WorkspaceFileSerializer(serializers.ModelSerializer):
    class Meta:
        model = WorkspaceFile
        fields = "__all__"