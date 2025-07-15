import logging

from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _
from django.views.generic import (
    CreateView,
    DeleteView,
    ListView,
    UpdateView,
)

from task_manager.utils.request import format_ip_log

from .forms import LabelForm
from .models import Label

logger = logging.getLogger(__name__)


class LabelListView(ListView):
    model = Label
    context_object_name = 'labels'
    template_name = 'labels/list.html'


class LabelUpdateView(LoginRequiredMixin, UpdateView):
    model = Label
    form_class = LabelForm
    template_name = 'labels/update.html'
    success_url = reverse_lazy('labels:list')

    def form_valid(self, form):
        response = super().form_valid(form)
        label = form.instance
        messages.success(self.request, _('Label successfully updated'))
        logger.info(f'✏️ Label successfully updated: {label} '
                    f'{format_ip_log(self.request)}')
        return response


class LabelCreateView(LoginRequiredMixin, CreateView):
    model = Label
    form_class = LabelForm
    template_name = 'labels/create.html'
    success_url = reverse_lazy('labels:list')

    def form_valid(self, form):
        response = super().form_valid(form)
        label = form.instance
        messages.success(self.request, _('Label successfully created'))
        logger.info(f'✅ New label created: {label} '
                    f'{format_ip_log(self.request)}')
        return response


class LabelDeleteView(LoginRequiredMixin, DeleteView):
    model = Label
    template_name = 'labels/delete.html'
    success_url = reverse_lazy('labels:list')
    context_object_name = 'label'

    def post(self, request, *args, **kwargs):
        label = self.get_object()
        if self._is_in_use(label):
            messages.error(
                request,
                _('Cannot delete label because '
                  'it is in use by one or more tasks.')
            )
            logger.warning(
                f'⚠️ Attempted to delete label in use: '
                f'{label} {format_ip_log(request)}'
            )
        else:
            label.delete()
            messages.success(request, _('Label successfully deleted'))
            logger.info(
                f'❌ Label deleted: {label} {format_ip_log(request)}'
            )
        return redirect(self.success_url)

    @staticmethod
    def _is_in_use(label):
        return label.task_set.exists()
