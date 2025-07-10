import random

import pytest
from django.urls import reverse

from task_manager.statuses.models import Status
from task_manager.tests.utils import extract_messages, get_random_record


@pytest.fixture
def sample_statuses():
    Status.objects.create(name='новый')
    Status.objects.create(name='в работе')


@pytest.fixture
def authenticated_client(client, django_user_model):
    user = django_user_model.objects.create_user(
        username='testuser', password='testpass')
    client.force_login(user)
    return client


# # ----- List (Read) view -----------------------------------------------
# Tests that the statuses list view is accessible and context is populated
@pytest.mark.django_db
def test_statuses_list_view(client, sample_statuses):
    url = reverse('statuses:list')
    response = client.get(url)

    assert response.status_code == 200
    assert 'statuses/list.html' in (t.name for t in response.templates)
    assert 'statuses' in response.context

    statuses = response.context['statuses']
    names = [status.name for status in statuses]
    assert 'новый' in names
    assert 'в работе' in names


# ----- Delete testing ----------------------------------------------
# Tests that unauthenticated users are redirected when trying to delete
@pytest.mark.django_db
@pytest.mark.parametrize('method', ['get', 'post'], ids=['GET', 'POST'])
def test_status_delete_not_authenticated(
        sample_statuses, method, client, django_user_model):
    # victim_status = random.choice(Status.objects.all())
    victim_status = get_random_record(Status)
    url = reverse('statuses:delete', kwargs={'pk': victim_status.pk})
    response = getattr(client, method)(url, follow=False)

    assert response.status_code == 302
    assert reverse('login') in response.headers['Location']
    assert Status.objects.filter(pk=victim_status.pk).exists()


# Tests successful deletion of a status by an authenticated user
@pytest.mark.django_db
def test_status_delete_authenticated(authenticated_client, sample_statuses):
    status = random.choice(Status.objects.all())
    url = reverse('statuses:delete', kwargs={'pk': status.pk})
    response = authenticated_client.get(url)

    assert response.status_code == 200
    assert 'statuses/delete.html' in [t.name for t in response.templates]
    assert response.context['status'] == status

    response = authenticated_client.post(url, follow=True)
    last_redirect_url = response.redirect_chain[-1][0]
    expected_url = reverse('statuses:list')
    messages = extract_messages(response)

    assert response.status_code == 200
    assert response.redirect_chain
    assert last_redirect_url == expected_url
    assert any('Статус успешно удален' in m for m in messages)
    assert not Status.objects.filter(pk=status.pk).exists()
    assert Status.objects.count() == 1


# ----- Update view ------------------------------------------------------
# Tests that unauthenticated users cannot access update view
@pytest.mark.django_db
@pytest.mark.parametrize('method', ['get', 'post'], ids=['GET', 'POST'])
def test_status_update_not_authenticated(sample_statuses, method, client):
    target_status = random.choice(Status.objects.all())
    target_status_name = target_status.name
    url = reverse('statuses:update', kwargs={'pk': target_status.pk})
    data = {'name': 'старый'}
    response = getattr(client, method)(url, data, follow=False)
    target_status.refresh_from_db()

    assert response.status_code == 302
    assert reverse('login') in response.headers['Location']
    assert target_status.name == target_status_name


# Tests that authenticated users can update an existing status
@pytest.mark.django_db
def test_status_update_authenticated(authenticated_client, sample_statuses):
    target_status = random.choice(Status.objects.all())
    url = reverse('statuses:update', kwargs={'pk': target_status.pk})
    data = {'name': 'еще новее'}
    response = authenticated_client.get(url, data)

    assert response.status_code == 200
    assert 'statuses/update.html' in [t.name for t in response.templates]
    assert response.context['status'] == target_status

    response = authenticated_client.post(url, data, follow=True)
    last_redirect_url = response.redirect_chain[-1][0]
    expected_url = reverse('statuses:list')
    messages = extract_messages(response)
    target_status.refresh_from_db()

    assert response.status_code == 200
    assert response.redirect_chain
    assert last_redirect_url == expected_url
    assert any('Статус успешно изменен' in m for m in messages)
    assert target_status.name == data['name']


# Tests that duplicate name in update form shows validation error
@pytest.mark.django_db
def test_status_update_duplicate_name(authenticated_client):
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


# Tests that empty name in update form shows validation error
@pytest.mark.django_db
def test_status_update_empty_name(authenticated_client):
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
# Tests that unauthenticated users cannot access create view
@pytest.mark.django_db
@pytest.mark.parametrize('method', ['get', 'post'], ids=['GET', 'POST'])
def test_status_create_not_authenticated(
        sample_statuses, method, client, django_user_model):
    url = reverse('statuses:create')
    data = {'name': 'еще новее'}
    response = getattr(client, method)(url, data, follow=False)

    assert response.status_code == 302
    assert reverse('login') in response.headers['Location']
    assert not Status.objects.filter(name=data["name"]).exists()


# Tests that authenticated users can create a new status
@pytest.mark.django_db
def test_status_create_authenticated(authenticated_client, sample_statuses):
    url = reverse('statuses:create')
    data = {'name': 'вновь созданный'}
    response = authenticated_client.get(url, data)

    assert response.status_code == 200
    assert 'statuses/create.html' in [t.name for t in response.templates]

    response = authenticated_client.post(url, data, follow=True)
    last_redirect_url = response.redirect_chain[-1][0]
    expected_url = reverse('statuses:list')
    messages = extract_messages(response)

    assert response.status_code == 200
    assert response.redirect_chain
    assert last_redirect_url == expected_url
    assert any('Статус успешно создан' in m for m in messages)
    assert Status.objects.filter(name=data["name"]).exists()
    assert Status.objects.count() == 3


# Tests that duplicate name in create form shows validation error
@pytest.mark.django_db
def test_status_create_duplicate_name(authenticated_client):
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


# Tests that empty name in create form shows validation error
@pytest.mark.django_db
def test_status_create_empty_name(authenticated_client):
    url = reverse('statuses:create')
    data = {'name': ''}
    response = authenticated_client.post(url, data, follow=True)
    form = response.context['form']

    assert response.status_code == 200
    assert not form.is_valid()
    assert 'name' in form.errors
    assert any('обязательное' in e.lower() for e in form.errors['name'])
    assert Status.objects.count() == 0
