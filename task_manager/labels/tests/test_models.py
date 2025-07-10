import datetime

import pytest
from django.db.utils import IntegrityError

from task_manager.labels.models import Label


@pytest.mark.django_db
def test_label_creation():
    label = Label.objects.create(name='в работе')
    assert label.name == 'в работе'
    assert isinstance(label.created_at, datetime.datetime)


@pytest.mark.django_db
def test_label_str_representation():
    label = Label(name='тест')
    assert str(label) == 'тест'


@pytest.mark.django_db
def test_label_name_unique():
    Label.objects.create(name='дубликат')
    with pytest.raises(IntegrityError):
        Label.objects.create(name='дубликат')
