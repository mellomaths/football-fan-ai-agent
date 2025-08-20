# ⚽ Football Fan AI Agent

An intelligent AI agent powered by DeepSeek API that helps football fans search for upcoming games, get team information, and chat about football. Features automated data synchronization and a flexible Docker-based deployment system.

## Todos

- [ ] Implement [NLTK](https://realpython.com/nltk-nlp-python/) for natural language processing.
- [ ] Implement Telegram bot integration for real-time updates.
- [ ] Add more football leagues and teams.
- [ ] Improve AI chat capabilities with more football-specific knowledge.

## 🚀 Features

- **AI-Powered Football Chat**: Intelligent conversations about football using DeepSeek API
- **Match Database**: Comprehensive database of football matches and competitions
- **Automated Scheduler**: Periodic data synchronization and calendar updates
- **Google Calendar Integration**: Add football matches to your calendar automatically
- **Docker Ready**: Containerized deployment with multiple entrypoints
- **OAuth Authentication**: Google Calendar integration using OAuth 2.0

## 📋 Prerequisites

- Python 3.13+
- Docker and Docker Compose
- Google Cloud account (for Google Calendar integration)
- Football-data.org API key (optional, for live data)

## 🚀 Quick Start with Docker

### 1. Clone and Setup
```bash
git clone <repository-url>
cd football-fan-ai-agent
cp env.template .env
# Edit .env with your API keys
```

### 2. Build and Run
```bash
# Build the Docker image
./docker-run.sh build

# Run the default service (shows help)
./docker-run.sh run

# Load database data
./docker-run.sh load-db

# Add team matches to calendar
./docker-run.sh add-calendar "Team Name"
```

### 3. Google Calendar Setup
Choose your preferred authentication method:

```bash
# Show setup guide
./docker-run.sh setup-calendar

# List available calendars
./docker-run.sh calendar-list

# Add team matches to Google Calendar
./docker-run.sh add-team-calendar "Flamengo"
```

## 🐳 Docker Usage

### Using the Shell Script
```bash
# Available commands
./docker-run.sh help

# Database operations
./docker-run.sh load-db

# Calendar operations
./docker-run.sh calendar-list
./docker-run.sh add-team-calendar "Team Name"

# Scheduler service
./docker-run.sh scheduler-bg
./docker-run.sh scheduler-logs
./docker-run.sh scheduler-stop

# Interactive shell
./docker-run.sh shell
```

### Using Make
```bash
# Build and run
make build
make run

# Calendar operations
make calendar-list
make add-team-calendar TEAM='Flamengo'

# Scheduler
make scheduler-bg
make scheduler-logs
```

### Using Docker Compose Directly
```bash
# Default service
docker-compose up football-fan-ai

# Commands profile
docker-compose --profile commands run --rm load-database
docker-compose --profile commands run --rm add-to-calendar "Team Name"

# Calendar profile
docker-compose --profile calendar run --rm calendar-list
docker-compose --profile calendar run --rm add-team-to-calendar

# Scheduler profile
docker-compose --profile scheduler up scheduler
```

## 🔐 Google Calendar Authentication

The project uses **OAuth 2.0 authentication** for Google Calendar integration.

See [GOOGLE_CALENDAR_AUTH.md](GOOGLE_CALENDAR_AUTH.md) for detailed setup instructions.

### Quick Authentication Setup
```env
# OAuth 2.0 Authentication (Required)
GOOGLE_CALENDAR_CREDENTIALS_PATH=credentials.json
GOOGLE_CALENDAR_TOKEN_PATH=token.json
```

## ⏰ Scheduler Service

The scheduler runs periodic jobs automatically:

```bash
# Start scheduler in background
./docker-run.sh scheduler-bg

# View scheduler logs
./docker-run.sh scheduler-logs

# Stop scheduler
./docker-run.sh scheduler-stop
```

**Scheduled Jobs:**
- Database loading: Every Monday at 10:30 AM
- Calendar updates: On-demand via commands

## 📱 Application Usage

### Available Commands
```bash
# Core operations
python main.py load-database
python main.py add-to-calendar "Team Name"

# Google Calendar operations
python main.py calendar-list
python main.py add-team-to-calendar "Team Name"
python main.py setup-calendar

# Help
python main.py --help
```

### Docker Commands
```bash
# All operations available via Docker
./docker-run.sh help
make help
```

## 🏗️ Project Structure

```
football-fan-ai-agent/
├── 📁 src/
│   ├── 📁 agents/           # AI and data agents
│   ├── 📁 cron/            # Scheduled jobs
│   ├── 📁 infrastructure/  # Core services
│   └── config.py           # Configuration
├── 📁 db/                  # Database files
├── 🐳 Dockerfile           # Container definition
├── 🐳 docker-compose.yml   # Multi-service orchestration
├── 🐳 docker-run.sh        # Convenience script
├── 🐳 Makefile             # Alternative interface
├── 📄 env.template         # Environment configuration
├── 📄 GOOGLE_CALENDAR_SETUP.md    # Calendar setup guide
├── 📄 GOOGLE_CALENDAR_AUTH.md     # Authentication methods
└── 📄 README.md            # This file
```

## ⚙️ Configuration

### Environment Variables
Copy `env.template` to `.env` and configure:

```bash
# Copy the template and edit with your API keys
cp env.template .env
# Edit .env with your actual API keys
```

**Required for Google Calendar:**
- Choose one authentication method from the template
- See [GOOGLE_CALENDAR_AUTH.md](GOOGLE_CALENDAR_AUTH.md) for details

**Supported Competitions:**
- Premier League
- La Liga
- Bundesliga
- Serie A
- Ligue 1
- And more (configurable in `src/config.py`)

## 🚨 Troubleshooting

### Common Issues

#### Docker Issues
```bash
# Check service status
./docker-run.sh status

# View logs
./docker-run.sh logs

# Clean up and restart
./docker-run.sh clean
./docker-run.sh build
```

#### Google Calendar Issues
```bash
# Check authentication
./docker-run.sh calendar-list

# View setup guide
./docker-run.sh setup-calendar

# Check environment variables
cat .env | grep GOOGLE_CALENDAR
```

#### Scheduler Issues
```bash
# Check scheduler status
./docker-run.sh scheduler-logs

# Restart scheduler
./docker-run.sh scheduler-stop
./docker-run.sh scheduler-bg
```

### Debug Commands
```bash
# Interactive debugging
./docker-run.sh shell

# Direct Docker access
docker-compose --profile commands run --rm shell

# Check all services
docker-compose ps
```

## 🛠️ Development

### Adding New Commands
1. Add command to `main.py` using Typer decorators
2. Add corresponding service to `docker-compose.yml`
3. Update `docker-run.sh` and `Makefile`
4. Test with Docker

### Adding New Scheduled Jobs
1. Create job function in `src/cron/jobs.py`
2. Add schedule in `scheduler.py`
3. Test with scheduler service

### Local Development
```bash
# Install dependencies
uv sync

# Run locally
python main.py --help

# Run with Docker
./docker-run.sh shell
```

## 📚 Documentation

- [Google Calendar Setup](GOOGLE_CALENDAR_SETUP.md) - Complete setup guide
- [Google Calendar Authentication](GOOGLE_CALENDAR_AUTH.md) - All auth methods
- [Docker Usage](docker-compose.yml) - Service definitions and examples

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test with Docker
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License.

## 🙏 Acknowledgments

- [DeepSeek](https://www.deepseek.com/) for AI capabilities
- [Football-data.org](https://www.football-data.org/) for match data
- [Google Calendar API](https://developers.google.com/calendar) for calendar integration
- [Docker](https://www.docker.com/) for containerization

---

⚽ **Happy Football Watching!** ⚽
