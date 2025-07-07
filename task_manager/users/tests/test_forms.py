import pytest

from task_manager.users.forms import (
    CustomUserCreationForm,
    CustomUserUpdateForm,
)


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

    form = CustomUserUpdateForm(data=user_data)
    assert form.is_valid()
#
#
# def test_password_mismatch(user_data, django_user_model):
#     user_data['password2'] = 'different123'
#     form = CustomUserCreationForm(data=user_data)
#     assert not form.is_valid()
#     assert 'password2' in form.errors
