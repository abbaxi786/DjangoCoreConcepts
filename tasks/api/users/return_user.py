from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

class LoginSerializer(TokenObtainPairSerializer):

    def validate(self, attrs):
        data = super().validate(attrs)

        company = self.user.profile.company

        data["id"] = self.user.id
        data["username"] = self.user.username
        data["email"] = self.user.email
        data["company"] = {
            "name": company.company_name,
        }

        return data