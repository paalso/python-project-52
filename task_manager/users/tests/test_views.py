import pytest
from django.contrib.messages import get_messages
from django.urls import reverse


def extract_messages(response):
    return [str(m) for m in get_messages(response.wsgi_request)]


@pytest.fixture
def delete_user_setup(client, django_user_model):
    user = django_user_model.objects.get(pk=1)
    client.force_login(user)
    url = reverse('users:delete', kwargs={'pk': user.pk})
    return client, user, url


@pytest.mark.django_db
def test_users_list_view(load_users, client, django_user_model):
    url = reverse('users:list')
    response = client.get(url)

    assert response.status_code == 200
    assert 'users/list.html' in (t.name for t in response.templates)
    assert 'users' in response.context
    assert len(response.context['users']) == django_user_model.objects.count()


@pytest.mark.django_db
def test_delete_user_not_authenticated(load_users, client, django_user_model):
    victim = django_user_model.objects.get(pk=1)
    url = reverse('users:delete', kwargs={'pk': victim.pk})
    response = client.post(url, follow=True)
    messages = extract_messages(response)

    assert any('Вы не авторизованы! Пожалуйста, выполните вход.' ==
               m for m in messages)
    assert response.redirect_chain
    assert '/login' in response.redirect_chain[-1][0]
    assert django_user_model.objects.filter(pk=victim.pk).exists()


@pytest.mark.django_db
def test_delete_user_by_other_authenticated_user(
        load_users, client, django_user_model):
    victim = django_user_model.objects.get(pk=1)
    authenticated_user = django_user_model.objects.get(pk=2)
    client.force_login(authenticated_user)
    url = reverse('users:delete', kwargs={'pk': victim.pk})
    response = client.post(url, follow=True)
    messages = extract_messages(response)

    assert any('У вас нет прав для изменения другого пользователя.' ==
               m for m in messages)
    assert response.redirect_chain
    assert reverse('users:list') in response.redirect_chain[-1][0]
    assert django_user_model.objects.filter(pk=victim.pk).exists()
    assert response.wsgi_request.user.is_authenticated
    assert response.wsgi_request.user == authenticated_user


@pytest.mark.django_db
def test_delete_self_user_without_confirmation(
        load_users, django_user_model, delete_user_setup):
    client, user, url = delete_user_setup
    response = client.post(url, follow=True)
    messages = extract_messages(response)

    assert not any('успешно удал' in m.lower() for m in messages)
    assert django_user_model.objects.filter(pk=user.pk).exists()
    expected_url = reverse('users:list')
    last_redirect_url = response.redirect_chain[-1][0]
    assert last_redirect_url.endswith(expected_url)
    assert response.wsgi_request.user == user
    assert response.wsgi_request.user.is_authenticated


@pytest.mark.django_db
def test_delete_self_user_with_confirmation(
        load_users, django_user_model, delete_user_setup):
    client, user, url = delete_user_setup
    response = client.get(url)

    assert response.status_code == 200
    assert 'users/delete.html' in (t.name for t in response.templates)
    assert 'Да, удалить' in response.text

    response = client.post(url, {'confirm': 'true'}, follow=True)
    messages = extract_messages(response)

    assert any('Пользователь успешно удален' == m for m in messages)
    assert not django_user_model.objects.filter(pk=user.pk).exists()
    expected_url = reverse('users:list')
    last_redirect_url = response.redirect_chain[-1][0]
    assert last_redirect_url.endswith(expected_url)
    assert not response.wsgi_request.user.is_authenticated
