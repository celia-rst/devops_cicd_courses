from rest_framework import serializers
from .models import Task

class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        # L'owner n'est pas exposé publiquement via l'API, il est déduit côté serveur
        # fields définit les champs que le serializer expose dans l’API, 
        # à la fois pour recevoir les données et pour construire la réponse.
        fields = ['id', 'title', 'completed']