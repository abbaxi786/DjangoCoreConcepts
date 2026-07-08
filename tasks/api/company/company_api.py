from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .company_serializer import CompanyRegistrationSerializer
import threading
from api.email.sendEmail import send_welcome_email  

@api_view(["POST"])
def register_company(request):

    serializer = CompanyRegistrationSerializer(
        data=request.data
    )

    if serializer.is_valid():
        serializer.save()
        t1 = threading.Thread(target=send_welcome_email, args=(request.data["email"], request.data["username"]))
        t1.start()

        return Response(
            {
                "message": "Company created successfully.",
                "company": serializer.data
            },
            status=status.HTTP_201_CREATED
        )

    return Response(
        serializer.errors,
        status=status.HTTP_400_BAD_REQUEST
    )