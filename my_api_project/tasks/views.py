from rest_framework import generics, permissions
from .models import Task
from .serializers import TaskSerializer

# Vue pour lister (GET) toutes les tâches et en créer (POST) de nouvelles
class TaskListCreateAPIView(generics.ListCreateAPIView):
    serializer_class = TaskSerializer
    permission_classes = [permissions.IsAuthenticated]  # Verrouille l'accès aux utilisateurs connectés

    def get_queryset(self):
        # Sécurité vitale : On ne retourne QUE les tâches appartenant à l'utilisateur qui fait la requête
        return Task.objects.filter(owner=self.request.user)

    def perform_create(self, serializer):
        # Lors du POST, on force l'owner de la tâche à être l'utilisateur faisant la requête
        serializer.save(owner=self.request.user) # DRF crée l’objet Task et appelle sa sauvegarde en base (model.save()).

# Vue pour consulter, modifier ou supprimer une tâche spécifique
class TaskDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = TaskSerializer
    permission_classes =[permissions.IsAuthenticated]

    def get_queryset(self):
        # Même sécurité : on limite la recherche aux tâches de l'utilisateur
        return Task.objects.filter(owner=self.request.user)