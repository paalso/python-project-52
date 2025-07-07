import pytest

from task_manager.users.forms import CustomUserCreationForm


@pytest.fixture
def user_data():
    return {
        'username': 'dick',
        'first_name': 'Dick',
        'last_name': 'Johnson',
        'password1': 'pass123',
        'password2': 'pass123',
    }


def test_valid_user_forms(user_data, django_user_model):
    form = CustomUserCreationForm(data=user_data)
    assert form.is_valid()


def test_password_mismatch(user_data, django_user_model):
    user_data['password2'] = 'different123'
    form = CustomUserCreationForm(data=user_data)
    assert not form.is_valid()
    assert 'password2' in form.errors
    error_message = ('Введенные пароли не совпадают.')
    assert any(error_message in e for e in form.errors['password2'])


@pytest.mark.django_db
def test_password_too_short(user_data):
    user_data['password1'] = user_data['password2'] = 'pw'
    form = CustomUserCreationForm(data=user_data)
    assert not form.is_valid()
    assert 'password2' in form.errors
    error_message = ('Введённый пароль слишком короткий. '
                     'Он должен содержать как минимум 3 символа.')
    assert any(error_message in e for e in form.errors['password2'])


@pytest.mark.django_db
def test_username_not_unique_on_create_or_update(user_data, django_user_model):
    existing_user = django_user_model.objects.create_user(
        username='user1', password='pass123')
    form_data = {
        'username': existing_user.username,
        'password1': 'pass123',
        'password2': 'pass123',
    }
    form = CustomUserCreationForm(data=form_data)

    assert not form.is_valid()
    assert 'username' in form.errors
    error_message = 'Пользователь с таким именем уже существует.'
    assert any(error_message in e for e in form.errors['username'])
