from django.db import models
from rest_framework import serializers

# Create your models here.

class Project(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()

    def __str__(self):
        return self.name
    
class Task(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='tasks')
    name = models.CharField(max_length=100)
    description = models.TextField()
    due_date = models.DateField()
    class Status(models.TextChoices):
        PENDING = 'PENDING', 'Pending'
        IN_PROGRESS = 'IN_PROGRESS', 'In Progress'
        COMPLETED = 'COMPLETED', 'Completed'
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.PENDING)
    completed = models.BooleanField(default=False)

    def __str__(self):
        return self.name
