# ========================
# Django Project Makefile
# ========================

# Development server port
PORT = 8080

# Shortcut for manage.py commands
MANAGE := uv run python manage.py

# ========================
# General Commands
# ========================

.PHONY: help
help:  ## Show this help message
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-22s\033[0m %s\n", $$1, $$2}'

start:  ## Start Django development server
	@$(MANAGE) runserver 0.0.0.0:$(PORT)

setup: db-clean deps migrate  ## Clean DB, install deps and run migrations

sync:  ## Install project dependencies using uv
	@uv sync

# ========================
# Database Management
# ========================

db-clean:  ## Delete SQLite database file
	@rm -f db.sqlite3

reset-db: db-clean migrate  ## Clean and reinitialize the database

migrate:  ## Apply migrations
	@$(MANAGE) migrate

makemigrations:  ## Create new migrations
	@$(MANAGE) makemigrations

showmigrations:  ## Show current migration status
	@$(MANAGE) showmigrations

sqlite:  ## Open SQLite CLI on the project database
	sqlite3 db.sqlite3

psql:  ## Open psql CLI on the project database
	psql -U postgres -h localhost -d test -W

# ========================
# Development Tools
# ========================

shell:  ## Launch Django shell_plus with IPython
	@$(MANAGE) shell_plus --ipython

makemessages:  ## Extract translations for ru and ua
	uv run sh -c 'django-admin makemessages -l ru && django-admin makemessages -l ua'

compilemessages:  ## Compile translation files (.po -> .mo)
	uv run django-admin compilemessages

code-lint:  ## Run Ruff code linter
	@uv run ruff check task_manager

template-lint:  ## Lint Django templates with djlint
	@uv run djlint task_manager/**/templates/ --reformat --indent=2

lint:  ## Run all linters (ruff + djlint)
	@$(MAKE) code-lint
	@$(MAKE) template-lint

lint-fix:  ## Auto-fix linting issues using ruff
	@uv run ruff check --fix task_manager

format:  ## Format code using ruff
	@uv run ruff format task_manager

qa:  ## Run all linters + tests + template lint
	@$(MAKE) lint
	@$(MAKE) test

cov:  ## Run tests with coverage report
	@uv run coverage run -m pytest
	@uv run coverage report -m
	@uv run coverage html && echo "Open htmlcov/index.html"

test:  ## Run tests (optionally: NAME=tests/test_users.py or -k keyword)
	@uv run pytest -v $(NAME)

test-nodeid:  ## Run single test by nodeid: NODEID=tests/test_users.py::test_login
	@uv run pytest -v $(NODEID)

clean:  ## Remove .pyc, __pycache__, coverage, translations, htmlcov
	find . -name '*.pyc' -delete
	find . -name '__pycache__' -type d -exec rm -r {} +
	rm -rf .coverage htmlcov locale/*/LC_MESSAGES/*.mo
