import pytest
from rest_framework import status
from django.urls import reverse
from .models import Task
from django.contrib.auth.models import User

# On autorise l'accès à la DB pour tout le fichier
pytestmark = pytest.mark.django_db

def test_get_tasks_unauthenticated(api_client):
    """Vérifie qu'un utilisateur non authentifié reçoit une erreur 403 (ou 401)."""
    # ARRANGE: L'URL de notre endpoint, générée dynamiquement avec reverse()
    url = reverse('task-list-create')

    # ACT: On utilise le client VIERGE (non connecté) via la fixture
    response = api_client.get(url)

    # ASSERT
    assert response.status_code in[status.HTTP_401_UNAUTHORIZED, status.HTTP_403_FORBIDDEN]

def test_create_task(authenticated_client, user):
    """Vérifie qu'un utilisateur authentifié peut créer une tâche."""
    # ARRANGE
    url = reverse('task-list-create')
    task_data = {"title": "A new task from API"}

    # ACT: On utilise le client CONNECTÉ. 
    # format='json' demande au client DRF d'encoder proprement le dictionnaire en JSON.
    response = authenticated_client.post(url, data=task_data, format='json')

    # ASSERT
    assert response.status_code == status.HTTP_201_CREATED
    assert Task.objects.count() == 1

    # On vérifie que la base a bien enregistré la donnée avec le bon owner
    task = Task.objects.first()
    assert task.title == "A new task from API"
    assert task.owner == user

def test_list_user_tasks(authenticated_client, sample_task):
    """Vérifie que la liste des tâches ne contient que celles de l'utilisateur."""
    # ARRANGE: On crée un utilisateur tiers et une tâche qui lui appartient
    other_user = User.objects.create_user(username='other')
    Task.objects.create(title="Other user's task", owner=other_user)

    url = reverse('task-list-create')

    # ACT
    response = authenticated_client.get(url)

    # ASSERT
    assert response.status_code == status.HTTP_200_OK

    # La réponse ne doit contenir qu'UN seul élément (la 'sample_task' de l'utilisateur principal)
    assert len(response.data) == 1
    assert response.data[0]['title'] == sample_task.title

def test_update_task(authenticated_client, sample_task):
    """Vérifie la mise à jour partielle via l'API (PATCH)."""
    url = reverse('task-detail', kwargs={'pk': sample_task.pk})
    update_data = {"title": "Updated Title", "completed": True}

    response = authenticated_client.patch(url, data=update_data, format='json')

    assert response.status_code == status.HTTP_200_OK
    sample_task.refresh_from_db()
    assert sample_task.title == "Updated Title"
    assert sample_task.completed is True

def test_delete_task(authenticated_client, sample_task):
    """Vérifie la suppression d'une ressource (DELETE)."""
    url = reverse('task-detail', kwargs={'pk': sample_task.pk})

    response = authenticated_client.delete(url)

    assert response.status_code == status.HTTP_204_NO_CONTENT
    assert Task.objects.filter(pk=sample_task.pk).count() == 0

# La magie de Pytest : on passe un tableau de méthodes HTTP à tester !
@pytest.mark.parametrize("http_method", ["get", "patch", "delete"])
def test_user_cannot_access_other_user_task(authenticated_client, user2, http_method):
    """
    Factorise le test de permission d'isolation pour GET, PATCH et DELETE.
    """
    # 1. On attribue la ressource au second utilisateur
    other_task = Task.objects.create(title="Other User's Task", owner=user2)
    url = reverse('task-detail', kwargs={'pk': other_task.pk})

    # 2. Prépare les données pour la méthode PATCH (les autres méthodes l'ignoreront)
    kwargs = {}
    if http_method == "patch":
        kwargs['data'] = {"title": "hacked"}
        kwargs['format'] = 'json'

    # 3. Utilise getattr pour appeler dynamiquement la méthode du client
    # L'équivalent de faire `authenticated_client.get(...)` ou `.patch(...)`
    method_to_call = getattr(authenticated_client, http_method)
    response = method_to_call(url, **kwargs)

    # 4. Le testeur est bloqué ! L'API renvoie 404 (non trouvée pour lui)
    assert response.status_code == status.HTTP_404_NOT_FOUND

# On définit le nom des variables injectées ("input_title", "expected_status")
# puis on passe un tableau de tuples contenant les valeurs pour chaque scénario.
@pytest.mark.parametrize(
    "input_title, expected_status",[
        ("A valid title", status.HTTP_201_CREATED),      # Scénario 1 : Succès
        ("", status.HTTP_400_BAD_REQUEST),               # Scénario 2 : Échec validation DRF
    ]
)
def test_create_task_validation(authenticated_client, input_title, expected_status):
    """Teste la validation stricte lors de la création de tâches."""
    # ARRANGE
    url = reverse('task-list-create')
    task_data = {"title": input_title}

    # ACT
    response = authenticated_client.post(url, data=task_data, format='json')

    # ASSERT : On compare le résultat avec le code statut attendu passé en paramètre
    assert response.status_code == expected_status