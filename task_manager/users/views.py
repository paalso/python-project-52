# task_manager/users/views.py
from django.contrib import messages
from django.contrib.auth.views import LogoutView
from django.shortcuts import render
from django.urls import reverse_lazy
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
    next_page = 'index'

    def post(self, request, *args, **kwargs):
        messages.success(request, "Вы успешно вышли из системы.")
        return super().post(request, *args, **kwargs)


class UserUpdateView(View):
    def get(self, request, *args, **kwargs):
        user_id = kwargs.get('pk')
        user = CustomUser.objects.get(id=user_id)
        # form = UserForm(instance=user)
        return render(
            request, 'users/update.html'
        )


class UserDeleteView(View):
    def get(self, request, *args, **kwargs):
        user_id = kwargs.get('pk')
        user = CustomUser.objects.get(id=user_id)
        # form = UserForm(instance=user)
        return render(
            request, 'users/delete.html'
        )
