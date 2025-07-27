import os
import platform
import sys

from django.http import JsonResponse
from django.utils.timezone import now


def get_debug_info(request):
    debug_info = {
        'env': {
            'DEBUG': os.getenv('DEBUG'),
            'ALLOWED_HOSTS': os.getenv('ALLOWED_HOSTS'),
            # 'DATABASE_URL': os.getenv('DATABASE_URL'),
            'TIMEZONE': os.getenv('TIMEZONE'),
        },
        'request': {
            'host': request.get_host(),
            'path': request.path,
            'method': request.method,
            'user_agent': request.META.get('HTTP_USER_AGENT'),
            'ip': request.META.get('REMOTE_ADDR'),
            'lang': request.LANGUAGE_CODE,
            'user': (str(request.user) if request.user.is_authenticated
                     else 'Anonymous'),
        },
        'server': {
            'timestamp': now().isoformat(),
            'python_version': sys.version,
            'platform': platform.platform(),
        }
    }

    return JsonResponse(debug_info)
