import logging

from django.http import HttpResponse
from django.views.generic import (
    ListView,
)

# from .forms import StatusForm
# from .models import Status

logger = logging.getLogger(__name__)


class TaskListView(ListView):
    def get(self, request, *args, **kwargs):
        return HttpResponse('Task list must be implemented here')
