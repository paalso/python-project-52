# task_manager/tasks/filters.py
import django_filters
from django import forms

from task_manager.labels.models import Label
from task_manager.statuses.models import Status
from task_manager.users.models import CustomUser

from .models import Task


class TaskFilter(django_filters.FilterSet):
    status = django_filters.ModelChoiceFilter(
        queryset=Status.objects.all(), label='Статус')

    executor = django_filters.ModelChoiceFilter(
        queryset=CustomUser.objects.all(), label='Исполнитель')
    label = django_filters.ModelChoiceFilter(  # custom name
        field_name='labels',
        queryset=Label.objects.all(),
        label='label'
    )
    self_tasks = django_filters.BooleanFilter(  # custom name
        method='filter_only_my_tasks',
        label='self_tasks',
        widget=forms.CheckboxInput()
    )

    def filter_only_my_tasks(self, queryset, name, value):
        if value and self.request.user.is_authenticated:
            return queryset.filter(author=self.request.user)
        return queryset

    class Meta:
        model = Task
        fields = ['status', 'executor', 'label', 'self_tasks']
