import os

import dj_database_url
from dotenv import load_dotenv


def load_env(base_dir):
    load_dotenv(dotenv_path=base_dir / ".env")

    return {
        'DEBUG': os.getenv('DEBUG', 'False') == "True",
        'SECRET_KEY': os.getenv('SECRET_KEY'),
        'ALLOWED_HOSTS': os.getenv('ALLOWED_HOSTS', '').split(','),
        'DATABASES': {
            'default': _build_db_config()
        }
    }


def _build_db_config():
    db_url = os.getenv('DATABASE_URL')
    config = dj_database_url.parse(db_url, conn_max_age=600)
    if not config['ENGINE'].endswith('sqlite3') and \
            not os.getenv('DEBUG', 'False') == 'True':
        config['OPTIONS'] = {'sslmode': 'require'}
    return config
