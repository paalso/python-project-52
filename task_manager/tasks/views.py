import logging

from django.http import HttpResponse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _
from django.views.generic import (
    ListView, CreateView, UpdateView, DeleteView
)

# from .forms import StatusForm
from .models import Task

logger = logging.getLogger(__name__)


class TaskListView(ListView):
    model = Task
    context_object_name = 'tasks'
    template_name = 'tasks/list.html'


class TaskCreateView(LoginRequiredMixin, CreateView):
    pass


class TaksUpdateView(LoginRequiredMixin, UpdateView):
    pass


class TaskDeleteView(LoginRequiredMixin, DeleteView):
    pass
