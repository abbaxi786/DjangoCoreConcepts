from django.db import models
from django.contrib.auth.models import User


class AuditLog(models.Model):

    class Action(models.TextChoices):
        CREATE = ('CREATE','Create')
        UPDATE = ('UPDATE','Update')
        DELETE = ('DELETE','Delete')

    
    user = models.ForeignKey(User,on_delete=models.SET_NULL, null=True)

    actions = models.CharField(
        max_length=20,
        choices= Action.choices
    )

    modelName = models.CharField(max_length=100)

    objectId = models.PositiveIntegerField()

    timestamp = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return f"{self.user} - {self.action}"
