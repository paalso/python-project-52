import pytest

from task_manager.statuses.models import Status
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
