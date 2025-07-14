# task_manager/tests/builders.py

from task_manager.users.models import CustomUser
from task_manager.labels.models import Label
from task_manager.statuses.models import Status
from task_manager.tasks.models import Task


def build_label(name='some progress'):
    return Label.objects.create(name=name)


def build_status(name='some status'):
    return Status.objects.create(name=name)


def build_user(
        username='tom',
        first_name='Tom',
        last_name='Dickson',
        password='pass123'
    ):
    user = CustomUser.objects.create_user(
        username=username,
        password=password,
    )
    user.first_name = first_name
    user.last_name = last_name
    user.save()
    return user


def create_task(
    name='Some Task',
    description='Some description...',
    status=None,
    author=None,
    executor=None,
    labels=None,
):
    status = status or build_status()
    author = author or build_user(username='author_user')
    executor = executor or build_user(username='executor_user')

    task = Task.objects.create(
        name=name,
        description=description,
        status=status,
        author=author,
        executor=executor,
    )

    if labels:
        task.labels.set(labels)

    return task
