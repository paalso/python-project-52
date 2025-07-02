import logging

from django.contrib import messages
from django.contrib.auth.views import LoginView
from django.shortcuts import render
from django.utils.translation import gettext_lazy as _
from django.views import View

from task_manager.forms import LoginForm

logger = logging.getLogger(__name__)


class IndexView(View):
    def get(self, request, *args, **kwargs):
        user = request.user
        logger.debug(f'👁 Index page viewed by {user}')
        return render(request, 'index.html')


class LoginUserView(LoginView):
    template_name = 'login.html'
    authentication_form = LoginForm

    def form_valid(self, form):
        response = super().form_valid(form)
        user = self.request.user
        ip = self.request.META.get('REMOTE_ADDR', 'unknown')
        messages.success(self.request, _('You are logged in.'))
        logger.info(f'🔐 {user} successfully logged in from IP={ip}')
        return response
