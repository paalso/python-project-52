import datetime

import pytest
from django.db.utils import IntegrityError

from task_manager.statuses.models import Status


@pytest.mark.django_db
def test_status_creation():
    status = Status.objects.create(name='в работе')
    assert status.name == 'в работе'
    assert isinstance(status.created_at, datetime.datetime)


@pytest.mark.django_db
def test_status_str_representation():
    status = Status(name='тест')
    assert str(status) == 'тест'


@pytest.mark.django_db
def test_status_name_unique():
    Status.objects.create(name='дубликат')
    with pytest.raises(IntegrityError):
        Status.objects.create(name='дубликат')
