from django.contrib import messages
from django.shortcuts import redirect
from django.utils.translation import gettext_lazy as _


class UserAccessMixin:
    """Mixin for processing access refusals."""

    def handle_no_permission(self):
        if not self.request.user.is_authenticated:
            messages.error(self.request,
                           _('You are not authorized! Please log in.'))
            return redirect('login')

        messages.error(self.request,
                       _('You do not have permission to edit another user.'))

        return redirect('users:list')
