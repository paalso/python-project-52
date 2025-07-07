# task_manager/users/views.py
import logging

from django.contrib import messages
from django.contrib.auth import logout
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.views import LogoutView
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _
from django.views import View
from django.views.generic import CreateView, ListView, UpdateView

from .forms import CustomUserCreationForm, CustomUserUpdateForm
from .mixins import UserAccessMixin
from .models import CustomUser

logger = logging.getLogger(__name__)


def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        return x_forwarded_for.split(",")[0].strip()
    return request.META.get('REMOTE_ADDR', 'unknown')


def format_ip_log(request, label='from IP', sep='='):
    ip = get_client_ip(request)
    return f'{label}{sep}{ip}'


class UserListView(ListView):
    model = CustomUser
    context_object_name = 'users'
    template_name = 'users/list.html'

    def get(self, request, *args, **kwargs):
        logger.info(f'👥 User list viewed by {self.request.user} '
                     f'{format_ip_log(self.request)}')
        return super().get(request, *args, **kwargs)


class UserRegisterView(CreateView):
    form_class = CustomUserCreationForm
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
        response = super().form_valid(form)
        user = form.instance
        logger.info(
            f'✅ User {user} was successfully updated '
            f'{format_ip_log(self.request)}')
        messages.success(
            self.request,
            _('User successfully updated'))
        return response


# TODO: refactor using generic views and mixins
class UserDeleteView(View):
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

        if request.POST.get('confirm') == 'true':
            logger.info(f'🗑️ Deleting user: {user} '
                         f'{format_ip_log(self.request)}')
            user.delete()
            logout(request)
            messages.success(request, _('User was successfully deleted.'))
            return redirect('users:list')

        return redirect('users:list')

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
