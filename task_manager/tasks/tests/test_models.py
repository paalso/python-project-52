import pytest
from django.db.models import ProtectedError
from django.db.utils import IntegrityError

from task_manager.labels.models import Label
from task_manager.statuses.models import Status
from task_manager.tasks.models import Task
from task_manager.users.models import CustomUser


@pytest.fixture
def task_data():
    status = Status.objects.create(name='some status')
    author = CustomUser.objects.create_user(
        username='author_user', password='pass123')
    executor = CustomUser.objects.create_user(
        username='executor_user', password='pass123')
    return {
        'name': 'Some Task',
        'description': 'Some description...',
        'status': status,
        'author': author,
        'executor': executor
    }


@pytest.mark.django_db
def test_task_creation_with_empty_labels(task_data):
    task = Task.objects.create(**task_data)

    assert task.name == 'Some Task'
    assert task.description == 'Some description...'
    assert task.status.name == 'some status'
    assert task.author.username == 'author_user'
    assert task.executor.username == 'executor_user'
    assert not task.labels.exists()
    assert str(task) == 'Some Task'


@pytest.mark.django_db
def test_task_creation_with_non_empty_labels(task_data):
    label1 = Label.objects.create(name='label1')
    label2 = Label.objects.create(name='label2')
    task = Task.objects.create(**task_data)
    task.labels.set([label1, label2])

    assert set(task.labels.all()) == {label1, label2}


@pytest.mark.django_db
def test_task_deletion_protects_status(task_data):
    task_data.pop('status')

    with (pytest.raises(IntegrityError)):
        Task.objects.create(**task_data)


@pytest.mark.parametrize('user_field', ['author', 'executor'])
@pytest.mark.django_db
def test_cannot_create_task_without_user(task_data, user_field):
    task_data.pop(user_field)

    with pytest.raises(IntegrityError):
        Task.objects.create(**task_data)


@pytest.mark.django_db
def test_unique_name_constraint(task_data):
    Task.objects.create(**task_data)

    with pytest.raises(IntegrityError):
        Task.objects.create(**task_data)


@pytest.mark.django_db
def test_cannot_delete_status_if_task_exists(task_data):
    task = Task.objects.create(**task_data)
    with pytest.raises(ProtectedError):
        task.status.delete()


@pytest.mark.parametrize('user_field', ['author', 'executor'])
@pytest.mark.django_db
def test_cannot_delete_user_if_task_exists(task_data, user_field):
    task = Task.objects.create(**task_data)
    user = getattr(task, user_field)
    with pytest.raises(ProtectedError):
        user.delete()
