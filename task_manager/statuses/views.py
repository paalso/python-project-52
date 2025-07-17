import logging

from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models.deletion import ProtectedError
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _
from django.views.generic import (
    CreateView,
    DeleteView,
    ListView,
    UpdateView,
)

from task_manager.mixins import StrictLoginRequiredMessageMixin
from task_manager.utils.request import format_ip_log

from .forms import StatusForm
from .models import Status

logger = logging.getLogger(__name__)


class StatusListView(StrictLoginRequiredMessageMixin, ListView):
    model = Status
    context_object_name = 'statuses'
    template_name = 'statuses/list.html'


class StatusUpdateView(LoginRequiredMixin, UpdateView):
    model = Status
    form_class = StatusForm
    template_name = 'statuses/update.html'
    success_url = reverse_lazy('statuses:list')

    def form_valid(self, form):
        response = super().form_valid(form)
        status = form.instance
        messages.success(self.request, _('Status successfully updated'))
        logger.info(f'✏️ Status successfully updated: {status} '
                    f'{format_ip_log(self.request)}')
        return response


class StatusCreateView(LoginRequiredMixin, CreateView):
    model = Status
    form_class = StatusForm
    template_name = 'statuses/create.html'
    success_url = reverse_lazy('statuses:list')

    def form_valid(self, form):
        response = super().form_valid(form)
        status = form.instance
        messages.success(self.request, _('Status successfully created'))
        logger.info(f'✅ New status created: {status} '
                    f'{format_ip_log(self.request)}')
        return response


class StatusDeleteView(LoginRequiredMixin, DeleteView):
    model = Status
    template_name = 'statuses/delete.html'
    success_url = reverse_lazy('statuses:list')
    context_object_name = 'status'

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        try:
            self.object.delete()
            messages.success(request, _('Status successfully deleted'))
            logger.info(
                f'❌ Status deleted: {self.object} {format_ip_log(request)}'
            )
        except ProtectedError:
            messages.error(
                request,
                _('Cannot delete status because '
                  'it is in use by one or more tasks.')
            )
            logger.warning(
                f'⚠️ Attempted to delete status in use: '
                f'{self.object} {format_ip_log(request)}'
            )
        return redirect(self.success_url)
