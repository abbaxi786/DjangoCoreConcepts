from rest_framework.decorators import api_view
from rest_framework import response
from rest_framework import status
from .user_serializer import UserSerializer


@api_view(['POST'])
def Register(request):
    serializer = UserSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return response.Response({"data":serializer.data, "message": "User registered successfully"}, status=status.HTTP_201_CREATED)
    return response.Response({"errors": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)