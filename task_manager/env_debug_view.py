import os

from django.http import JsonResponse
from django.views import View


class EnvDebugView(View):
    def get(self, request):
        env_vars = {
            'DEBUG': os.getenv('DEBUG'),
            'ALLOWED_HOSTS': os.getenv('ALLOWED_HOSTS'),
            'DATABASE_URL': os.getenv('DATABASE_URL'),
            'TIMEZONE': os.getenv('TIMEZONE'),
        }
        return JsonResponse(env_vars)
