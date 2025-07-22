import pytest
from django.urls import reverse

from task_manager.tasks.models import Task
from task_manager.tests.builders import (
    build_label,
    build_status,
    build_task,
    build_user,
)
from task_manager.tests.utils import assert_redirected_with_message


@pytest.fixture
def sample_tasks():
    author = build_user(username='author_user')
    executor1 = build_user(username='executor1')
    executor2 = build_user(username='executor2')

    status_open = build_status(name='Open')
    status_closed = build_status(name='Closed')

    label_bug = build_label(name='bug')
    label_feature = build_label(name='feature')

    t1 = build_task(
        name='Bug by author/executor1',
        status=status_open,
        author=author,
        executor=executor1,
        labels=[label_bug],
    )

    t2 = build_task(
        name='Feature by author/executor2',
        status=status_closed,
        author=author,
        executor=executor2,
        labels=[label_feature],
    )

    t3 = build_task(
        name='Bug by executor1',
        status=status_open,
        author=executor1,
        executor=executor1,
        labels=[label_bug],
    )

    t4 = build_task(
        name='Feature by executor2',
        status=status_closed,
        author=executor2,
        executor=executor2,
        labels=[label_feature, label_bug],
    )

    return {
        'author': author,
        'executors': [executor1, executor2],
        'statuses': [status_open, status_closed],
        'labels': [label_bug, label_feature],
        'tasks': [t1, t2, t3, t4],
    }


# ----- List (Read) view -----------------------------------------------
@pytest.mark.django_db
def test_tasks_list_requires_auth(client):
    response = client.get(reverse('tasks:list'), follow=False)
    assert response.status_code == 302
    assert reverse('login') in response.url

    response = client.get(reverse('tasks:list'), follow=True)
    assert_redirected_with_message(
        response,
        reverse('login'),
        'Вы не авторизованы! Пожалуйста, выполните вход.'
    )


@pytest.mark.django_db
def test_tasks_list_view(authenticated_client):
    url = reverse('tasks:list')
    response = authenticated_client.get(url)
    content = response.content.decode()

    assert response.status_code == 200
    assert 'tasks' in response.context
    assert 'tasks/list.html' in [t.name for t in response.templates]

    assert 'name="status"' in content
    assert 'id="id_status"' in content

    assert 'name="executor"' in content
    assert 'id="id_executor"' in content

    assert 'name="label"' in content
    assert 'id="id_label"' in content

    assert 'name="self_tasks"' in content
    assert 'id="id_self_tasks"' in content


@pytest.mark.django_db
def test_filter_by_status(authenticated_client, sample_tasks):
    status = sample_tasks['statuses'][0]  # status_open
    url = reverse('tasks:list') + f'?status={status.pk}&executor=&label='
    response = authenticated_client.get(url)
    filtered_tasks = response.context['tasks']
    expected_tasks = [t for t in sample_tasks['tasks'] if t.status == status]

    assert set(filtered_tasks) == set(expected_tasks)
    assert len(filtered_tasks) == 2


@pytest.mark.django_db
def test_filter_by_executor(authenticated_client, sample_tasks):
    user = sample_tasks['executors'][0]  # executor1
    url = reverse('tasks:list') + f'?status=&executor={user.pk}&label=1'
    response = authenticated_client.get(url)
    filtered_tasks = response.context['tasks']
    expected_tasks = [t for t in sample_tasks['tasks'] if t.executor == user]

    assert set(filtered_tasks) == set(expected_tasks)
    assert len(filtered_tasks) == 2


@pytest.mark.django_db
def test_filter_by_label(authenticated_client, sample_tasks):
    label = sample_tasks['labels'][0]  # label_bug

    url = reverse('tasks:list') + f'?status=&executor=&label={label.pk}'
    response = authenticated_client.get(url)

    filtered_tasks = response.context['tasks']
    expected_tasks = [
        t for t in sample_tasks['tasks']
        if label in t.labels.all()
    ]

    assert set(filtered_tasks) == set(expected_tasks)
    assert len(filtered_tasks) == 3


