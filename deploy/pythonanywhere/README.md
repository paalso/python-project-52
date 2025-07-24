# Deploying on [PythonAnywhere](https://www.pythonanywhere.com)

## 📦 Cloning and installing dependencies

```bash
git clone https://github.com/paalso/python-project-52.git
cd python-project-52
python3.13 -m venv .venv
source .venv/bin/activate
deploy/extract_deps.sh -p pyproject.toml
pip install -r requirements.txt
```

### ⚙️ Environment variables
```bash
cp deploy/pythonanywhere/.env_copy .env
source deploy/pythonanywhere/load_env.sh
```

`.env` should  contain something like:
```bash
DEBUG=False
SECRET_KEY=some-secret-key
ALLOWED_HOSTS=paalso.pythonanywhere.com
DATABASE_URL=sqlite:////home/paalso/python-project-52/db.sqlite3
```

### 🗄️ Migrations and database
```bash
python manage.py migrate
```

### 🕸️ PythonAnywhere configuration
Source code: `/home/paalso/python-project-52`

Virtualenv: `/home/paalso/python-project-52/.venv`

WSGI config:
```python
import os
import sys
from pathlib import Path

project_folder = Path(__file__).resolve().parent.parent / 'python-project-52'

path = '/home/paalso/python-project-52/'
if path not in sys.path:
    sys.path.insert(0, path)

os.environ['DJANGO_SETTINGS_MODULE'] = 'task_manager.settings'

# ruff: noqa: E402
from django.core.wsgi import get_wsgi_application

application = get_wsgi_application()
```

Make sure this is saved to your WSGI file, e.g.:

```bash
/var/www/paalso_pythonanywhere_com_wsgi.py
```

### 🛜 Reload
Go to the PythonAnywhere [Web tab](https://www.pythonanywhere.com/user/paalso/webapps/) and click Reload.

### ✅ Check
Go to the browser:
👉 [https://paalso.pythonanywhere.com](https://paalso.pythonanywhere.com)
