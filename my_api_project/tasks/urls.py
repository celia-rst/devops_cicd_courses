from django.urls import path
from .views import TaskListCreateAPIView, TaskDetailAPIView


urlpatterns =[
    # Endpoint principal pour lister et créer
    path('api/tasks/', TaskListCreateAPIView.as_view(), name='task-list-create'),
    # Nouvelle route avec capture de l'ID (Primary Key)
    path('api/tasks/<int:pk>/', TaskDetailAPIView.as_view(), name='task-detail'),
]