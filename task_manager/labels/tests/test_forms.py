import pytest

from task_manager.labels.forms import LabelForm
from task_manager.labels.models import Label


@pytest.mark.django_db
def test_valid_create_user_form():
    label = {'name': 'some label'}
    form = LabelForm(data=label)
    assert form.is_valid()


@pytest.mark.django_db
def test_label_not_unique():
    Label.objects.create(name='not unique label')
    label = {'name': 'not unique label'}
    form = LabelForm(data=label)
    assert not form.is_valid()
    assert 'name' in form.errors
    error_message = 'уже существует'
    assert any(error_message in e for e in form.errors['name'])


@pytest.mark.django_db
def test_label_name_required():
    form = LabelForm(data={'name': ''})
    assert not form.is_valid()
    assert 'name' in form.errors
    print(f'form.errors: {form.errors}')
    assert any('обязательное' in e.lower() for e in form.errors['name'])


@pytest.mark.django_db
def test_label_name_too_long():
    long_name = 'very long label name ' * 5
    form = LabelForm(data={'name': long_name})
    assert not form.is_valid()
    assert 'name' in form.errors
