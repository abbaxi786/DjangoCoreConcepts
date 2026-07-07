from django.contrib.auth.models import User, Group
from rest_framework import serializers

from .company_model import Company, Profile
from django.db import transaction


class CompanyRegistrationSerializer(serializers.Serializer):

    company_name = serializers.CharField(max_length=100)
    description = serializers.CharField()

    username = serializers.CharField(max_length=150)
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    @transaction.atomic
    def create(self, validated_data):

        user = User.objects.create_user(
            username=validated_data["username"],
            email=validated_data["email"],
            password=validated_data["password"]
        )
        print(f"This is the user {user}")

        company = Company.objects.create(
            company_name=validated_data["company_name"],
            description=validated_data["description"],
            owner=user
        )

        Profile.objects.create(
            user=user,
            company=company
        )

        admin_group = Group.objects.get(name="Admin")
        user.groups.add(admin_group)

        return company