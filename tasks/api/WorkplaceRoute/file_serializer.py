from rest_framework import serializers
from ..models import WorkspaceFile

class WorkspaceFileSerializer(serializers.ModelSerializer):
    file_url = serializers.SerializerMethodField()

    class Meta:
        model = WorkspaceFile
        fields = [
            "id",
            "uploaded_by",
            "file",
            "file_url",
            "uploaded_at",
        ]

    def get_file_url(self, obj):
        request = self.context.get("request")
        if request:
            return request.build_absolute_uri(obj.file.url)
        return obj.file.url