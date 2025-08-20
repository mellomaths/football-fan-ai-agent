#!/bin/bash

# Football Fan AI Agent Docker Runner Script

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to print colored output
print_info() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

print_header() {
    echo -e "${BLUE}[HEADER]${NC} $1"
}

# Function to show help
show_help() {
    echo "Football Fan AI Agent Docker Runner"
    echo ""
    echo "Usage: $0 [COMMAND] [OPTIONS]"
    echo ""
    echo "Commands:"
    echo "  build           Build the Docker image"
    echo "  run             Run the default service (help)"
    echo "  load-db         Load database data"
    echo "  add-calendar    Add team matches to calendar (requires team name)"
    echo "  shell           Open a shell in the container"
    echo "  hello           Run hello command"
    echo "  scheduler       Start the scheduler service"
    echo "  scheduler-bg    Start the scheduler service in background"
    echo "  scheduler-stop  Stop the scheduler service"
    echo "  scheduler-logs  Show scheduler logs"
    echo "  logs            Show container logs"
    echo "  status          Show status of all services"
    echo "  stop            Stop all containers"
    echo "  clean           Remove all containers and images"
    echo "  help            Show this help message"
    echo ""
    echo "Google Calendar Commands:"
    echo "  calendar-list   List available Google Calendars"
    echo "  add-team-calendar Add team matches to Google Calendar"
    echo "  setup-calendar  Show Google Calendar setup guide"
    echo ""
    echo "Examples:"
    echo "  $0 build"
    echo "  $0 load-db"
    echo "  $0 add-calendar 'Manchester United'"
    echo "  $0 shell"
    echo "  $0 scheduler"
    echo "  $0 calendar-list"
    echo "  $0 add-team-calendar 'Flamengo'"
    echo ""
    echo "Docker Compose Profiles:"
    echo "  default:        Main service (help command)"
    echo "  commands:       All command services (load-db, add-calendar, shell, hello)"
    echo "  scheduler:      Scheduler service for running periodic jobs"
    echo "  calendar:       Google Calendar integration services"
}

# Function to build the image
build_image() {
    print_info "Building Docker image..."
    docker-compose build
    print_info "Build completed successfully!"
}

# Function to run the default service
run_default() {
    print_info "Running default service (help)..."
    docker-compose up football-fan-ai
}

# Function to load database
load_database() {
    print_info "Loading database..."
    docker-compose --profile commands run --rm load-database
}

# Function to add team to calendar
add_to_calendar() {
    if [ -z "$1" ]; then
        print_error "Team name is required!"
        echo "Usage: $0 add-calendar 'Team Name'"
        exit 1
    fi
    
    print_info "Adding team '$1' matches to calendar..."
    # Create a temporary service override for the specific team
    docker-compose --profile commands run --rm \
        -e TEAM_NAME="$1" \
        add-to-calendar \
        python main.py add-to-calendar "$1"
}

# Function to open shell
open_shell() {
    print_info "Opening shell in container..."
    docker-compose --profile commands run --rm shell
}

# Function to run hello command
run_hello() {
    print_info "Running hello command..."
    docker-compose --profile commands run --rm hello
}

# Function to start scheduler
start_scheduler() {
    print_info "Starting scheduler service..."
    docker-compose --profile scheduler up scheduler
}

# Function to start scheduler in background
start_scheduler_background() {
    print_info "Starting scheduler service in background..."
    docker-compose --profile scheduler up -d scheduler
    print_info "Scheduler started in background. Use '$0 scheduler-logs' to view logs."
}

# Function to stop scheduler
stop_scheduler() {
    print_info "Stopping scheduler service..."
    docker-compose --profile scheduler stop scheduler
    print_info "Scheduler stopped!"
}

# Function to show scheduler logs
show_scheduler_logs() {
    print_info "Showing scheduler logs..."
    docker-compose --profile scheduler logs -f scheduler
}

# Function to list Google Calendars
list_calendars() {
    print_info "Listing available Google Calendars..."
    docker-compose --profile calendar run --rm calendar-list
}

# Function to add team to Google Calendar
add_team_to_google_calendar() {
    if [ -z "$1" ]; then
        print_error "Team name is required!"
        echo "Usage: $0 add-team-calendar 'Team Name'"
        exit 1
    fi
    
    print_info "Adding team '$1' matches to Google Calendar..."
    docker-compose --profile calendar run --rm \
        -e TEAM_NAME="$1" \
        add-team-to-calendar \
        python main.py add-team-to-calendar "$1"
}

# Function to show calendar setup guide
show_calendar_setup() {
    print_info "Showing Google Calendar setup guide..."
    docker-compose --profile calendar run --rm setup-calendar
}

# Function to show logs
show_logs() {
    print_info "Showing logs for all services..."
    docker-compose logs -f
}

# Function to show status
show_status() {
    print_info "Status of all services:"
    echo ""
    print_header "Default Profile Services:"
    docker-compose ps --services --filter "profile=default"
    echo ""
    print_header "Commands Profile Services:"
    docker-compose ps --services --filter "profile=commands"
    echo ""
    print_header "Scheduler Profile Services:"
    docker-compose ps --services --filter "profile=scheduler"
    echo ""
    print_header "Calendar Profile Services:"
    docker-compose ps --services --filter "profile=calendar"
    echo ""
    print_header "All Running Containers:"
    docker-compose ps
}

# Function to stop containers
stop_containers() {
    print_info "Stopping all containers..."
    docker-compose down
    print_info "All containers stopped!"
}

# Function to clean up
clean_up() {
    print_warning "This will remove all containers and images. Are you sure? (y/N)"
    read -r response
    if [[ "$response" =~ ^([yY][eE][sS]|[yY])$ ]]; then
        print_info "Removing all containers and images..."
        docker-compose down --rmi all --volumes --remove-orphans
        print_info "Cleanup completed!"
    else
        print_info "Cleanup cancelled."
    fi
}

# Function to run all command services
run_all_commands() {
    print_info "Running all command services..."
    docker-compose --profile commands up
}

# Main script logic
case "${1:-help}" in
    "build")
        build_image
        ;;
    "run")
        run_default
        ;;
    "load-db")
        load_database
        ;;
    "add-calendar")
        add_to_calendar "$2"
        ;;
    "shell")
        open_shell
        ;;
    "hello")
        run_hello
        ;;
    "scheduler")
        start_scheduler
        ;;
    "scheduler-bg")
        start_scheduler_background
        ;;
    "scheduler-stop")
        stop_scheduler
        ;;
    "scheduler-logs")
        show_scheduler_logs
        ;;
    "calendar-list")
        list_calendars
        ;;
    "add-team-calendar")
        add_team_to_google_calendar "$2"
        ;;
    "setup-calendar")
        show_calendar_setup
        ;;
    "logs")
        show_logs
        ;;
    "status")
        show_status
        ;;
    "stop")
        stop_containers
        ;;
    "clean")
        clean_up
        ;;
    "all-commands")
        run_all_commands
        ;;
    "help"|*)
        show_help
        ;;
esac
