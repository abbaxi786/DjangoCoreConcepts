from rest_framework.decorators import api_view,permission_classes
from rest_framework import response
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


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def Register(request):
    serializer = UserSerializer(data=request.data,context={'company': request.user.profile.company})
    if serializer.is_valid():
        serializer.save()
        t1 = threading.Thread(target=send_welcome_email, args=(serializer.data['email'], serializer.data['username']))
        t1.start()
        return response.Response({"data":serializer.data, "message": "User registered successfully"}, status=status.HTTP_201_CREATED)
    return response.Response({"errors": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)


class LoginThrottle(AnonRateThrottle):
    scope = "login"


class LoginView(TokenObtainPairView):
    serializer_class = LoginSerializer
    throttle_classes = [LoginThrottle]