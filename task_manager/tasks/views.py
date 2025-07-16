# task_manager/tasks/views.py
import logging

from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _
from django.views.generic import CreateView, DeleteView, DetailView, UpdateView
from django_filters.views import FilterView

from task_manager.utils.request import format_ip_log

from .filters import TaskFilter
from .forms import TaskForm
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


class TaskDetailView(LoginRequiredMixin, DetailView):
    model = Task
    template_name = 'tasks/show.html'
    context_object_name = 'task'


class TaskCreateView(LoginRequiredMixin, CreateView):
    model = Task
    form_class = TaskForm
    template_name = 'tasks/create.html'
    success_url = reverse_lazy('tasks:list')

    def form_valid(self, form):
        form.instance.author = self.request.user
        response = super().form_valid(form)
        task = form.instance
        messages.success(self.request, _('Task successfully created'))
        logger.info(f'✅ New task created: {task} '
                    f'{format_ip_log(self.request)}')
        return response


class TaskUpdateView(LoginRequiredMixin, UpdateView):
    model = Task
    form_class = TaskForm
    template_name = 'tasks/update.html'
    success_url = reverse_lazy('tasks:list')

    def form_valid(self, form):
        form.instance.author = self.request.user
        response = super().form_valid(form)
        task = form.instance
        messages.success(self.request, _('Task successfully updated'))
        logger.info(f'✏️ Task updated: {task} '
                    f'{format_ip_log(self.request)}')
        return response


class TaskDeleteView(LoginRequiredMixin, DeleteView):
    pass
