# task_manager/users/views.py
from django.contrib import messages
from django.contrib.auth.views import LogoutView
from django.shortcuts import render
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _
from django.views import View
from django.views.generic import CreateView

from .forms import CustomUserCreationForm
from .models import CustomUser


class UserListView(View):
    def get(self, request, *args, **kwargs):
        users = CustomUser.objects.all()
        print(users)
        return render(
            request,
            'users/list.html',
            context={'users': users}
        )


class UserRegisterView(CreateView):
    form_class = CustomUserCreationForm
    template_name = 'users/register.html'
    success_url = reverse_lazy('index')


class UserLogoutView(LogoutView):
    def post(self, request, *args, **kwargs):
        messages.info(request,
                      _('You have successfully logged out of the system.'))
        return super().post(request, *args, **kwargs)


class UserUpdateView(View):
    def get(self, request, *args, **kwargs):
        return render(
            request, 'users/update.html'
        )


class UserDeleteView(View):
    def get(self, request, *args, **kwargs):
        return render(
            request, 'users/delete.html'
        )
