import pytest
from django.urls import reverse

from task_manager.statuses.models import Status


@pytest.fixture
def fill_statuses():
    Status.objects.create(name='новый')
    Status.objects.create(name='в работе')


# ----- Read testing ------------------------------------------------
@pytest.mark.django_db
def test_statuses_list_view(client, fill_statuses):
    url = reverse('statuses:list')
    response = client.get(url)

    assert response.status_code == 200
    assert 'statuses/list.html' in (t.name for t in response.templates)
    assert 'statuses' in response.context

    statuses = response.context['statuses']
    print(statuses)
    names = [status.name for status in statuses]
    assert 'новый' in names
    assert 'в работе' in names
