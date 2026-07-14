from django.contrib import admin
from .models import Project, Task,Message,WorkPlace,Note
from .company.company_model import Company, Profile
from .auditLog.auditModel import AuditLog



class ProjectAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "description", "company", "is_deleted")


admin.site.register(Project, ProjectAdmin)

admin.site.register(WorkPlace)
admin.site.register(Note)

class TaskAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "name",
        "description",
        "due_date",
        "status",
        "completed",
        "assigned_to",
        "project",
        "is_deleted",)
admin.site.register(Task, TaskAdmin)


class CompanyAdmin(admin.ModelAdmin):
    list_display = ("id", "company_name", "description", "owner")


admin.site.register(Company, CompanyAdmin)
admin.site.register(Profile)
admin.site.register(AuditLog)

class MessageAdmin(admin.ModelAdmin):
    list_display = ("id", "room_name", "username", "message", "created_at")
admin.site.register(Message, MessageAdmin)



