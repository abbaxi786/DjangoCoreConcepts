from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from django.shortcuts import get_object_or_404
from ..models import WorkPlace,Project,Note
from rest_framework.response import Response
from .serializer import WorkPlaceSerializer,NoteSerializer

@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def WorkPlaceView(request, projectId):
    if request.method == "GET":

        data = WorkPlace.objects.filter(project=projectId)
        serializer = WorkPlaceSerializer(data, many=True)

        return Response({'data': serializer.data, 'status': status.HTTP_200_OK})
    
    if request.method == "POST":

        project = get_object_or_404(Project, id=projectId)
        serializer = WorkPlaceSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save(project=project)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        
        print(serializer.errors) 
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
@api_view(["GET"])
def CheckWorkPlaceExist(request, projectId):

    exists = WorkPlace.objects.filter(
        project=projectId
    ).exists()
    if exists:
        room_name = WorkPlace.objects.filter(project=projectId).values_list('room_name', flat=True).first()
        return Response(room_name, status=status.HTTP_200_OK)

    return Response(exists)

@api_view(["GET"])
@permission_classes([IsAuthenticated])
def GetNoteOfWorkPlace(request, work_place_name):

    history = Note.objects.filter(
        work_place__room_name=work_place_name
    ).order_by("-created_at")

    serializer = NoteSerializer(history, many=True)

    return Response(serializer.data, status=status.HTTP_200_OK)







