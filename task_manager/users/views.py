import logging

from django.contrib import messages
from django.contrib.auth import logout
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.views import LogoutView
from django.db.models.deletion import ProtectedError
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _
from django.views import View
from django.views.generic import CreateView, ListView, UpdateView

from task_manager.utils.request import format_ip_log

from .forms import CustomUserForm, CustomUserUpdateForm
from .mixins import UserAccessMixin
from .models import CustomUser

logger = logging.getLogger(__name__)


class UserListView(ListView):
    model = CustomUser
    context_object_name = 'users'
    template_name = 'users/list.html'

    def get(self, request, *args, **kwargs):
        logger.info(f'👥 User list viewed by {self.request.user} '
                     f'{format_ip_log(self.request)}')
        return super().get(request, *args, **kwargs)


class UserRegisterView(CreateView):
    form_class = CustomUserForm
    template_name = 'users/register.html'
    success_url = reverse_lazy('login')

    def form_valid(self, form):
        response = super().form_valid(form)
        user = form.instance
        messages.success(self.request, _('User successfully registered'))
        logger.info(f'🆕👤 New user registered: {user} '
                    f'{format_ip_log(self.request)}')
        return response


class UserLogoutView(LogoutView):
    next_page = 'index'
    
    def post(self, request, *args, **kwargs):
        user = request.user
        logger.info(
            f'🚪 {user} logged out {format_ip_log(self.request)}')
        messages.info(
            request, _('You have successfully logged out of the system'))
        return super().post(request, *args, **kwargs)


class UserUpdateView(
    LoginRequiredMixin, UserAccessMixin, UserPassesTestMixin, UpdateView):
    model = CustomUser
    form_class = CustomUserUpdateForm
    template_name = 'users/update.html'
    success_url = reverse_lazy('users:list')

    def test_func(self):
        return self.request.user.pk == self.kwargs['pk']

    def form_valid(self, form):
        user = form.instance
        logger.info(
            f'✅ User {user} was successfully updated '
            f'{format_ip_log(self.request)}')
        messages.success(
            self.request,
            _('User successfully updated'))
        return super().form_valid(form)


# TODO: refactor using generic views and mixins
class UserDeleteView(View):
    redirect_url = reverse_lazy('users:list')

    def get(self, request, pk):
        check = self._check_permissions(request, pk)
        if check:
            return check
        return render(request, 'users/delete.html')

    def post(self, request, pk):
        check = self._check_permissions(request, pk)
        if check:
            return check

        user = get_object_or_404(CustomUser, pk=pk)

        if request.POST.get('confirm') != 'true':
            return redirect(self.redirect_url)

        try:
            logger.info(f'📄 Current user: {user} '
                        f'{format_ip_log(self.request)}')
            user.delete()
            logout(request)
            messages.success(request, _('User was successfully deleted.'))
            logger.info(f'🗑️ Deleting user: {user} '
                        f'{format_ip_log(self.request)}')
        except ProtectedError:
            messages.error(
                request,
                _('Cannot delete user because '
                  'it is in use by one or more tasks.')
            )
            logger.warning(
                f'⚠️ Attempted to delete user in use: '
                f'{user} {format_ip_log(request)}'
            )

        return redirect(self.redirect_url)

    def _check_permissions(self, request, pk):
        if not request.user.is_authenticated:
            messages.error(request, _(
                'You are not authorized! Please log in.'))
            return redirect('login')

        if request.user.pk != pk:
            messages.error(request, _(
                'You do not have permission to modify another user.'))
            return redirect('users:list')

        return None
