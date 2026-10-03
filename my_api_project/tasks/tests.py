from django.test import TestCase
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from .models import Task
from rest_framework.test import APITestCase
from rest_framework import status

# `TestCase` → met en place une base de données de test jetable, recréée avant chaque test.
class TaskModelTests(TestCase):

    def test_task_creation(self):
        """
        Vérifie la création d'une tâche et ses valeurs par défaut (cas heureux).
        """
        # `create_user` crée un utilisateur en gérant correctement le hachage du mot de passe.
        user = User.objects.create_user(username='testuser', password='password123')

        # `create` enregistre directement l'instance dans la BDD.
        task = Task.objects.create(title="A new task", owner=user)

        # Assertions pour vérifier que les champs correspondent à ce qu’on attend.
        self.assertEqual(task.title, "A new task")   # le titre est correct
        self.assertFalse(task.completed)             # par défaut, completed = False
        self.assertEqual(task.owner, user)           # le propriétaire est correct
        self.assertEqual(str(task), "A new task")    # __str__ renvoie bien le titre. Quand on écrit str(task), Python appelle task.__str__() définie dans le modèle Task et renvoie le texte défini par son return

    def test_task_requires_title(self):
        """
        Vérifie que la validation du modèle échoue si le titre est vide (cas d'erreur).
        """
        user = User.objects.create_user(username='anotheruser', password='password123')

        # Ici on instancie la tâche sans la sauvegarder en base.
        task = Task(title="", owner=user)

        # full_clean() lance les validations strictes définies dans le modèle (blank=False).
        # Comme "title" est vide, on s’attend à ce que Django lève une ValidationError.
        # Le gestionnaire "with self.assertRaises" vérifie que cette erreur survient bien.
        with self.assertRaises(ValidationError):
            task.full_clean()

        # Pourquoi full_clean() ? La méthode .save() de Django ne valide pas toujours tous les champs avant d'écrire en base (selon le type de base de données). Appeler .full_clean() dans un test est la garantie absolue de déclencher les validateurs de modèle (comme blank=False, les validateurs d'email, de longueur, etc.). 

    def test_mark_as_complete_method(self):
        # On prépare la donnée
        user = User.objects.create_user(username='tester', password='pwd')
        task = Task.objects.create(title="Incomplete task", owner=user)

        # On appelle la méthode métier que l'on veut tester
        task.mark_as_complete()

        # On recharge obligatoirement l'objet depuis la base de données 
        # pour s'assurer que le .save() a bien fonctionné
        task.refresh_from_db()

        # On vérifie le résultat
        self.assertTrue(task.completed)

class TaskAPITests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="testuser", password="password123",)
        self.task = Task.objects.create(title="A task", owner=self.user)
        self.client.force_authenticate(user=self.user)

    def test_update_task(self):
        """Vérifie qu'un utilisateur peut mettre à jour sa propre tâche (PUT)."""
        update_data = {"title": "Updated Title", "completed": True}
        response = self.client.put(
            f'/api/tasks/{self.task.id}/',
            data=update_data,
            format='json'
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Ne jamais oublier de rafraîchir l'objet local avant de le vérifier
        self.task.refresh_from_db()
        self.assertEqual(self.task.title, "Updated Title")
        self.assertTrue(self.task.completed)

    def test_delete_task(self):
        """Vérifie qu'un utilisateur peut supprimer sa tâche (DELETE)."""
        response = self.client.delete(f'/api/tasks/{self.task.id}/')

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Task.objects.count(), 0)

    def test_user_cannot_access_other_users_task(self):
        """Sécurité : Vérifie l'isolation des ressources."""
        other_user = User.objects.create_user(username='otheruser', password='password123')
        other_task = Task.objects.create(title="Other User's Task", owner=other_user)

        # Le client (testuser) tente d'accéder à la tâche de other_user
        response = self.client.get(f'/api/tasks/{other_task.id}/')

        # Le queryset filtrant sur self.request.user, Django ne trouve pas la tâche,
        # il renvoie donc un 404 (ce qui empêche d'indiquer si la tâche existe ou non à un attaquant).
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

class TaskUnauthenticatedTests(APITestCase):

    def test_list_tasks_unauthenticated(self):
        """Vérifie que l'API est protégée contre les anonymes."""
        # Notez que nous n'avons PAS utilisé force_authenticate() ici !
        response = self.client.get('/api/tasks/')

        # Avec DRF et SessionAuthentication, un accès non autorisé retourne 403 Forbidden. 
        # (Il retournerait 401 avec TokenAuthentication).
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

######### Explication test API (ex. avec PUT) #########
# 1. Préparer la tâche
# Dans setUp(), le test crée un utilisateur et une tâche :
# self.task = Task.objects.create(title="A task", owner=self.user)
# Ici, le test utilise directement le modèle Task pour enregistrer la tâche en base. Le serializer n’intervient pas encore. Django donne à la tâche un identifiant, par exemple 5.

# 2. Construire et envoyer la requête
# update_data = {"title": "Updated Title", "completed": True}
# response = self.client.put(
#     f'/api/tasks/{self.task.id}/',
#     data=update_data,
#     format='json'
# )
# L’adresse devient, par exemple, /api/tasks/5/. self.client.put(...) envoie à cette adresse les nouvelles valeurs de la tâche.

# 3. Trouver la view
# Dans tasks/urls.py, cette adresse correspond à la view TaskDetailAPIView. Cette view hérite de RetrieveUpdateDestroyAPIView, qui sait gérer la consultation, la modification et la suppression d’une tâche.

# 4. Trouver la bonne tâche avec le modèle
# La view appelle get_queryset(), qui utilise :
# Task.objects.filter(owner=self.request.user)
# Django cherche les tâches appartenant à l’utilisateur connecté. Puis DRF utilise le pk de l’adresse (5) pour trouver la tâche précise parmi elles. Le modèle représente cette tâche et ses champs en base.

# 5. Valider et enregistrer avec le serializer
# Pour le PUT, DRF passe la tâche existante et les nouvelles données au TaskSerializer. Celui-ci vérifie les champs autorisés (title, completed), puis DRF enregistre les nouvelles valeurs sur le modèle. owner ne change pas : le serializer ne l'expose pas et les données envoyées ne le contiennent pas.

# 6. Vérifier le résultat
# DRF renvoie une réponse, attendue avec le statut 200 OK. Puis le test fait :
# self.task.refresh_from_db()
# Cela recharge la tâche depuis la base. Les assertions vérifient alors que title vaut "Updated Title" et que completed vaut True.

# En une phrase : le test envoie les données, la view trouve la tâche de l’utilisateur, le serializer valide les changements, Django les enregistre via le modèle, puis le test vérifie la base. Les étapes apparaissent dans tests.py, views.py, serializers.py et urls.py.