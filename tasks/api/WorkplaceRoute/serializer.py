from rest_framework import serializers
from ..models import WorkPlace,Note



class WorkPlaceSerializer(serializers.ModelSerializer):

    class Meta:
        model = WorkPlace
        fields = "__all__"




class NoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Note
        fields = "__all__"