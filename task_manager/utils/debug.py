import os
import platform
import sys

from django.utils.timezone import now


def get_debug_info(request):
    hostname = request.get_host()
    provider = detect_hosting_provider(hostname)

    debug_info = {
        'env': {
            'DEBUG': os.getenv('DEBUG'),
            'ALLOWED_HOSTS': os.getenv('ALLOWED_HOSTS'),
            # 'DATABASE_URL': os.getenv('DATABASE_URL'),
            'TIMEZONE': os.getenv('TIMEZONE'),
        },
        'request': {
            'host': hostname,
            'path': request.path,
            'hosting_provider': provider or {},
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

    return debug_info


def detect_hosting_provider(hostname: str) -> dict[str, str] | None:
    if hostname.startswith('127.') or 'localhost' in hostname:
        return

    known_providers = {
        'pythonanywhere.com': {
            'name': 'PythonAnywhere',
            'url': 'https://www.pythonanywhere.com/',
        },
        'vercel.app': {
            'name': 'Vercel',
            'url': 'https://vercel.com/',
        },
        'render.com': {
            'name': 'Render',
            'url': 'https://render.com/',
        },
        'railway.app': {
            'name': 'Railway',
            'url': 'https://railway.app/',
        },
    }

    for domain, info in known_providers.items():
        if hostname.rsplit('/').endswith(domain):
            return info

    return None
