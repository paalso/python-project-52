import logging

from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _
from django.views.generic import CreateView, ListView, UpdateView, View

from task_manager.utils.request import format_ip_log

from .forms import StatusForm
from .models import Status

logger = logging.getLogger(__name__)


class StatusListView(ListView):
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


class StatusDeleteView(View):
    pass
