import pytest
from django.urls import reverse

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
