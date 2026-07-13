from django.db import models
# Create your models here.

class Project(models.Model):
    name = models.CharField(max_length=100,blank=True)
    description = models.TextField()

    company = models.ForeignKey("Company",on_delete=models.CASCADE)
    is_deleted = models.BooleanField(default=False)


    def __str__(self):
        return self.name
    
class Task(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='tasks')
    name = models.CharField(max_length=100)
    description = models.TextField()
    due_date = models.DateField()
    is_deleted = models.BooleanField(default=False)
    class Status(models.TextChoices):
        PENDING = 'PENDING', 'Pending'
        IN_PROGRESS = 'IN_PROGRESS', 'In Progress'
        COMPLETED = 'COMPLETED', 'Completed'
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.PENDING)
    completed = models.BooleanField(default=False)
    assigned_to = models.ForeignKey('auth.User', on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return self.name
    


class Message(models.Model):
    room_name = models.CharField(max_length=100)
    username = models.CharField(max_length=100)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["created_at"]

class Board(models.Model):
    room_name = models.CharField()
    board_content = models.TextField()

class WorkPlace(models.Model):
    room_name = models.CharField()
    company = models.ForeignKey("Company", on_delete=models.CASCADE)
