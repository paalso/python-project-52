
import pytest


@pytest.fixture
def authenticated_client(client, django_user_model):
    user = django_user_model.objects.create_user(
        username='testuser', password='testpass'
    )
    client.force_login(user)
    return client
