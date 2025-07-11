# task_manager/tasks/views.py
import logging

from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import CreateView, DeleteView, UpdateView
from django_filters.views import FilterView

from .filters import TaskFilter
from .models import Task

logger = logging.getLogger(__name__)


class TaskListView(FilterView):
    model = Task
    filterset_class = TaskFilter
    template_name = 'tasks/list.html'
    context_object_name = 'tasks'

    def get_filterset(self, filterset_class):
        return filterset_class(
            self.request.GET,
            request=self.request,
            queryset=self.get_queryset()
        )


class TaskCreateView(LoginRequiredMixin, CreateView):
    pass


class TaksUpdateView(LoginRequiredMixin, UpdateView):
    pass


class TaskDeleteView(LoginRequiredMixin, DeleteView):
    pass
