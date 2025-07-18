import pytest
from django.urls import reverse

from task_manager.tests.utils import assert_redirected_with_message

data = {'username': 'testuser', 'password': 'pass123'}


@pytest.fixture
def create_user(django_user_model):
    django_user_model.objects.create_user(**data)


@pytest.mark.django_db
def test_login_view_success(client, create_user):
    response = client.post(reverse('login'), data, follow=False)

    assert response.status_code == 302
    assert '_auth_user_id' in client.session

    response = client.post(reverse('login'), data, follow=True)

    assert_redirected_with_message(
        response,
        reverse('index'),
        'Вы залогинены'
    )


@pytest.mark.django_db
def test_login_view_invalid(client, create_user):
    response = client.post(reverse('login'), {
        'username': 'wrong',
        'password': 'wrong',
    })
    error_message = \
        ('Пожалуйста, введите правильные имя пользователя и пароль. '
         'Оба поля могут быть чувствительны к регистру.')

    assert response.status_code == 200
    assert error_message in response.text
    assert '_auth_user_id' not in client.session
