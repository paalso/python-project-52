from django.views.generic import ListView, UpdateView, View

from .models import Status


class StatusListView(ListView):
    model = Status
    context_object_name = 'status'
    template_name = 'statuses/list.html'


class StatusUpdateView(UpdateView):
    pass


class StatusDeleteView(View):
    pass
