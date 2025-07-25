# task_manager/tasks/filters.py
import django_filters
from django import forms

from task_manager.labels.models import Label
from task_manager.statuses.models import Status
from task_manager.users.models import CustomUser

from .models import Task


class TaskFilter(django_filters.FilterSet):
    status = django_filters.ModelChoiceFilter(
        queryset=Status.objects.all(),
        label='Статус',
        widget=forms.Select(
            attrs={"class": "form-select mr-3 ml-2", "id": "id_status"})
    )

    executor = django_filters.ModelChoiceFilter(
        queryset=CustomUser.objects.all(),
        label='Исполнитель',
        widget=forms.Select(
            attrs={"class": "form-select mr-3 ml-2", "id": "id_executor"})
    )

    label = django_filters.ModelChoiceFilter(
        field_name='labels',
        queryset=Label.objects.all(),
        label='Метка',
        widget=forms.Select(
            attrs={"class": "form-select mr-3 ml-2", "id": "id_label"})
    )

    self_tasks = django_filters.BooleanFilter(
        method='filter_only_my_tasks',
        label='Только свои задачи',
        widget=forms.CheckboxInput(
            attrs={"class": "form-check-input mr-3", "id": "id_self_tasks"})
    )

    def filter_only_my_tasks(self, queryset, name, value):
        if value and self.request.user.is_authenticated:
            return queryset.filter(author=self.request.user)
        return queryset

    class Meta:
        model = Task
        fields = ['status', 'executor', 'label', 'self_tasks']
