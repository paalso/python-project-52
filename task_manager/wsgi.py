# ruff: noqa: E402

"""
WSGI config for task_manager project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.2/howto/deployment/wsgi/
"""

import os
from pathlib import Path

import dotenv

# Load .env file before Django settings
project_dir = Path(__file__).resolve().parent.parent
dotenv.load_dotenv(dotenv_path=project_dir / ".env")

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'task_manager.settings')

from django.core.wsgi import get_wsgi_application

application = get_wsgi_application()
