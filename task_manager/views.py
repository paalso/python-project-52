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
        logger.info(f'User: {user}, authenticated: {user.is_authenticated}')
        return render(request, 'index.html')


class LoginUserView(LoginView):
    template_name = 'login.html'
    authentication_form = LoginForm

    def form_valid(self, form):
        messages.success(self.request, _('You are logged in.'))
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, _(
            'Please enter the correct user name and password.'
            'Both fields may be case sensitive.'))
        return super().form_invalid(form)
