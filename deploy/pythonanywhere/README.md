# Deploying on [PythonAnywhere](https://www.pythonanywhere.com)

## Step-by-step

1. Clone the project to PythonAnywhere
2. Create and activate virtualenv
3. Install dependencies

```bash
python3.13 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

4. Adjust .env file for production:
```bash
# .env
DEBUG=False
SECRET_KEY=your-production-key
ALLOWED_HOSTS=yourusername.pythonanywhere.com
DATABASE_URL=sqlite:////home/yourusername/python-project-52/db.sqlite3
```

5. Add environment variables and run migrations:
```bash
source deploy/load_env.sh
python manage.py migrate
```