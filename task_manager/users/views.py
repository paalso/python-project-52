
from django.http import HttpResponse
from django.views import View


class IndexView(View):
    def get(self, request, *args, **kwargs):
        message = 'The list of users must be here'
        return HttpResponse(message)
