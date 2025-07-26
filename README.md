[![CI](https://github.com/paalso/python-project-52/actions/workflows/ci.yml/badge.svg)](https://github.com/paalso/python-project-52/actions/workflows/ci.yml)
[![codecov](https://codecov.io/github/paalso/python-project-52/graph/badge.svg?token=P8H6NHLCMW)](https://codecov.io/github/paalso/python-project-52)
 [![Actions Status](https://github.com/paalso/python-project-52/actions/workflows/hexlet-check.yml/badge.svg)](https://github.com/paalso/python-project-52/actions)

## Level 4 project on [Hexlet](https://ru.hexlet.io/), program [Python developer](https://ru.hexlet.io/programs/python).
### [Менеджер задач (Task Manager)](https://ru.hexlet.io/programs/python/projects/52)

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

