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
    @echo "All linters fixed successfully."

lint-ruff-fix:
    ruff check --fix

lint-black-fix:
    black . --exclude venv
    @echo "Black formatting applied."

lint-isort-fix:
    isort .

lint: lint-ruff lint-flake8 lint-pylint lint-black
    @echo "All linters passed successfully."

lint-ruff:
    ruff check

lint-flake8:
    flake8

lint-pylint:
    pylint .

lint-black:
    black --check

# Format code
format:
    @echo "Formatting code..."
    @just lint-black-fix
    @just lint-isort-fix
    @echo "Code formatting completed."

# Docker Operations
build:
    @echo "Building Docker image..."
    docker-compose build
    @echo "Build completed successfully!"

run:
    @echo "Running default service (help)..."
    docker-compose up football-fan-ai

shell:
    @echo "Opening interactive shell in container..."
    docker-compose --profile commands run --rm shell

load-db:
    @echo "Loading database data..."
    docker-compose --profile commands run --rm load-database

add-calendar TEAM:
    @echo "Adding team '{{TEAM}}' matches to calendar..."
    docker-compose --profile commands run --rm \
        -e TEAM_NAME="{{TEAM}}" \
        add-to-calendar \
        python main.py add-to-calendar "{{TEAM}}"

hello:
    @echo "Running hello command..."
    docker-compose --profile commands run --rm hello

# Google Calendar Commands
calendar-list:
    @echo "Listing available Google Calendars..."
    docker-compose --profile calendar run --rm calendar-list

add-team-calendar TEAM:
    @echo "Adding team '{{TEAM}}' matches to Google Calendar..."
    docker-compose --profile calendar run --rm \
        -e TEAM_NAME="{{TEAM}}" \
        add-team-to-calendar \
        python main.py add-team-to-calendar "{{TEAM}}"

setup-calendar:
    @echo "Showing Google Calendar setup guide..."
    docker-compose --profile calendar run --rm setup-calendar

# Scheduler Commands
scheduler:
    @echo "Starting scheduler service (foreground)..."
    docker-compose --profile scheduler up scheduler

scheduler-bg:
    @echo "Starting scheduler service in background..."
    docker-compose --profile scheduler up -d scheduler
    @echo "Scheduler started in background. Use 'just scheduler-logs' to view logs."

scheduler-stop:
    @echo "Stopping scheduler service..."
    docker-compose --profile scheduler stop scheduler
    @echo "Scheduler stopped!"

scheduler-logs:
    @echo "Showing scheduler logs..."
    docker-compose --profile scheduler logs -f scheduler

# Management Commands
status:
    @echo "Status of all services:"
    @echo ""
    @echo "Default Profile Services:"
    @docker-compose ps --services --filter "profile=default" || echo "No default services"
    @echo ""
    @echo "Commands Profile Services:"
    @docker-compose ps --services --filter "profile=commands" || echo "No command services"
    @echo ""
    @echo "Scheduler Profile Services:"
    @docker-compose ps --services --filter "profile=scheduler" || echo "No scheduler services"
    @echo ""
    @echo "Calendar Profile Services:"
    @docker-compose ps --services --filter "profile=calendar" || echo "No calendar services"
    @echo ""
    @echo "All Running Containers:"
    @docker-compose ps

logs:
    @echo "Showing logs for all services..."
    docker-compose logs -f

stop:
    @echo "Stopping all containers..."
    docker-compose down
    @echo "All containers stopped!"

clean:
    @echo "This will remove all containers and images. Are you sure? (y/N)"
    @read -p "Continue? " response
    @if [ "$$response" = "Y" ] || [ "$$response" = "y" ]; then \
        echo "Removing all containers and images..."; \
        docker-compose down --rmi all --volumes --remove-orphans; \
        echo "Cleanup completed!"; \
    else \
        echo "Cleanup cancelled."; \
    fi

# Force clean without confirmation
clean-force:
    @echo "Removing project containers and images..."
    docker rm football-fan-ai-agent
    docker-compose down --rmi all --volumes --remove-orphans
    @echo "Cleanup completed!"

# Utility Commands
test-docker:
    @echo "Testing Docker setup..."
    docker-compose config
    @echo "Docker Compose configuration is valid."

db-shell:
    @echo "Opening database shell..."
    docker-compose --profile commands run --rm shell

# Development Commands
dev-install:
    @echo "Installing development dependencies..."
    uv sync --dev

dev-run:
    @echo "Running application locally..."
    python main.py --help

dev-test:
    @echo "Running tests..."
    python -m pytest

# Quick Commands
quick-start:
    @echo "Quick start sequence..."
    @just build
    @just run

quick-calendar TEAM:
    @echo "Quick calendar setup for team '{{TEAM}}'..."
    @just calendar-list
    @just add-team-calendar TEAM="{{TEAM}}"

# Help Commands
help:
    @echo "Football Fan AI Agent - Available Commands:"
    @echo ""
    @echo "Development & Linting:"
    @echo "  just lint              - Run all linters"
    @echo "  just lint-fix          - Fix linting issues automatically"
    @echo "  just format            - Format code with black and isort"
    @echo ""
    @echo "Docker Operations:"
    @echo "  just build             - Build Docker image"
    @echo "  just run               - Run default service (help)"
    @echo "  just shell             - Open interactive shell in container"
    @echo "  just load-db           - Load database data"
    @echo "  just add-calendar      - Add team to calendar (set TEAM=name)"
    @echo ""
    @echo "Google Calendar:"
    @echo "  just calendar-list     - List available Google Calendars"
    @echo "  just add-team-calendar - Add team matches to Google Calendar (set TEAM=name)"
    @echo "  just setup-calendar    - Show Google Calendar setup guide"
    @echo ""
    @echo "Scheduler:"
    @echo "  just scheduler         - Start scheduler service (foreground)"
    @echo "  just scheduler-bg      - Start scheduler service (background)"
    @echo "  just scheduler-logs    - Show scheduler logs"
    @echo "  just scheduler-stop    - Stop scheduler service"
    @echo ""
    @echo "Management:"
    @echo "  just status            - Show service status"
    @echo "  just logs              - Show container logs"
    @echo "  just stop              - Stop all containers"
    @echo "  just clean             - Remove project containers and images (with confirmation)"
    @echo "  just clean-force       - Remove project containers and images (no confirmation)"
    @echo ""
    @echo "Examples:"
    @echo "  just add-calendar TEAM='Manchester United'"
    @echo "  just add-team-calendar TEAM='Flamengo'"
    @echo "  just scheduler-bg"

docker-help:
    @echo "Docker Compose Profiles:"
    @echo "  default:    Main service (help command)"
    @echo "  commands:   All command services (load-db, add-calendar, shell, hello)"
    @echo "  scheduler:  Scheduler service for periodic jobs"
    @echo "  calendar:   Google Calendar integration services"
    @echo ""
    @echo "Available Services:"
    @docker-compose config --services

calendar-help:
    @echo "Google Calendar Authentication Methods:"
    @echo "  1. OAuth 2.0 - Interactive browser authentication"
    @echo "  2. Service Account - Automated, no browser interaction"
    @echo "  3. Application Default Credentials - Uses gcloud CLI"
    @echo "  4. API Key - Simple read-only access"
    @echo ""
    @echo "See GOOGLE_CALENDAR_AUTH.md for detailed setup instructions."

# List all available recipes
list:
    @just --list
