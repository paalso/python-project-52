import logging

from django.conf import settings
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from django.utils.translation import gettext_lazy as _

from task_manager.utils.request import format_ip_log

logger = logging.getLogger(__name__)


class StrictLoginRequiredMessageMixin(LoginRequiredMixin):
    login_message = _('You are not authorized! Please log in.')

    def handle_no_permission(self):
        request = self.request
        if not request.user.is_authenticated:
            messages.error(request, self.login_message)
            full_path = request.get_full_path()
            logger.warning(
                f'🚫 Unauthorized attempt to access '
                f'{full_path} {format_ip_log(request)}'
            )
            return redirect(settings.LOGIN_URL)
        return super().handle_no_permission()
