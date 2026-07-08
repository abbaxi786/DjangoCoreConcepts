from rest_framework import serializers
from django.contrib.auth.models import User, Group
from django.db import transaction
from .company_model import Company, Profile


class CompanyRegistrationSerializer(serializers.Serializer):
    company_name = serializers.CharField(max_length=100)
    description = serializers.CharField()

    username = serializers.CharField(source="owner.username", read_only=True)
    email = serializers.EmailField(source="owner.email", read_only=True)

    password = serializers.CharField(write_only=True, required=True)

    @transaction.atomic
    def create(self, validated_data):
        user = User.objects.create_user(
            username=self.initial_data["username"],
            email=self.initial_data["email"],
            password=self.initial_data["password"],
        )

        company = Company.objects.create(
            company_name=validated_data["company_name"],
            description=validated_data["description"],
            owner=user,
        )

        Profile.objects.create(
            user=user,
            company=company,
        )

        admin_group = Group.objects.get(name="Admin")
        user.groups.add(admin_group)

        return company