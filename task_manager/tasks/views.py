import logging

from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _
from django.views.generic import CreateView, DeleteView, DetailView, UpdateView
from django_filters.views import FilterView

from task_manager.mixins import StrictLoginRequiredMessageMixin
from task_manager.utils.request import format_ip_log

from .filters import TaskFilter
from .forms import TaskForm
from .models import Task

logger = logging.getLogger(__name__)


class TaskListView(StrictLoginRequiredMessageMixin, FilterView):
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
        response = super().form_valid(form)
        task = form.instance
        messages.success(self.request, _('Task successfully updated'))
        logger.info(f'✏️ Task updated: {task} '
                    f'{format_ip_log(self.request)}')
        return response


class TaskDeleteView(LoginRequiredMixin, DeleteView):
    model = Task
    template_name = 'tasks/delete.html'
    success_url = reverse_lazy('tasks:list')
    context_object_name = 'task'

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return self.handle_no_permission()

        self.object = self.get_object()
        if self.object.author != request.user:
            messages.error(request, _('Only the author can delete the task.'))
            message = (f'🚫 Attempt to delete task {self.object} '
                       f'with foreign authorization {format_ip_log(request)}')
            logger.warning(message)
            return redirect(self.success_url)

        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        logger.info(f'🗑️ Task deleted: {self.object} {format_ip_log(request)}')
        messages.success(request, _('Task successfully deleted'))
        return super().post(request, *args, **kwargs)
