from django.shortcuts import get_object_or_404
from .models import Project
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from .serializer import ProjectSerilizers
from .decorator import CheckUserGroup


@api_view(["GET", "POST"])
@permission_classes([IsAuthenticated])
@CheckUserGroup(["Manager", "Admin", "Employee"])
def Home(request):

    company = request.user.profile.company

    if request.method == "GET":
        projects = Project.objects.filter(company=company)

        serializer = ProjectSerilizers(projects, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)

    elif request.method == "POST":

        if not request.user.groups.filter(name__in=["Manager", "Admin"]).exists():

            return Response(
                {"message": "Only Manager and Admin can create projects."},
                status=status.HTTP_403_FORBIDDEN
            )

        serializer = ProjectSerilizers(data=request.data)

        if serializer.is_valid():

            serializer.save(company=company)

            return Response(
                serializer.data,
                status=status.HTTP_201_CREATED
            )

        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )


@api_view(["GET", "PUT", "PATCH", "DELETE"])
@permission_classes([IsAuthenticated])
@CheckUserGroup(["Manager", "Admin"])
def HomeChange(request, id):

    company = request.user.profile.company

    project = get_object_or_404(
        Project,
        id=id,
        company=company
    )

    if request.method == "GET":

        serializer = ProjectSerilizers(project)

        return Response(
            serializer.data,
            status=status.HTTP_200_OK
        )

    elif request.method == "PUT":

        if not request.user.groups.filter(name="Admin").exists():

            return Response(
                {"message": "Only Admin can update projects."},
                status=status.HTTP_403_FORBIDDEN
            )

        serializer = ProjectSerilizers(
            project,
            data=request.data
        )

        if serializer.is_valid():

            serializer.save()

            return Response(
                serializer.data,
                status=status.HTTP_200_OK
            )

        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )

    elif request.method == "PATCH":

        if not request.user.groups.filter(name="Admin").exists():

            return Response(
                {"message": "Only Admin can update projects."},
                status=status.HTTP_403_FORBIDDEN
            )

        serializer = ProjectSerilizers(
            project,
            data=request.data,
            partial=True
        )

        if serializer.is_valid():

            serializer.save()

            return Response(
                serializer.data,
                status=status.HTTP_200_OK
            )

        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )

    elif request.method == "DELETE":

        if not request.user.groups.filter(name="Admin").exists():

            return Response(
                {"message": "Only Admin can delete projects."},
                status=status.HTTP_403_FORBIDDEN
            )

        project.delete()

        return Response(
            {"message": "Project deleted successfully."},
            status=status.HTTP_204_NO_CONTENT
        )