@pytest.mark.django_db
def test_filter_self_tasks(client, sample_tasks):
    user = sample_tasks['author']
    client.force_login(user)
    url = reverse('tasks:list') + '?self_tasks=on'
    response = client.get(url)
    filtered_tasks = response.context['tasks']
    expected_tasks = [t for t in sample_tasks['tasks'] if t.author == user]
    assert set(filtered_tasks) == set(expected_tasks)
    assert len(filtered_tasks) == 2


@pytest.mark.django_db
def test_filter_by_multiple_fields(authenticated_client, sample_tasks):
    status = sample_tasks['statuses'][0]       # status_open
    executor = sample_tasks['executors'][0]    # executor1
    label = sample_tasks['labels'][0]          # label_bug

    query = f'?status={status.pk}&executor={executor.pk}&label={label.pk}'
    url = reverse('tasks:list') + query

    response = authenticated_client.get(url)
    filtered_tasks = response.context['tasks']

    expected_tasks = [
        t for t in sample_tasks['tasks']
        if t.status == status
        and t.executor == executor
        and label in t.labels.all()
    ]

    assert set(filtered_tasks) == set(expected_tasks)
    assert len(filtered_tasks) == 2


# ----- Create view -----------------------------------------------
@pytest.mark.django_db
@pytest.mark.parametrize('method', ['get', 'post'], ids=['GET', 'POST'])
def test_task_create_not_authenticated(method, client, task_data):
    """Unauthenticated users cannot create a task and should be redirected"""
    url = reverse('tasks:create')
    response = getattr(client, method)(url, task_data, follow=False)

    assert response.status_code == 302
    assert reverse('login') in response.headers['Location']
    assert not Task.objects.filter(name=task_data["name"]).exists()


@pytest.mark.django_db
def test_task_create_authenticated(authenticated_client):
    """Authenticated user can create a task"""
    url = reverse('tasks:create')

    get_response = authenticated_client.get(url)
    assert get_response.status_code == 200
    assert 'tasks/create.html' in [t.name for t in get_response.templates]

    status = build_status()
    executor = build_user()
    label1 = build_label('label1')
    label2 = build_label('label2')
    post_data = {
        'name': 'Task name',
        'description': 'Some description...',
        'status': status.id,
        'labels': [label1.id, label2.id],
        'executor': executor.id,
    }

    post_response = authenticated_client.post(url, post_data, follow=True)

    assert_redirected_with_message(
        post_response,
        reverse('tasks:list'),
        'Задача успешно создана'
    )
    assert post_response.status_code == 200
    assert Task.objects.count() == 1

    task = Task.objects.first()
    assert task.name == 'Task name'
    assert set(task.labels.all()) == {label1, label2}
    assert task.author == authenticated_client.user


def test_task_create_duplicate_name(authenticated_client, task_data):
    """Cannot create a task if the name already exists"""
    Task.objects.create(**task_data)
    response = authenticated_client.post(reverse('tasks:create'), task_data)

    assert response.status_code == 200
    assert 'form' in response.context

    form = response.context['form']
    assert not form.is_valid()
    assert 'name' in form.errors
    assert any('уже существует' in e for e in form.errors['name'])
    assert Task.objects.count() == 1


@pytest.mark.django_db
@pytest.mark.parametrize('missing_field', ['name', 'status', 'executor'])
def test_task_create_missing_fields(
        authenticated_client, task_data, missing_field):
    """Create should fail if required fields are missing"""
    task_data.pop(missing_field)
    response = authenticated_client.post(reverse('tasks:create'), task_data)

    assert response.status_code == 200
    assert 'form' in response.context

    form = response.context['form']
    assert not form.is_valid()
    assert missing_field in form.errors
    assert not Task.objects.exists()


# ----- Update view -----------------------------------------------
@pytest.mark.django_db
@pytest.mark.parametrize('method', ['get', 'post'], ids=['GET', 'POST'])
def test_task_update_not_authenticated(method, client, task_data):
    """Unauthenticated users should be redirected from update view"""
    task = Task.objects.create(**task_data)
    url = reverse('tasks:update', args=[task.id])
    response = getattr(client, method)(url, task_data, follow=False)

    assert response.status_code == 302
    assert reverse('login') in response.headers['Location']


