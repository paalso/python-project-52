import random

import pytest
from django.urls import reverse

from task_manager.labels.models import Label
from task_manager.tests.builders import build_label, build_task
from task_manager.tests.utils import (
    assert_redirected_with_message,
    get_random_record,
)


@pytest.fixture
def sample_labels():
    Label.objects.create(name='новый')
    Label.objects.create(name='в работе')


# ----- List (Read) view -----------------------------------------------
@pytest.mark.django_db
def test_labels_list_view(client, sample_labels):
    """Tests that the labels list view is accessible and context
    is populated"""
    url = reverse('labels:list')
    response = client.get(url)

    assert response.status_code == 200
    assert 'labels/list.html' in (t.name for t in response.templates)
    assert 'labels' in response.context

    labels = response.context['labels']
    names = [label.name for label in labels]
    assert 'новый' in names
    assert 'в работе' in names


# ----- Delete view ----------------------------------------------------
# TODO: (optional) Add edge-case tests:
# - Attempt to delete a label with a non-existent ID (e.g., pk=99999)
# This will help to further cover possible exceptions and edge cases.

@pytest.mark.django_db
@pytest.mark.parametrize('method', ['get', 'post'], ids=['GET', 'POST'])
def test_label_delete_not_authenticated(
        sample_labels, method, client, django_user_model):
    """Tests that unauthenticated users are redirected when trying to delete"""
    # victim_label = random.choice(Label.objects.all())
    victim_label = get_random_record(Label)
    url = reverse('labels:delete', kwargs={'pk': victim_label.pk})
    response = getattr(client, method)(url, follow=False)

    assert response.status_code == 302
    assert reverse('login') in response.headers['Location']
    assert Label.objects.filter(pk=victim_label.pk).exists()


@pytest.mark.django_db
def test_label_delete_authenticated(authenticated_client, sample_labels):
    """Tests successful deletion of a label by an authenticated user"""
    label = random.choice(Label.objects.all())
    url = reverse('labels:delete', kwargs={'pk': label.pk})
    response = authenticated_client.get(url)

    assert response.status_code == 200
    assert 'labels/delete.html' in [t.name for t in response.templates]
    assert response.context['label'] == label

    response = authenticated_client.post(url, follow=True)

    assert response.status_code == 200
    assert_redirected_with_message(
        response,
        reverse('labels:list'),
        'Метка успешно удалена'
    )
    assert not Label.objects.filter(pk=label.pk).exists()
    assert Label.objects.count() == 1


# WARNING: Does not comply with technical specifications
@pytest.mark.django_db
def test_label_delete_linked_to_tasks(authenticated_client):
    """Tests that label linked to tasks can be deleted"""
    linked_to_tasks_label = build_label()
    build_task(labels=[linked_to_tasks_label])

    url = reverse('labels:delete', kwargs={'pk': linked_to_tasks_label.pk})
    response = authenticated_client.post(url, follow=True)

    assert_redirected_with_message(
        response,
        reverse('labels:list'),
        'Невозможно удалить метку, потому что она используется'
    )
    assert Label.objects.filter(pk=linked_to_tasks_label.pk).exists()


# ----- Update view ----------------------------------------------------
# TODO: (optional) Add edge-case tests:
# - Attempt to update a label with a name exceeding the maximum allowed length
# (specified in the model)
# This will help to further cover possible exceptions and edge cases.

@pytest.mark.django_db
@pytest.mark.parametrize('method', ['get', 'post'], ids=['GET', 'POST'])
def test_label_update_not_authenticated(sample_labels, method, client):
    """Tests that unauthenticated users cannot access update view"""
    target_label = random.choice(Label.objects.all())
    target_label_name = target_label.name
    url = reverse('labels:update', kwargs={'pk': target_label.pk})
    data = {'name': 'старый'}
    response = getattr(client, method)(url, data, follow=False)
    target_label.refresh_from_db()

    assert response.status_code == 302
    assert reverse('login') in response.headers['Location']
    assert target_label.name == target_label_name


