import pytest
from django.utils import translation


@pytest.fixture
def authenticated_client(client, django_user_model):
    user = django_user_model.objects.create_user(
        username='testuser', password='testpass'
    )
    client.force_login(user)
    client.user = user
    return client


@pytest.fixture(autouse=True)
def activate_ru_locale():
    translation.activate('ru')
    yield
    translation.deactivate()
