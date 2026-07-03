from django.shortcuts import render
from django.shortcuts import get_object_or_404
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
    
@api_view(["GET","DELETE","PUT"])
def HomeChange(request,id):
   
   foundItem = get_object_or_404(Project,id=id)  

   if request.method == "GET":
       serial = ProjectSerilizers(foundItem)
       if serial.is_valid():
           return Response({data:serial.data},status=status.HTTP_200_OK)
       else:
            return Response(serial.errors, status=status.HTTP_400_BAD_REQUEST)
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

            
    
