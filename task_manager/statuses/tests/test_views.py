import pytest
from django.urls import reverse

from task_manager.statuses.models import Status
from task_manager.utils.request import extract_messages


@pytest.fixture
def fill_statuses():
    Status.objects.create(name='новый')
    Status.objects.create(name='в работе')


@pytest.fixture
def authenticated_client(client, django_user_model):
    user = django_user_model.objects.create_user(
        username='testuser', password='testpass')
    client.force_login(user)
    return client


# ----- Read testing ------------------------------------------------
@pytest.mark.django_db
def test_statuses_list_view(client, fill_statuses):
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
@pytest.mark.django_db
@pytest.mark.parametrize('method', ['get', 'post'], ids=['GET', 'POST'])
def test_status_delete_not_authenticated(
        fill_statuses, method, client, django_user_model):
    victim = Status.objects.first()
    url = reverse('users:delete', kwargs={'pk': victim.pk})
    getattr(client, method)(url, follow=True)

    assert Status.objects.filter(pk=victim.pk).exists()


@pytest.mark.django_db
def test_status_delete_authenticated_success(
        authenticated_client, fill_statuses):
    status = Status.objects.first()
    url = reverse('statuses:delete', kwargs={'pk': status.pk})
    response = authenticated_client.get(url)

    assert response.status_code == 200
    assert 'statuses/delete.html' in [t.name for t in response.templates]
    assert response.context['status'] == status

    response = authenticated_client.post(url, follow=True)

    assert response.status_code == 200
    assert response.redirect_chain
    last_redirect_url = response.redirect_chain[-1][0]

    expected_url = reverse('statuses:list')
    assert last_redirect_url == expected_url
    print(f'expected_url: {expected_url}')

    messages = extract_messages(response)
    assert any('Статус успешно удален' in m for m in messages)
    assert not Status.objects.filter(pk=status.pk).exists()
    assert Status.objects.count() == 1
