import pytest

from task_manager.users.models import CustomUser


@pytest.mark.django_db
@pytest.mark.parametrize(
    'pk, expected',
    [
        (1, 'user 1 - admin, full name admin'),
        (2, 'user 2 - mikeward, full name Mike Ward'),
        (3, 'user 3 - socrates, full name Socrates'),
    ],
    ids=['admin', 'mikeward', 'socrates']
)
def test_custom_user_str(load_users, pk, expected):
    user = CustomUser.objects.get(pk=pk)
    assert str(user) == expected
