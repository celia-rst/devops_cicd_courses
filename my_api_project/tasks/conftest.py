import pytest
from django.contrib.auth.models import User
from rest_framework.test import APIClient
from .models import Task

@pytest.fixture
def user_password():
    """Fixture simple retournant une chaîne de caractères."""
    return 'a-strong-password'

@pytest.fixture
def user(db, user_password):
    """
    Fixture pour créer et retourner un utilisateur standard.
    Notez qu'elle dépend des fixtures 'user_password' et 'db' (fournie par pytest-django).
    """
    return User.objects.create_user(username='testuser', password=user_password)

@pytest.fixture
def user2(db):
    """Fixture pour créer un second utilisateur dans l'application."""
    return User.objects.create_user(username='otheruser', password='password123')

@pytest.fixture
def api_client():
    """
    Fixture pour créer une instance de client API vierge (non connecté).
    On utilise le APIClient de Django Rest Framework (idéal pour le JSON).
    """
    return APIClient()

@pytest.fixture
def authenticated_client(api_client, user):
    """
    Fixture qui compose d'autres fixtures pour retourner un client API authentifié.
    Nous utilisons force_authenticate (standard DRF) pour une exécution ultra-rapide.
    """
    api_client.force_authenticate(user=user)
    return api_client

@pytest.fixture
def sample_task(user):
    """
    Fixture qui crée et retourne une tâche appartenant à l'utilisateur de la fixture 'user'.
    C'est un pattern courant : les fixtures s'imbriquent comme des briques Lego.
    """
    return Task.objects.create(title="Sample Task", owner=user)