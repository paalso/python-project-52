from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.views import View

from task_manager.users.models import CustomUser

class IndexView(View):
    def get(self, request, *args, **kwargs):
        template_name = 'users/list.html'
        users = CustomUser.objects.all()
        print(users)
        return render(
            request,
            template_name,
            context={'users': users}
        )