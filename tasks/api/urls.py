from django.urls import path
from . import views
from .task_api import Tasks, TaskManupulate
from .user_api import Register
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)


urlpatterns = [
    path('api/', views.Home),
    path('api_project/<int:id>', views.HomeChange), 
    path('api/tasks/', Tasks),
    path('api/task/<int:id>', TaskManupulate),
    path('api/register/', Register),
    path('api/login/', TokenObtainPairView.as_view()),
    path('api/login/refresh/', TokenRefreshView.as_view()),    
]
