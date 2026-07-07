from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .company_serializer import CompanyRegistrationSerializer

@api_view(["POST"])
def register_company(request):

    serializer = CompanyRegistrationSerializer(
        data=request.data
    )

    if serializer.is_valid():
        company = serializer.save()

        return Response(
            {
                "message": "Company created successfully.",
                "company": company.company_name
            },
            status=status.HTTP_201_CREATED
        )

    return Response(
        serializer.errors,
        status=status.HTTP_400_BAD_REQUEST
    )