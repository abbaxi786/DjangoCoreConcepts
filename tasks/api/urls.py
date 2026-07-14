from django.urls import path
from . import views
from .task_api import Tasks, TaskManupulate, GetProjectTasks
from .users.user_api import Register
from rest_framework_simplejwt.views import (
    TokenRefreshView,
)
from .users.user_api import LoginView
from api.company.company_api import register_company,get_companies
from api.WorkplaceRoute.workplace_api import WorkPlaceView,CheckWorkPlaceExist,GetNoteOfWorkPlace




urlpatterns = [
    path('api/', views.Home),
    path('api_project/<int:id>', views.HomeChange), 
    path('api/tasks/', Tasks),
    path('api/task/<int:id>', TaskManupulate),
    path('api/task_project/<int:project_id>', GetProjectTasks),
    path('api/register/', Register),
    path('api/login/', LoginView.as_view()),
    path('api/login/refresh/', TokenRefreshView.as_view()),    
    path('api/register/company/', register_company),
    path('api/company/<int:id>/', get_companies),
    path('api/workplace/create/<int:projectId>', WorkPlaceView),
    path('api/workplace/check/<int:projectId>',CheckWorkPlaceExist),
    path('api/workplace/note/<str:work_place_name>',GetNoteOfWorkPlace)
]
