from django.db import models
from django.contrib.auth.models import User

# cours unittest
# class Task(models.Model): 
#     # models.Model est la classe de base pour tous les modèles Django. 
#     # Elle fournit des fonctionnalités pour interagir avec la base de données 
#     # comme save(), delete(), et des méthodes pour effectuer des requêtes.
#     title = models.CharField(max_length=200, blank=False)
#     completed = models.BooleanField(default=False)

#     # Lien avec l'utilisateur propriétaire de la tâche.
#     # related_name='tasks' permet d'accéder à toutes les tâches d'un user via user.tasks.all()
#     owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='tasks')

#     # Fonction qui définit comment un objet du modèle s’affiche sous forme de texte
#     def __str__(self):
#         # Affichage lisible de l'objet (utile dans l'admin ou les logs d'erreurs de tests)
#         return self.title

#     def mark_as_complete(self):
#         """Marque la tâche comme terminée et la sauvegarde immédiatement."""
#         self.completed = True
#         self.save()

# cours pytest
class TaskManager(models.Manager):
    """Un manager personnalisé pour les tâches."""
    def completed(self):
        """Retourne uniquement les tâches complétées."""
        return self.get_queryset().filter(completed=True)

class Task(models.Model):
    """Représente une tâche dans la to-do list."""
    title = models.CharField(max_length=200, blank=False)
    completed = models.BooleanField(default=False)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='tasks')
    objects = TaskManager() # Attachement du manager personnalisé

    def __str__(self):
        """Retourne le titre de la tâche pour une représentation lisible."""
        return self.title

    def mark_as_complete(self):
        """Marque la tâche comme terminée et la sauvegarde."""
        self.completed = True
        self.save()