import pytest
from django.urls import reverse


# ----- Read testing ------------------------------------------------
@pytest.mark.django_db
def test_tasks_list_view(client):
    url = reverse('tasks:list')
    response = client.get(url)

    assert response.status_code == 200
    assert 'tasks' in response.context

    content = response.content.decode()

    assert 'name="status"' in content
    assert 'id="id_status"' in content

    assert 'name="executor"' in content
    assert 'id="id_executor"' in content

    assert 'name="label"' in content
    assert 'id="id_label"' in content

    assert 'name="self_tasks"' in content
    assert 'id="id_self_tasks"' in content
