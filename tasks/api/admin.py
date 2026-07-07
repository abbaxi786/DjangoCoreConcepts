from django.contrib import admin
from .models import Project, Task
from .company.company_model import Company, Profile

admin.site.register(Project)
admin.site.register(Task)
admin.site.register(Company)
admin.site.register(Profile)

# Register your models here.
