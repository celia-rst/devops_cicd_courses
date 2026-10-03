import pytest
from django.core.exceptions import ValidationError
from .models import Task

# La marque 'pytest.mark.django_db' indique que TOUS les tests de ce fichier
# ont l'autorisation d'accéder à la base de données.
pytestmark = pytest.mark.django_db

def test_task_str_representation(sample_task):
    """Teste que la méthode __str__ du modèle retourne bien le titre."""
    # ARRANGE: La fixture 'sample_task' a déjà inséré notre objet en base pour nous !

    # ACT & ASSERT: On vérifie directement le résultat avec un simple 'assert'.
    assert str(sample_task) == "Sample Task"

def test_task_requires_title(user):
    """Teste la validation du modèle pour un titre vide."""
    # ARRANGE: Crée une instance de tâche sans la sauvegarder en base
    task = Task(owner=user, title="")

    # ACT & ASSERT: Vérifie que full_clean() lève une ValidationError.
    # `pytest.raises` est l'équivalent Pytest de `self.assertRaises`.
    with pytest.raises(ValidationError):
        task.full_clean()

def test_mark_as_complete_method(sample_task):
    """Teste que la méthode mark_as_complete fonctionne."""
    # ARRANGE : La fixture 'sample_task' nous donne par défaut une tâche avec completed=False
    assert sample_task.completed is False

    # ACT : On exécute la méthode métier
    sample_task.mark_as_complete()

    # ASSERT :
    # On recharge l'objet depuis la base de données pour être certain
    # que la méthode interne .save() a bien été appelée par notre méthode.
    sample_task.refresh_from_db()
    assert sample_task.completed is True

def test_completed_tasks_manager(user):
    """Teste que le manager personnalisé 'completed' filtre correctement."""
    # ARRANGE
    Task.objects.create(title="Completed Task", owner=user, completed=True)
    Task.objects.create(title="Incomplete Task", owner=user, completed=False)
    Task.objects.create(title="Another Completed Task", owner=user, completed=True)

    # ACT
    completed_tasks = Task.objects.completed()

    # ASSERT
    assert completed_tasks.count() == 2
    # On peut aussi vérifier mathématiquement que les tâches incomplètes n'y sont pas
    assert not completed_tasks.filter(completed=False).exists()