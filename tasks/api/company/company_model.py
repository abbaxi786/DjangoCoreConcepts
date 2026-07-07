from django.db import models
from django.contrib.auth.models import User


class Company(models.Model):
    company_name = models.CharField(max_length=100)
    description = models.TextField()

    owner = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="owned_companies"
    )

    def __str__(self):
        return self.company_name


class Profile(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE
    )

    company = models.ForeignKey(
        Company,
        on_delete=models.CASCADE
    )

    def __str__(self):
        return f"{self.user.username} - {self.company.company_name}"