from django.urls import path
from . import views
from .task_api import Tasks, TaskManupulate

urlpatterns = [
    path('api/', views.Home),
    path('api_project/<int:id>', views.HomeChange), 
    path('api/tasks/', Tasks),
    path('api/task/<int:id>', TaskManupulate)
]
