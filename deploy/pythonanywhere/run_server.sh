#!/bin/bash

# Activate virtualenv, load envs and run Django dev server (for testing)
cd "$(dirname "$0")/.."

source .venv/bin/activate
source deploy/load_env.sh

echo "Starting Django app at http://127.0.0.1:8000/"
python manage.py runserver