@pytest.mark.django_db
def test_task_update_authenticated(authenticated_client):
    """Authenticated user can update a task"""
    author = authenticated_client.user
    old_executor = build_user()
    task = Task.objects.create(
        name='Old task',
        description='Old description',
        status=build_status(),
        executor=old_executor,
        author=author
    )
    label1 = build_label('Old Label')
    task.labels.set([label1])

    new_status = build_status('In progress')
    new_executor = build_user('new-exec')
    label2 = build_label('New Label')

    update_data = {
        'name': 'Updated Task',
        'description': 'Updated description',
        'status': new_status.id,
        'executor': new_executor.id,
        'labels': [label2.id],
    }

    url = reverse('tasks:update', args=[task.id])
    response = authenticated_client.post(url, update_data, follow=True)

    assert_redirected_with_message(
        response,
        reverse('tasks:list'),
        'Задача успешно изменена'
    )

    task.refresh_from_db()
    assert task.name == 'Updated Task'
    assert task.description == 'Updated description'
    assert task.status == new_status
    assert task.executor == new_executor
    assert set(task.labels.all()) == {label2}


@pytest.mark.django_db
def test_task_update_duplicate_name(authenticated_client, task_data):
    """Cannot update task to a name that already exists"""
    Task.objects.create(**task_data | {'name': 'Existing Task'})
    task = Task.objects.create(**task_data | {'name': 'Initial Task'})

    url = reverse('tasks:update', args=[task.id])
    update_data = task_data.copy()
    update_data['name'] = 'Existing Task'

    response = authenticated_client.post(url, update_data)

    assert response.status_code == 200
    form = response.context['form']
    assert not form.is_valid()
    assert 'name' in form.errors
    assert any('уже существует' in e for e in form.errors['name'])


@pytest.mark.django_db
@pytest.mark.parametrize('missing_field', ['name', 'status', 'executor'])
def test_task_update_missing_fields(
        authenticated_client, task_data, missing_field):
    """Update should fail if required fields are missing"""
    task = Task.objects.create(**task_data)

    update_data = task_data.copy()
    update_data.pop(missing_field)

    url = reverse('tasks:update', args=[task.id])
    response = authenticated_client.post(url, update_data)

    assert response.status_code == 200
    form = response.context['form']
    assert not form.is_valid()
    assert missing_field in form.errors


# ----- Delete view -----------------------------------------------
@pytest.mark.django_db
@pytest.mark.parametrize('method', ['get', 'post'], ids=['GET', 'POST'])
def test_task_delete_not_authenticated(method, client, task_data):
    """Unauthenticated users cannot delete a task and should be redirected"""
    task = Task.objects.create(**task_data)
    url = reverse('tasks:delete', args=[task.id])
    response = getattr(client, method)(url, follow=False)

    assert response.status_code == 302
    assert reverse('login') in response.headers['Location']
    assert Task.objects.filter(id=task.id).exists()


@pytest.mark.django_db
def test_task_delete_not_author(authenticated_client, task_data):
    """Users who are not the author should not be able to delete the task"""
    other_user = build_user('other-user')
    task = Task.objects.create(**task_data | {'author': other_user})
    url = reverse('tasks:delete', args=[task.id])

    response = authenticated_client.post(url, follow=True)

    assert_redirected_with_message(
        response,
        reverse('tasks:list'),
        'Задачу может удалить только ее автор'
    )
    assert Task.objects.filter(id=task.id).exists()


@pytest.mark.django_db
def test_task_delete_authenticated_author(authenticated_client, task_data):
    """Author can delete their task"""
    task_data = task_data | {'author': authenticated_client.user}
    task = build_task(**task_data)

    url = reverse('tasks:delete', args=[task.id])
    get_response = authenticated_client.get(url)
    assert get_response.status_code == 200
    assert 'tasks/delete.html' in [t.name for t in get_response.templates]

    post_response = authenticated_client.post(url, follow=True)

    assert_redirected_with_message(
        post_response,
        reverse('tasks:list'),
        'Задача успешно удалена'
    )
    assert not Task.objects.filter(id=task.id).exists()
