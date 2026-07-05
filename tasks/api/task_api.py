from django.shortcuts import get_object_or_404
from .models import Task
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .serializer import TaskSerializer

@api_view(['GET',"POST"])
def Tasks(request):
    if request.method == "GET":
        data = Task.objects.all()
        serilized = TaskSerializer(data, many= True)
        return Response(serilized.data,status= status.HTTP_200_OK)
    if request.method == "POST":
        body = request.data
        serilized = TaskSerializer(data= body)
        if serilized.is_valid():
            serilized.save()
            return Response(serilized.data,status=status.HTTP_201_CREATED)
        else: return Response(serilized.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET','PUT','DELETE',"PATCH"])
def TaskManupulate(request,id):
    if request.method == "GET":
        foundItem = get_object_or_404(Task,id=id)
        serilized = TaskSerializer(foundItem)
        return Response(serilized.data,status=status.HTTP_200_OK)
    elif request.method == "PUT":
        foundItem = get_object_or_404(Task,id=id)
        serilized = TaskSerializer(foundItem, data= request.data)
        if serilized.is_valid():
            serilized.save()
            return Response(serilized.data,status=status.HTTP_205_RESET_CONTENT)
        else: return Response(serilized.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == "DELETE":
        foundItem = get_object_or_404(Task,id=id)
        foundItem.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    elif request.method == "PATCH":
        foundItem = get_object_or_404(Task,id=id)
        serilized = TaskSerializer(foundItem, data= request.data, partial=True)
        if serilized.is_valid():
            serilized.save()
            return Response(serilized.data,status=status.HTTP_205_RESET_CONTENT)
        else: return Response(serilized.errors, status=status.HTTP_400_BAD_REQUEST)




