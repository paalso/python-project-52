import pytest

from task_manager.forms import LoginForm

data = {'username': 'testuser', 'password': 'pass123'}


@pytest.fixture
def create_user(django_user_model):
    django_user_model.objects.create_user(**data)


@pytest.mark.django_db
def test_login_form_valid(create_user):
    form = LoginForm(data=data)
    assert form.is_valid()


@pytest.mark.django_db
def test_login_form_empty_data():
    form = LoginForm(data={})
    errors = form.errors
    assert not form.is_valid()
    assert 'username' in errors and 'password' in errors


@pytest.mark.django_db
@pytest.mark.parametrize('data', [
    {'username': 'testuser', 'password': ''},
    {'username': '', 'password': 'pass123'},
])
def test_login_form_partial_data(data):
    form = LoginForm(data=data)
    errors = form.errors
    assert not form.is_valid()
    assert errors


@pytest.mark.parametrize('data_spoiler', [
    {'username': 'wrong'},
    {'password': 'wrong'},
])
@pytest.mark.django_db
def test_login_form_invalid2(create_user, data_spoiler):
    error_data = data | data_spoiler
    form = LoginForm(data=error_data)
    error_message = \
        ('Пожалуйста, введите правильные имя пользователя и пароль. '
         'Оба поля могут быть чувствительны к регистру.')
    assert not form.is_valid()
    assert error_message in form.non_field_errors()