@pytest.mark.django_db
def test_label_update_authenticated(authenticated_client, sample_labels):
    """Tests that authenticated users can update an existing label"""
    target_label = random.choice(Label.objects.all())
    url = reverse('labels:update', kwargs={'pk': target_label.pk})
    data = {'name': 'еще новее'}
    response = authenticated_client.get(url, data)

    assert response.status_code == 200
    assert 'labels/update.html' in [t.name for t in response.templates]
    assert response.context['label'] == target_label

    response = authenticated_client.post(url, data, follow=True)
    target_label.refresh_from_db()

    assert response.status_code == 200
    assert_redirected_with_message(
        response,
        reverse('labels:list'),
        'Метка успешно изменена'
    )
    assert target_label.name == data['name']


@pytest.mark.django_db
def test_label_update_duplicate_name(authenticated_client):
    """Tests that duplicate name in update form shows validation error"""
    Label.objects.create(name='оригинал')
    other = Label.objects.create(name='дубликат')
    url = reverse('labels:update', kwargs={'pk': other.pk})
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
def test_label_update_empty_name(authenticated_client):
    """Tests that empty name in update form shows validation error"""
    target_label = Label.objects.create(name='длинное имя')
    target_label_name = target_label.name
    url = reverse('labels:update', kwargs={'pk': target_label.pk})
    data = {'name': ''}
    response = authenticated_client.post(url, data, follow=True)
    form = response.context['form']
    target_label.refresh_from_db()

    assert response.status_code == 200
    assert not form.is_valid()
    assert 'name' in form.errors
    assert any('обязательное' in e.lower() for e in form.errors['name'])
    assert Label.objects.count() == 1
    assert target_label.name == target_label_name


# ----- Create view ----------------------------------------------------
@pytest.mark.django_db
@pytest.mark.parametrize('method', ['get', 'post'], ids=['GET', 'POST'])
def test_label_create_not_authenticated(
        sample_labels, method, client, django_user_model):
    """Tests that unauthenticated users cannot access create view"""
    url = reverse('labels:create')
    data = {'name': 'еще новее'}
    response = getattr(client, method)(url, data, follow=False)

    assert response.status_code == 302
    assert reverse('login') in response.headers['Location']
    assert not Label.objects.filter(name=data["name"]).exists()


@pytest.mark.django_db
def test_label_create_authenticated(authenticated_client, sample_labels):
    """Tests that authenticated users can create a new label"""
    url = reverse('labels:create')
    data = {'name': 'вновь созданный'}
    response = authenticated_client.get(url, data)

    assert response.status_code == 200
    assert 'labels/create.html' in [t.name for t in response.templates]

    response = authenticated_client.post(url, data, follow=True)

    assert response.status_code == 200
    assert_redirected_with_message(
        response,
        reverse('labels:list'),
        'Метка успешно создана'
    )
    assert Label.objects.filter(name=data["name"]).exists()
    assert Label.objects.count() == 3


@pytest.mark.django_db
def test_label_create_duplicate_name(authenticated_client):
    """Tests that duplicate name in create form shows validation error"""
    data = {'name': 'уникальный'}
    Label.objects.create(**data)
    url = reverse('labels:create')
    response = authenticated_client.post(url, data, follow=True)
    form = response.context['form']

    assert response.status_code == 200
    assert 'form' in response.context
    assert not form.is_valid()
    assert 'name' in form.errors
    assert any('уже существует' in e for e in form.errors['name'])
    assert Label.objects.filter(name='уникальный').count() == 1


@pytest.mark.django_db
def test_label_create_empty_name(authenticated_client):
    """Tests that empty name in create form shows validation error"""
    url = reverse('labels:create')
    data = {'name': ''}
    response = authenticated_client.post(url, data, follow=True)
    form = response.context['form']

    assert response.status_code == 200
    assert not form.is_valid()
    assert 'name' in form.errors
    assert any('обязательное' in e.lower() for e in form.errors['name'])
    assert Label.objects.count() == 0
