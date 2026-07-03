from django.shortcuts import render
from .models import Project
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .serializer import ProjectSerilizers


# Create your views here.
@api_view(['GET','POST'])
def Home(request):

    if request.method == 'GET':
        data = Project.objects.all()
        serializers1 = ProjectSerilizers(data, many=True)
        return Response(serializers1.data)
    
    if request.method == 'POST':
        print(request.data)
        serializers = ProjectSerilizers(data = request.data)
        if serializers.is_valid():
            serializers.save()
            return Response(serializers.data, status=status.HTTP_201_CREATED)
        return Response(serializers.errors, status=status.HTTP_400_BAD_REQUEST)
