from django.http import HttpResponse
from rest_framework import generics, permissions

from .models import Task
from .serializers import TaskSerializer


# Vue pour lister les tâches et en créer de nouvelles.
class TaskListCreateAPIView(generics.ListCreateAPIView):
    serializer_class = TaskSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        # Ne retourne que les tâches appartenant à l'utilisateur connecté.
        return Task.objects.filter(owner=self.request.user)

    def perform_create(self, serializer):
        # Associe la nouvelle tâche à l'utilisateur connecté.
        serializer.save(owner=self.request.user)


# Vue pour consulter, modifier ou supprimer une tâche.
class TaskDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = TaskSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        # Limite aussi la recherche aux tâches de l'utilisateur connecté.
        return Task.objects.filter(owner=self.request.user)

    # Flake8 va détecter que cette variable n'est jamais utilisée
    def ma_vue(request):
        variable_inutile = "test"
        return HttpResponse("Hello")
