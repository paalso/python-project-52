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

# ========================
# Development Tools
# ========================

shell:  ## Launch Django shell_plus with IPython
	@$(MANAGE) shell_plus --ipython

test:  ## Run tests using pytest
	@$(MANAGE) test

makemessages:  ## Extract translations for ru and ua
	uv run sh -c 'django-admin makemessages -l ru && django-admin makemessages -l ua'

compilemessages:  ## Compile translation files (.po -> .mo)
	uv run django-admin compilemessages

lint:  ## Check code style using ruff
	@uv run ruff check task_manager

lint-fix:  ## Auto-fix linting issues using ruff
	@uv run ruff check --fix task_manager

djlint:  ## Check and reformat Django templates using djlint
	@uv run djlint task_manager/**/templates/ --reformat --indent=2

check:  ## Run lint and tests
	@$(MAKE) lint
	@$(MAKE) test
	@$(MAKE) djlint
