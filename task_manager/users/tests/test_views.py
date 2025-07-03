import pytest
from django.urls import reverse

from task_manager.users.models import CustomUser


@pytest.mark.django_db
def test_users_list_view(client):
    url = reverse('users:list')
    response = client.get(url)

    assert response.status_code == 200
    assert 'users/list.html' in (t.name for t in response.templates)
    assert 'users' in response.context
    assert len(response.context['users']) == CustomUser.objects.count()
