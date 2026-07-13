from rest_framework import serializers
from ..models import WorkPlace



class WorkPlaceSerializer(serializers.ModelSerializer):

    class Meta:
        model = WorkPlace
        fields = "__all__"

    
    
