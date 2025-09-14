# Football Fan AI Agent Justfile
# Provides convenient commands for development, Docker operations, and Google Calendar integration

# Default target - show help
default:
    @just help

# Development & Linting Commands
lint-fix:
    @echo "Running linters with auto-fix..."
    @just lint-ruff-fix
    @just lint-black-fix
    @just lint-isort-fix
    @echo "All linters fixed successfully."

lint-ruff-fix:
    uv run ruff check --fix

lint-black-fix:
    uv run black . --exclude venv
    @echo "Black formatting applied."

lint-isort-fix:
    uv run isort .

lint: lint-ruff lint-flake8 lint-pylint lint-black
    @echo "All linters passed successfully."

lint-ruff:
    uv run ruff check

lint-flake8:
    uv run flake8

lint-pylint:
    uv run pylint .

lint-black:
    uv run black --check

# Docker Operations
build:
    @echo "Building Docker image..."
    docker compose build
    @echo "Build completed successfully!"

run:
    @echo "Running default service (help)..."
    docker compose up --build

# Management Commands
status:
    @echo "Status of all services:"
    @docker compose ps

logs:
    @echo "Showing logs for all services..."
    docker compose logs -f

stop:
    @echo "Stopping all containers..."
    docker compose down
    @echo "All containers stopped!"

