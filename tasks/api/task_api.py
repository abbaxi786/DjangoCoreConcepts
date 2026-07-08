from django.shortcuts import get_object_or_404
from .models import Task, Project
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from .serializer import TaskSerializer
from .auditLog.auditModel import AuditLog


@api_view(["GET", "POST"])
@permission_classes([IsAuthenticated])
def Tasks(request):

    company = request.user.profile.company

    if request.method == "GET":
        tasks = Task.objects.filter(project__company=company)
        serializer = TaskSerializer(tasks, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    elif request.method == "POST":

        project = get_object_or_404(
            Project,
            id=request.data["project"],
            company=company
        )

        serializer = TaskSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save(project=project)
            AuditLog.objects.create(
                user=request.user,
                action=AuditLog.Action.CREATE,
                model_name="Task",
                object_id=serializer.id
            )
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["GET", "PUT", "PATCH", "DELETE"])
@permission_classes([IsAuthenticated])
def TaskManupulate(request, id):

    company = request.user.profile.company

    task = get_object_or_404(
        Task,
        id=id,
        project__company=company
    )

    if request.method == "GET":
        serializer = TaskSerializer(task)
        return Response(serializer.data, status=status.HTTP_200_OK)

    elif request.method == "PUT":

        serializer = TaskSerializer(task, data=request.data)

        if serializer.is_valid():
            serializer.save()
            AuditLog.objects.create(
                user=request.user,
                action=AuditLog.Action.UPDATE,
                model_name="Task",
                object_id=serializer.id
            )

            return Response(serializer.data, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == "PATCH":

        serializer = TaskSerializer(
            task,
            data=request.data,
            partial=True
        )

        if serializer.is_valid():
            serializer.save()
            AuditLog.objects.create(
                user=request.user,
                action=AuditLog.Action.UPDATE,
                model_name="Task",
                object_id=serializer.id
            )
            return Response(serializer.data, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == "DELETE":

        task.is_deleted = True
        task.save()
        AuditLog.objects.create(
            user=request.user,
            action=AuditLog.Action.DELETE,
            model_name="Task",
            object_id=task.id
        )
        return Response(status=status.HTTP_204_NO_CONTENT)