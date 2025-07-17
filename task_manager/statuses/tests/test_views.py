import pytest
from django.urls import reverse

from task_manager.statuses.models import Status
from task_manager.tests.builders import build_status, build_task
from task_manager.tests.utils import (
    assert_redirected_with_message,
    get_random_record,
)


@pytest.fixture
def sample_statuses():
    Status.objects.create(name='new')
    Status.objects.create(name='in progress')


# ----- List (Read) view -----------------------------------------------
@pytest.mark.django_db
def test_statuses_list_requires_auth(client):
    response = client.get(reverse('statuses:list'), follow=False)
    assert response.status_code == 302
    assert reverse('login') in response.url

    response = client.get(reverse('statuses:list'), follow=True)
    assert_redirected_with_message(
        response,
        reverse('login'),
        'Вы не авторизованы! Пожалуйста, выполните вход.'
    )


@pytest.mark.django_db
def test_statuses_list_view(authenticated_client, sample_statuses):
    """Tests that the statuses list view is accessible and context
    is populated"""
    url = reverse('statuses:list')
    response = authenticated_client.get(url)

    assert response.status_code == 200
    assert 'statuses/list.html' in (t.name for t in response.templates)
    assert 'statuses' in response.context

    statuses = response.context['statuses']
    names = [status.name for status in statuses]
    assert 'new' in names
    assert 'in progress' in names


# ----- Delete view ---------------------------------------------------
# TODO: (optional) Add edge-case tests:
# - Attempt to delete a status with a non-existent ID (e.g., pk=99999)
# This will help to further cover possible exceptions and edge cases.

@pytest.mark.django_db
@pytest.mark.parametrize('method', ['get', 'post'], ids=['GET', 'POST'])
def test_status_delete_not_authenticated(
        sample_statuses, method, client, django_user_model):
    """Tests that unauthenticated users are redirected when trying to delete"""
    victim_status = get_random_record(Status)
    url = reverse('statuses:delete', kwargs={'pk': victim_status.pk})
    response = getattr(client, method)(url, follow=False)

    assert response.status_code == 302
    assert reverse('login') in response.headers['Location']
    assert Status.objects.filter(pk=victim_status.pk).exists()


@pytest.mark.django_db
def test_status_delete_authenticated(authenticated_client, sample_statuses):
    """Tests successful deletion of a status by an authenticated user"""
    status = get_random_record(Status)
    url = reverse('statuses:delete', kwargs={'pk': status.pk})
    response = authenticated_client.get(url)

    assert response.status_code == 200
    assert 'statuses/delete.html' in [t.name for t in response.templates]
    assert response.context['status'] == status

    response = authenticated_client.post(url, follow=True)

    assert not Status.objects.filter(pk=status.pk).exists()
    assert Status.objects.count() == 1
    assert_redirected_with_message(
        response,
        reverse('statuses:list'),
        'Статус успешно удален'
    )


@pytest.mark.django_db
def test_status_delete_linked_to_tasks(authenticated_client):
    """Tests that status linked to tasks cannot be deleted"""
    linked_to_tasks_status = build_status()
    build_task(status=linked_to_tasks_status)
    url = reverse('statuses:delete', kwargs={'pk': linked_to_tasks_status.pk})
    response = authenticated_client.post(url, follow=True)

    assert_redirected_with_message(
        response,
        reverse('statuses:list'),
        'Невозможно удалить статус, потому что он используется'
    )
    assert Status.objects.filter(pk=linked_to_tasks_status.pk).exists()

# ----- Update view ----------------------------------------------------
# TODO: (optional) Add edge-case tests:
# - Attempt to update a status with a name exceeding the maximum allowed length
# (specified in the model)
# This will help to further cover possible exceptions and edge cases.


@pytest.mark.django_db
@pytest.mark.parametrize('method', ['get', 'post'], ids=['GET', 'POST'])
def test_status_update_not_authenticated(sample_statuses, method, client):
    """Tests that unauthenticated users cannot access update view"""
    target_status = get_random_record(Status)
    target_status_name = target_status.name
    url = reverse('statuses:update', kwargs={'pk': target_status.pk})
    data = {'name': 'старый'}
    response = getattr(client, method)(url, data, follow=False)
    target_status.refresh_from_db()

    assert response.status_code == 302
    assert reverse('login') in response.headers['Location']
    assert target_status.name == target_status_name


