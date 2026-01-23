[![CI](https://github.com/paalso/python-project-52/actions/workflows/ci.yml/badge.svg)](https://github.com/paalso/python-project-52/actions/workflows/ci.yml)
[![codecov](https://codecov.io/github/paalso/python-project-52/graph/badge.svg?token=P8H6NHLCMW)](https://codecov.io/github/paalso/python-project-52)

## Level 4 project, program Python developer
### Менеджер задач (Task Manager)

## 📚 About
Task Manager is a lightweight [Redmine](https://www.redmine.org/)-like system built with Django.
It uses Django Templates for server-side rendering and Bootstrap 5 for responsive design.

## Features
- 📝 Create and edit tasks

- 👤 Assign tasks to users

- 📌 Add multiple labels per task

- 🔄 Manage statuses (new, in progress, testing, completed, etc.)

- 🔍 Filter tasks by status, executor, labels, and author

- ✅ User registration and authentication

##  🛠️ Tech Stack
- Python 3.13

- Django 4+

- Bootstrap 5

- SQLite (default, can be swapped for PostgreSQL/MySQL)

- Optional .env support for environment management

## 🗂️ Project Structure (Brief)
```bash
task_manager/
├── users/         # User registration & management
├── tasks/         # Core task CRUD & filters
├── statuses/      # Manage task statuses
├── labels/        # Label creation and assignment
├── templates/     # Shared and base templates
├── locale/        # i18n translations (ru, ua)
├── utils/         # Request helpers, mixins
├── tests/         # Extensive unit tests
└── settings.py    # Project configuration
```

## 🛠️ Installation for Developers
To run the app locally in a development environment:

```bash
# Clone the repository
git clone https://github.com/paalso/python-project-83.git
cd python-project-83

# Install Python dependencies inside a virtual environment
make install

# Copy example environment and edit it if needed
cp .env_copy .env

# Run the app with hot reload (for development)
make dev
```
### 🔧 Notes:
You can edit `.env` to change database connection, debug mode, etc.

`make install` creates a virtual environment and installs dependencies using `uv`.

`make dev` runs the app with uvicorn in development mode (auto-reload enabled).

Ensure PostgreSQL is running locally or set up a remote `DATABASE_URL` in `.env`.

## 🚀 Demo
Live demo deployed on PythonAnywhere:
👉 [https://paalso.pythonanywhere.com/](https://paalso.pythonanywhere.com/)

To explore the system, register a new user and start managing tasks.

## 📄 Deployment
Deployment instructions for PythonAnywhere are available in [deploy/pythonanywhere/README.md](deploy/pythonanywhere/README.md)

## ✅ Status
✔️ Feature complete

🧪 Covered with unit tests

🌍 Localization supported (ru)

