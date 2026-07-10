from django.urls import path
from . import views
from .task_api import Tasks, TaskManupulate
from .users.user_api import Register
from rest_framework_simplejwt.views import (
    TokenRefreshView,
)
from .users.user_api import LoginView
from api.company.company_api import register_company,get_companies



urlpatterns = [
    path('api/', views.Home),
    path('api_project/<int:id>', views.HomeChange), 
    path('api/tasks/', Tasks),
    path('api/task/<int:id>', TaskManupulate),
    path('api/register/', Register),
    path('api/login/', LoginView.as_view()),
    path('api/login/refresh/', TokenRefreshView.as_view()),    
    path('api/register/company/', register_company),
    path('api/company/<int:id>/', get_companies),
]
