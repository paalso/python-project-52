import pytest
from django.db.utils import IntegrityError

from task_manager.users.models import CustomUser


@pytest.fixture
def user_data():
    return {
        'username': 'dick',
        'first_name': 'Dick',
        'last_name': 'Johnson',
        'password': 'pass123',
    }


@pytest.mark.django_db
def test_custom_user_name_unique(user_data):
    CustomUser.objects.create_user(**user_data)
    with pytest.raises(IntegrityError):
        CustomUser.objects.create_user(**user_data)


@pytest.mark.django_db
@pytest.mark.parametrize(
    'pk, expected',
    [
        (1, 'admin'),
        (2, 'Mike Ward'),
        (3, 'Socrates'),
    ],
    ids=['admin', 'mikeward', 'socrates']
)
def test_custom_user_str(load_users, pk, expected):
    user = CustomUser.objects.get(pk=pk)
    assert str(user) == expected
