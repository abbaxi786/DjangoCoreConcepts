from rest_framework.decorators import api_view,permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
# from Django.tasks import api
from .company_serializer import CompanyRegistrationSerializer
import threading
from api.email.sendEmail import send_welcome_email  
from api.company.company_model import Company

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

@api_view(["GET"])
@permission_classes([IsAuthenticated])
def get_companies(request, id):

    if request.method == "GET":
        company = Company.objects.get(id=id)
        serializer = CompanyRegistrationSerializer(company)
        return Response(serializer.data, status=status.HTTP_200_OK)
    pass