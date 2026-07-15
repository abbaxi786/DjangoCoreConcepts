from rest_framework.decorators import api_view, permission_classes, parser_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser
from django.shortcuts import get_object_or_404
from django.http import FileResponse

from ..models import WorkPlace, Project, Note, WorkspaceFile
from .serializer import WorkPlaceSerializer, NoteSerializer
from .file_serializer import WorkspaceFileSerializer


@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def WorkPlaceView(request, projectId):
    if request.method == "GET":
        workplaces = WorkPlace.objects.filter(project=projectId)
        serializer = WorkPlaceSerializer(workplaces, many=True)
        return Response({'data': serializer.data, 'status': status.HTTP_200_OK})

    if request.method == "POST":
        project = get_object_or_404(Project, id=projectId)
        serializer = WorkPlaceSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(project=project)
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["GET"])
def CheckWorkPlaceExist(request, projectId):
    exists = WorkPlace.objects.filter(project=projectId).exists()
    if exists:
        room_name = WorkPlace.objects.filter(project=projectId).values_list('room_name', flat=True).first()
        return Response(room_name, status=status.HTTP_200_OK)

    return Response(exists, status=status.HTTP_200_OK)


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def GetNoteOfWorkPlace(request, work_place_name):
    history = Note.objects.filter(work_place__room_name=work_place_name).order_by("-created_at")
    serializer = NoteSerializer(history, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(["POST"])
@parser_classes([MultiPartParser, FormParser])
@permission_classes([IsAuthenticated])
def UploadFile(request, work_place_name):
    workplace = get_object_or_404(WorkPlace, room_name=work_place_name)
    serializer = WorkspaceFileSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save(work_place=workplace, uploaded_by=request.user.username)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def GetWorkspaceFiles(request, work_place_name):

    files = WorkspaceFile.objects.filter(
        work_place__room_name=work_place_name,
        work_place__project__company=request.user.profile.company
    ).order_by("-uploaded_at")

    serializer = WorkspaceFileSerializer(
        files,
        many=True,
        context={"request": request}
    )

    return Response(serializer.data)

@api_view(["DELETE"])
@permission_classes([IsAuthenticated])
def DeleteWorkspaceFile(request, file_id):
    workspace_file = get_object_or_404(WorkspaceFile, id=file_id)
    if workspace_file.file:
        workspace_file.file.delete(save=False)

    workspace_file.delete()
    return Response({"message": "File deleted successfully."}, status=status.HTTP_200_OK)

@api_view(["GET"])
@permission_classes([IsAuthenticated])
def DownloadWorkspaceFile(request, file_id):

    workspace_file = get_object_or_404(
        WorkspaceFile,
        id=file_id
    )

    # Only allow users from the same company
    if workspace_file.work_place.project.company != request.user.profile.company:
        return Response(
            {"message": "Permission denied."},
            status=status.HTTP_403_FORBIDDEN
        )

    return FileResponse(
        workspace_file.file.open("rb"),
        as_attachment=True,
        filename=workspace_file.file.name.split("/")[-1]
    )