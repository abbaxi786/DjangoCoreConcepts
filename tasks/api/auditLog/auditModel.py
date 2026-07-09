from django.db import models
from django.contrib.auth.models import User


class AuditLog(models.Model):

    class Action(models.TextChoices):
        CREATE = ("CREATE", "Create")
        UPDATE = ("UPDATE", "Update")
        DELETE = ("DELETE", "Delete")
        UNAUTHORIZED_ACCESS = ("UNAUTHORIZED_ACCESS", "Unauthorized Access")

    user = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )

    action = models.CharField(
        max_length=30,
        choices=Action.choices
    )

    model_name = models.CharField(max_length=100)

    object_id = models.PositiveIntegerField(
        null=True,
        blank=True
    )

    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user} - {self.action}"