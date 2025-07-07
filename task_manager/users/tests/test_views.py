import pytest
from django.contrib.messages import get_messages
from django.urls import reverse


def extract_messages(response):
    return [str(m) for m in get_messages(response.wsgi_request)]


def assert_redirected_with_message(response, expected_url, message):
    assert response.status_code == 200
    assert response.redirect_chain
    last_redirect_url = response.redirect_chain[-1][0]
    assert last_redirect_url.endswith(expected_url)
    messages = extract_messages(response)
    assert any(message in m for m in messages)


@pytest.fixture
def delete_user_setup(client, django_user_model):
    user = django_user_model.objects.get(pk=2)
    client.force_login(user)
    url = reverse('users:delete', kwargs={'pk': user.pk})
    return client, user, url


@pytest.fixture
def update_user_setup(client, django_user_model):
    target_user = django_user_model.objects.create_user(
        username='Socrates', password='pass123')
    url = reverse('users:update', kwargs={'pk': target_user.pk})
    return client, target_user, url


@pytest.fixture
def user_data():
    return {
        'username': 'Platonicus',
        'first_name': 'Plato',
        'last_name': 'P.',
        'password1': 'pass123',
        'password2': 'pass123',
    }


# ----- Read testing ------------------------------------------------
@pytest.mark.django_db
def test_users_list_view(load_users, client, django_user_model):
    url = reverse('users:list')
    response = client.get(url)

    assert response.status_code == 200
    assert 'users/list.html' in (t.name for t in response.templates)
    assert 'users' in response.context
    assert len(response.context['users']) == django_user_model.objects.count()


# ----- Delete testing ----------------------------------------------
@pytest.mark.django_db
@pytest.mark.parametrize('method', ['get', 'post'], ids=['GET', 'POST'])
def test_delete_user_not_authenticated(method, client, django_user_model):
    victim = django_user_model.objects.create_user('victim', password='pwd')

    url = reverse('users:delete', kwargs={'pk': victim.pk})
    response = getattr(client, method)(url, follow=True)

    assert_redirected_with_message(
        response,
        reverse('login'),
        'Вы не авторизованы! Пожалуйста, выполните вход.'
    )
    assert django_user_model.objects.filter(pk=victim.pk).exists()


@pytest.mark.django_db
@pytest.mark.parametrize('method', ['get', 'post'], ids=['GET', 'POST'])
def test_delete_user_by_other_authenticated_user(
        method, client, django_user_model):

    victim = django_user_model.objects.create_user('victim', password='pwd')
    requesting_user = django_user_model.objects.create_user(
        'foreigner', password='pwd')
    client.force_login(requesting_user)

    url = reverse('users:delete', kwargs={'pk': victim.pk})
    response = getattr(client, method)(url, follow=True)

    assert_redirected_with_message(
        response,
        reverse('users:list'),
        'У вас нет прав для изменения другого пользователя.'
    )
    assert django_user_model.objects.filter(pk=victim.pk).exists()
    assert response.wsgi_request.user == requesting_user
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

    assert_redirected_with_message(
        response,
        reverse('users:list'),
        'Пользователь успешно удален'
    )
    assert not django_user_model.objects.filter(pk=user.pk).exists()
    assert not response.wsgi_request.user.is_authenticated


# ----- Update testing ----------------------------------------------
@pytest.mark.parametrize('method', ['get', 'post'], ids=['GET', 'POST'])
@pytest.mark.django_db
def test_update_user_not_authenticated(
        client, django_user_model, method, user_data):
    target_user = django_user_model.objects.create_user(
        username='Socrates', password='pass123')
    url = reverse('users:update', kwargs={'pk': target_user.pk})
    response = getattr(client, method)(url, user_data, follow=True)

    assert_redirected_with_message(
        response, reverse('login'),
        'Вы не авторизованы! Пожалуйста, выполните вход.')


@pytest.mark.parametrize('method', ['get', 'post'], ids=['GET', 'POST'])
@pytest.mark.django_db
def test_update_user_by_other_authenticated_user(
        client, django_user_model, method, user_data):
    target_user = django_user_model.objects.create_user(
        username='Socrates', password='pass123')
    url = reverse('users:update', kwargs={'pk': target_user.pk})
    requesting_user = django_user_model.objects.create_user(
        'foreigner', password='pwd')
    client.force_login(requesting_user)
    response = getattr(client, method)(url, user_data, follow=True)

    assert_redirected_with_message(
        response, reverse('users:list'),
        'У вас нет прав для изменения другого пользователя.')


@pytest.mark.django_db
def test_update_self_user(update_user_setup, user_data):
    client, target_user, url = update_user_setup
    client.force_login(target_user)
    response = client.post(url, user_data, follow=True)

    assert_redirected_with_message(
        response,
        reverse('users:list'),
        'Пользователь успешно изменен'
    )
    assert not response.wsgi_request.user.is_authenticated
    target_user.refresh_from_db()
    assert target_user.username == 'Platonicus'


@pytest.mark.django_db
def test_update_self_user_to_existing_username(
    client, django_user_model, load_users
):
    user_to_update = django_user_model.objects.get(username='mikeward')
    other_user = django_user_model.objects.get(username='socrates')
    client.force_login(user_to_update)
    url = reverse('users:update', kwargs={'pk': user_to_update.pk})
    data = {
        'username': other_user.username,
        'first_name': user_to_update.first_name,
        'last_name': user_to_update.last_name,
        'password1': 'pass123',
        'password2': 'pass123',
    }
    response = client.post(url, data, follow=True)

    assert response.status_code == 200
    assert 'form' in response.context
    form = response.context['form']
    assert form.errors
    assert 'username' in form.errors
    assert any(
        'Пользователь с таким именем уже существует.' in e
        for e in form.errors['username']
    )
    assert django_user_model.objects.filter(
        username=other_user.username).count() == 1
    assert django_user_model.objects.filter(
        username=user_to_update.username).count() == 1


# ----- Create (register) testing -----------------------------------
# ---- Navbar testing ----
def test_register_link_visibility(client, load_users, django_user_model):
    url = reverse('index')
    register_url = reverse('users:create')

    # nobody is authenticated
    unauthenticated_response = client.get(url)
    assert register_url in unauthenticated_response.text

    # somebody is authenticated
    authenticated_user = django_user_model.objects.get(pk=2)
    client.force_login(authenticated_user)
    authenticated_response = client.get(url)
    assert register_url not in authenticated_response.text


def test_create_user(client, user_data, django_user_model):
    url = reverse('users:create')
    response = client.post(url, user_data, follow=True)

    assert_redirected_with_message(
        response,
        reverse('login'),
        'Пользователь успешно зарегистрирован'
    )
    user = django_user_model.objects.get(username=user_data['username'])
    assert user.first_name == user_data['first_name']
    assert user.last_name == user_data['last_name']
    assert user.check_password(user_data['password1'])


def test_create_user_with_existing_username(
        client, user_data, django_user_model):
    django_user_model.objects.create_user(
        username=user_data['username'], password='testpass'
    )
    url = reverse('users:create')
    response = client.post(url, user_data, follow=True)

    assert response.status_code == 200

    assert 'form' in response.context
    form = response.context['form']
    assert form.errors
    assert 'username' in form.errors
    assert any('Пользователь с таким именем уже существует.' in e
               for e in form.errors['username'])
    assert django_user_model.objects.filter(
        username=user_data['username']).count() == 1
