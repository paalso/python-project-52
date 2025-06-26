from django.shortcuts import render
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