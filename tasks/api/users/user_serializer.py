from django.contrib.auth.models import User, Group
from rest_framework import serializers
from api.company.company_model import Profile


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "username", "email", "password"]
        extra_kwargs = {
            "password": {"write_only": True}
        }

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data["username"],
            email=validated_data["email"],
            password=validated_data["password"],
        )

        employee_group = Group.objects.get(name="Employee")
        user.groups.add(employee_group)

        Profile.objects.create(
            user=user,
            company=self.context["company"]
        )

        return user