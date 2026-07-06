from urllib import request

from django.shortcuts import render
from django.shortcuts import get_object_or_404
from .models import Project
from rest_framework.decorators import api_view , permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from .serializer import ProjectSerilizers



# Create your views here.

@api_view(['GET','POST'])
@permission_classes([IsAuthenticated])
def Home(request):

    if request.method == 'GET':
        data = Project.objects.all()
        serializers1 = ProjectSerilizers(data, many=True)
        return Response(serializers1.data)
    
    if request.method == 'POST':
        serializers = ProjectSerilizers(data = request.data)
        if serializers.is_valid():
            serializers.save()
            return Response(serializers.data, status=status.HTTP_201_CREATED)
        return Response(serializers.errors, status=status.HTTP_400_BAD_REQUEST)
    
@api_view(["GET","DELETE","PUT","PATCH"])
@permission_classes([IsAuthenticated])
def HomeChange(request,id):
   
    foundItem = get_object_or_404(Project,id=id)  

    if request.method == "GET":
        serial = ProjectSerilizers(foundItem)
        return Response(serial.data, status=status.HTTP_200_OK)
    elif request.method == "PUT":
        print(request.data)
        data = ProjectSerilizers(foundItem, data= request.data)
        if data.is_valid():
            data.save()
            return Response({"message":data.data},status= status.HTTP_205_RESET_CONTENT)    
        else:
            return Response(data.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == "DELETE":
        foundItem.delete()
        return Response({"message":"OBJECT IS BEING DELETED"},status= status.HTTP_205_RESET_CONTENT)    

            
    
