import pytest

from task_manager.statuses.forms import StatusForm
from task_manager.statuses.models import Status


@pytest.mark.django_db
def test_valid_create_user_form():
    status = {'name': 'some status'}
    form = StatusForm(data=status)
    assert form.is_valid()


@pytest.mark.django_db
def test_status_not_unique():
    Status.objects.create(name='not unique status')
    status = {'name': 'not unique status'}
    form = StatusForm(data=status)
    assert not form.is_valid()
    assert 'name' in form.errors
    error_message = 'уже существует'
    assert any(error_message in e for e in form.errors['name'])


@pytest.mark.django_db
def test_status_name_required():
    form = StatusForm(data={'name': ''})
    assert not form.is_valid()
    assert 'name' in form.errors
    print(f'form.errors: {form.errors}')
    assert any('обязательное' in e.lower() for e in form.errors['name'])


@pytest.mark.django_db
def test_status_name_too_long():
    long_name = 'very long status name' * 5
    form = StatusForm(data={'name': long_name})
    assert not form.is_valid()
    assert 'name' in form.errors
