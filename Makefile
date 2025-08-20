# Football Fan AI Agent Makefile
# Provides simple commands for Docker operations

.PHONY: help build run load-db add-calendar shell hello scheduler scheduler-bg scheduler-stop scheduler-logs calendar-list add-team-calendar setup-calendar logs status stop clean all-commands

# Default target
help:
	@echo "Football Fan AI Agent - Available Commands:"
	@echo ""
	@echo "Build & Run:"
	@echo "  make build          - Build Docker image"
	@echo "  make run            - Run default service (help)"
	@echo "  make load-db        - Load database data"
	@echo "  make add-calendar   - Add team to calendar (set TEAM=name)"
	@echo "  make shell          - Open interactive shell"
	@echo "  make hello          - Run hello command"
	@echo ""
	@echo "Scheduler:"
	@echo "  make scheduler      - Start scheduler service (foreground)"
	@echo "  make scheduler-bg   - Start scheduler service (background)"
	@echo "  make scheduler-stop - Stop scheduler service"
	@echo "  make scheduler-logs - Show scheduler logs"
	@echo ""
	@echo "Google Calendar:"
	@echo "  make calendar-list  - List available Google Calendars"
	@echo "  make add-team-calendar - Add team matches to Google Calendar (set TEAM=name)"
	@echo "  make setup-calendar - Show Google Calendar setup guide"
	@echo ""
	@echo "Management:"
	@echo "  make logs           - Show container logs"
	@echo "  make status         - Show service status"
	@echo "  make stop           - Stop all containers"
	@echo "  make clean          - Remove containers and images"
	@echo "  make all-commands   - Run all command services"
	@echo ""
	@echo "Examples:"
	@echo "  make add-calendar TEAM='Manchester United'"
	@echo "  make shell"
	@echo "  make scheduler-bg"
	@echo "  make add-team-calendar TEAM='Flamengo'"

# Build the Docker image
build:
	docker-compose build

# Run default service (help)
run:
	docker-compose up football-fan-ai

# Load database
load-db:
	docker-compose --profile commands run --rm load-database

# Add team to calendar (requires TEAM variable)
add-calendar:
	@if [ -z "$(TEAM)" ]; then \
		echo "Error: TEAM variable is required"; \
		echo "Usage: make add-calendar TEAM='Team Name'"; \
		exit 1; \
	fi
	docker-compose --profile commands run --rm \
		-e TEAM_NAME="$(TEAM)" \
		add-to-calendar \
		python main.py add-to-calendar "$(TEAM)"

# Open interactive shell
shell:
	docker-compose --profile commands run --rm shell

# Run hello command
hello:
	docker-compose --profile commands run --rm hello

# Start scheduler (foreground)
scheduler:
	docker-compose --profile scheduler up scheduler

# Start scheduler (background)
scheduler-bg:
	docker-compose --profile scheduler up -d scheduler
	@echo "Scheduler started in background. Use 'make scheduler-logs' to view logs."

# Stop scheduler
scheduler-stop:
	docker-compose --profile scheduler stop scheduler
	@echo "Scheduler stopped!"

# Show scheduler logs
scheduler-logs:
	docker-compose --profile scheduler logs -f scheduler

# List Google Calendars
calendar-list:
	docker-compose --profile calendar run --rm calendar-list

# Add team to Google Calendar (requires TEAM variable)
add-team-calendar:
	@if [ -z "$(TEAM)" ]; then \
		echo "Error: TEAM variable is required"; \
		echo "Usage: make add-team-calendar TEAM='Team Name'"; \
		exit 1; \
	fi
	docker-compose --profile calendar run --rm \
		-e TEAM_NAME="$(TEAM)" \
		add-team-to-calendar \
		python main.py add-team-to-calendar "$(TEAM)"

# Show Google Calendar setup guide
setup-calendar:
	docker-compose --profile calendar run --rm setup-calendar

# Show logs
logs:
	docker-compose logs -f

# Show status
status:
	@echo "Default Profile Services:"
	@docker-compose ps --services --filter "profile=default"
	@echo ""
	@echo "Commands Profile Services:"
	@docker-compose ps --services --filter "profile=commands"
	@echo ""
	@echo "Scheduler Profile Services:"
	@docker-compose ps --services --filter "profile=scheduler"
	@echo ""
	@echo "Calendar Profile Services:"
	@docker-compose ps --services --filter "profile=calendar"
	@echo ""
	@echo "All Running Containers:"
	@docker-compose ps

# Stop all containers
stop:
	docker-compose down

# Clean up everything
clean:
	docker-compose down --rmi all --volumes --remove-orphans

# Run all command services
all-commands:
	docker-compose --profile commands up
