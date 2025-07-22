
import pytest

from task_manager.tasks.forms import TaskForm
from task_manager.tests.builders import build_label


@pytest.mark.django_db
def test_task_form_valid(task_data):
    task_data['labels'] = [build_label(f'label{i}') for i in range(2)]
    form = TaskForm(data=task_data)
    assert form.is_valid()


@pytest.mark.django_db
def test_task_form_valid_without_labels(task_data):
    form = TaskForm(data=task_data)
    assert form.is_valid()


@pytest.mark.django_db
@pytest.mark.parametrize('missing_field', ['name', 'status', 'executor'])
def test_task_form_missing_required_fields(task_data, missing_field):
    task_data.pop(missing_field)
    form = TaskForm(data=task_data)
    assert not form.is_valid()
    assert missing_field in form.errors
