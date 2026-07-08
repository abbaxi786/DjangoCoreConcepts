from rest_framework.decorators import api_view
from rest_framework import response
from rest_framework import status
from .user_serializer import UserSerializer
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
)
from rest_framework.throttling import AnonRateThrottle
import threading
from api.email.sendEmail import send_welcome_email


@api_view(['POST'])
def Register(request):
    serializer = UserSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        t1 = threading.Thread(target=send_welcome_email, args=(serializer.data['email'], serializer.data['username']))
        t1.start()
        return response.Response({"data":serializer.data, "message": "User registered successfully"}, status=status.HTTP_201_CREATED)
    return response.Response({"errors": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)


class LoginThrottle(AnonRateThrottle):
    scope = "login"


class LoginView(TokenObtainPairView):
    throttle_classes = [LoginThrottle]