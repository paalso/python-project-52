# task_manager/users/views.py
import logging

from django.contrib import messages
from django.contrib.auth.views import LogoutView
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _
from django.views import View
from django.views.generic import CreateView, UpdateView

from .forms import CustomUserForm, CustomUserUpdateForm
from .models import CustomUser

logger = logging.getLogger(__name__)


class UserListView(View):
    def get(self, request, *args, **kwargs):
        logger.debug(f'👥 User list viewed by {request.user}')
        users = CustomUser.objects.all()
        return render(request, 'users/list.html', context={'users': users})


class UserRegisterView(CreateView):
    form_class = CustomUserForm
    template_name = 'users/register.html'
    success_url = reverse_lazy('login')

    def form_valid(self, form):
        response = super().form_valid(form)
        user = form.instance
        messages.success(
            self.request,
            _('The user successfully registered')
        )
        logger.info(
            f'🆕👤 New user registered: {user}')
        return response


class UserLogoutView(LogoutView):
    def post(self, request, *args, **kwargs):
        user = request.user
        ip = request.META.get('REMOTE_ADDR', 'unknown')
        logger.info(f'🚪 {user} logged out from IP={ip}')
        messages.info(
            request, _('You have successfully logged out of the system'))
        return super().post(request, *args, **kwargs)


class UserUpdateView(UpdateView):
    model = CustomUser
    form_class = CustomUserUpdateForm
    template_name = 'users/update.html'
    success_url = reverse_lazy('users:list')

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            messages.error(
                request, _('You are not authorized! Please log in.'))
            return redirect('login')

        if request.user.pk != kwargs['pk']:
            messages.error(
                request, _('You do not have permission to edit another user.'))
            return redirect('users:list')

        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        response = super().form_valid(form)
        user = form.instance
        ip = self.request.META.get('REMOTE_ADDR', 'unknown')
        messages.success(
            self.request,
            _('The user successfully updated')
        )
        logger.info(
            f'✅ The user {user} was successfully updated from ip {ip}')
        return response


class UserDeleteView(View):
    def get(self, request, pk):
        user = request.user
        logger.debug(f'ℹ️ Current user: {user}')

        if not request.user.is_authenticated:
            messages.error(
                request, _('You are not authorized! Please log in.'))
            return redirect('login')

        if user.pk != pk:
            messages.error(
                request, _('You do not have permission to edit another user.'))
            return redirect('users:list')

        logger.debug(f'ℹ️ request: {request}')
        return render(
            request, 'users/delete.html'
        )

    def post(self, request, pk):
        deletion_confirm = request.POST.get('confirm') == 'true'
        user = CustomUser.objects.get(pk=pk)
        if deletion_confirm and user:
            ip = self.request.META.get('REMOTE_ADDR', 'unknown')
            user.delete()
            messages.success(
                self.request,
                _('The user successfully deleted')
            )
            logger.debug(f'🗑️ {user} successfully deleted from ip {ip}')
        return redirect('users:list')
