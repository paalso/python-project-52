# ruff: noqa: E402

import os
import sys
from pathlib import Path

project_folder = Path(__file__).resolve().parent.parent / 'python-project-52'

path = '/home/paalso/python-project-52/'
if path not in sys.path:
    sys.path.insert(0, path)

os.environ['DJANGO_SETTINGS_MODULE'] = 'task_manager.settings'

from django.core.wsgi import get_wsgi_application

application = get_wsgi_application()
