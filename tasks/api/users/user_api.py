from rest_framework.decorators import api_view,permission_classes
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from .user_serializer import UserSerializer
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
)
from rest_framework.throttling import AnonRateThrottle
import threading
from api.email.sendEmail import send_welcome_email
from .return_user import LoginSerializer
from api.company.company_model import Profile


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def Register(request):
    if not request.user.groups.filter(name__in=["Manager", "Admin"]).exists():
            return Response(
                {"message": "Only Manager and Admin can create projects."},
                status=status.HTTP_403_FORBIDDEN
            )
    serializer = UserSerializer(data=request.data,context={'company': request.user.profile.company})
    if serializer.is_valid():
        serializer.save()
        t1 = threading.Thread(target=send_welcome_email, args=(serializer.data['email'], serializer.data['username']))
        t1.start()
        return Response({"data":serializer.data, "message": "User registered successfully"}, status=status.HTTP_201_CREATED)
    return Response({"errors": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)


class LoginThrottle(AnonRateThrottle):
    scope = "login"


class LoginView(TokenObtainPairView):
    serializer_class = LoginSerializer
    throttle_classes = [LoginThrottle]

from django.contrib.auth.models import User

@api_view(["GET"])
@permission_classes([IsAuthenticated])
def GetUsersOfCompany(request):

    company = request.user.profile.company

    users = User.objects.filter(
        profile__company=company
    )

    serializer = UserSerializer(users, many=True)

    return Response(serializer.data)