@pytest.mark.django_db
def test_status_update_authenticated(authenticated_client, sample_statuses):
    """Tests that authenticated users can update an existing status"""
    target_status = get_random_record(Status)
    url = reverse('statuses:update', kwargs={'pk': target_status.pk})
    data = {'name': 'еще новее'}
    response = authenticated_client.get(url, data)

    assert response.status_code == 200
    assert 'statuses/update.html' in [t.name for t in response.templates]
    assert response.context['status'] == target_status

    response = authenticated_client.post(url, data, follow=True)
    target_status.refresh_from_db()

    assert_redirected_with_message(
        response,
        reverse('statuses:list'),
        'Статус успешно изменен'
    )
    assert target_status.name == data['name']


@pytest.mark.django_db
def test_status_update_duplicate_name(authenticated_client):
    """Tests that duplicate name in update form shows validation error"""
    Status.objects.create(name='оригинал')
    other = Status.objects.create(name='дубликат')
    url = reverse('statuses:update', kwargs={'pk': other.pk})
    data = {'name': 'оригинал'}
    response = authenticated_client.post(url, data, follow=True)
    form = response.context['form']
    other.refresh_from_db()

    assert response.status_code == 200
    assert not form.is_valid()
    assert 'name' in form.errors
    assert any('уже существует' in e for e in form.errors['name'])
    assert other.name == 'дубликат'


@pytest.mark.django_db
def test_status_update_empty_name(authenticated_client):
    """Tests that empty name in update form shows validation error"""
    target_status = Status.objects.create(name='длинное имя')
    target_status_name = target_status.name
    url = reverse('statuses:update', kwargs={'pk': target_status.pk})
    data = {'name': ''}
    response = authenticated_client.post(url, data, follow=True)
    form = response.context['form']
    target_status.refresh_from_db()

    assert response.status_code == 200
    assert not form.is_valid()
    assert 'name' in form.errors
    assert any('обязательное' in e.lower() for e in form.errors['name'])
    assert Status.objects.count() == 1
    assert target_status.name == target_status_name


# ----- Delete view -----------------------------------------------------
@pytest.mark.django_db
@pytest.mark.parametrize('method', ['get', 'post'], ids=['GET', 'POST'])
def test_status_create_not_authenticated(
        sample_statuses, method, client, django_user_model):
    """Tests that unauthenticated users cannot access create view"""
    url = reverse('statuses:create')
    data = {'name': 'latest'}
    response = getattr(client, method)(url, data, follow=False)

    assert response.status_code == 302
    assert reverse('login') in response.headers['Location']
    assert not Status.objects.filter(name=data["name"]).exists()


@pytest.mark.django_db
def test_status_create_authenticated(authenticated_client, sample_statuses):
    """Tests that authenticated users can create a new status"""
    url = reverse('statuses:create')
    data = {'name': 'latest'}
    response = authenticated_client.get(url, data)

    assert response.status_code == 200
    assert 'statuses/create.html' in [t.name for t in response.templates]

    response = authenticated_client.post(url, data, follow=True)

    assert_redirected_with_message(
        response,
        reverse('statuses:list'),
        'Статус успешно создан'
    )
    assert Status.objects.filter(name=data["name"]).exists()
    assert Status.objects.count() == 3


@pytest.mark.django_db
def test_status_create_duplicate_name(authenticated_client):
    """Tests that duplicate name in create form shows validation error"""
    data = {'name': 'уникальный'}
    Status.objects.create(**data)
    url = reverse('statuses:create')
    response = authenticated_client.post(url, data, follow=True)
    form = response.context['form']

    assert response.status_code == 200
    assert 'form' in response.context
    assert not form.is_valid()
    assert 'name' in form.errors
    assert any('уже существует' in e for e in form.errors['name'])
    assert Status.objects.filter(name='уникальный').count() == 1


@pytest.mark.django_db
def test_status_create_empty_name(authenticated_client):
    """Tests that empty name in create form shows validation error"""
    url = reverse('statuses:create')
    data = {'name': ''}
    response = authenticated_client.post(url, data, follow=True)
    form = response.context['form']

    assert response.status_code == 200
    assert not form.is_valid()
    assert 'name' in form.errors
    assert any('обязательное' in e.lower() for e in form.errors['name'])
    assert Status.objects.count() == 0
