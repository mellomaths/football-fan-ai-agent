# ⚽ Football Fan AI Agent

An intelligent AI agent powered by DeepSeek API that helps football fans search for upcoming games, get team information, and chat about football. Features automated data synchronization and a flexible Docker-based deployment system.

## Todos

- [ ] Implement [NLTK](https://realpython.com/nltk-nlp-python/) for natural language processing.
- [ ] Implement Telegram bot integration for real-time updates.
- [ ] Add more football leagues and teams.
- [ ] Improve AI chat capabilities with more football-specific knowledge.

## 🚀 Features

- **🔍 Game Search**: Find upcoming football matches across major leagues
- **🏆 Team-specific Search**: Get upcoming games for your favorite team
- **🌍 League Search**: Find games in specific competitions
- **ℹ️ Team Information**: Get detailed team stats and details
- **💬 AI Chat**: Chat with an AI expert about football using DeepSeek
- **📅 Real-time Data**: Integration with football-data.org API
- **🕐 Automated Scheduler**: Periodic data updates and maintenance
- **🐳 Docker Ready**: Full containerization with multi-service support

## 🛠️ Installation

### Prerequisites

- **Docker** and **Docker Compose** installed
- **Python 3.13+** (for local development)
- **DeepSeek API key**
- **Football-data.org API key** for real match data

### Quick Start with Docker

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd football-fan-ai-agent
   ```

2. **Set up environment variables**
   ```bash
   # Copy the template and edit with your API keys
   cp .env.template .env
   # Edit .env with your actual API keys
   ```

3. **Build and run**
   ```bash
   # Build the Docker image
   ./docker-run.sh build
   
   # Run the application
   ./docker-run.sh run
   ```

### Local Development Setup

1. **Install dependencies using uv**
   ```bash
   uv sync
   ```

2. **Set up environment variables**
   Create a `.env` file in the project root:
   ```env
   DEEPSEEK_API_KEY=your_deepseek_api_key_here
   FOOTBALL_DATA_API_KEY=your_football_data_api_key_here
   FOOTBALL_DATA_API_BASE_URL=https://api.football-data.org/v4
   ```

3. **Get API Keys**
   - **DeepSeek API**: Sign up at [DeepSeek](https://platform.deepseek.com/)
   - **Football Data API**: Get a free API key from [football-data.org](https://www.football-data.org/)

## 🐳 Docker Usage

### Available Commands

```bash
# Build the image
./docker-run.sh build

# Run default service (help)
./docker-run.sh run

# Load database
./docker-run.sh load-db

# Add team to calendar
./docker-run.sh add-calendar "Manchester United"

# Interactive shell
./docker-run.sh shell

# Scheduler management
./docker-run.sh scheduler-bg      # Start scheduler in background
./docker-run.sh scheduler-stop    # Stop scheduler
./docker-run.sh scheduler-logs    # View scheduler logs

# Management
./docker-run.sh status            # Show service status
./docker-run.sh logs              # View all logs
./docker-run.sh stop              # Stop all containers
./docker-run.sh clean             # Clean up everything
```

### Alternative: Using Make

```bash
# Show all available commands
make help

# Build and run
make build
make run

# Scheduler operations
make scheduler-bg
make scheduler-logs
make scheduler-stop
```

### Docker Compose Profiles

- **`default`**: Main service (help command)
- **`commands`**: All command services (load-db, add-calendar, shell, hello)
- **`scheduler`**: Scheduler service for periodic jobs

```bash
# Run specific profiles
docker-compose --profile default up
docker-compose --profile commands up
docker-compose --profile scheduler up -d scheduler
```

## 🕐 Scheduler Service

The scheduler automatically runs periodic jobs to keep your football data up-to-date:

- **Database Loading**: Every Monday at 10:30 AM
- **Data Synchronization**: Automatic updates from football-data.org
- **Persistent Storage**: Data stored in mounted `db/` directory

### Scheduler Commands

```bash
# Start scheduler
./docker-run.sh scheduler-bg

# Monitor logs
./docker-run.sh scheduler-logs

# Stop scheduler
./docker-run.sh scheduler-stop
```

## 🎯 Application Usage

### Run the Application

```bash
# Using Docker
./docker-run.sh run

# Local development
python main.py --help
```

### Available Commands

```bash
# Load database
python main.py load-database

# Add team to calendar
python main.py add-to-calendar "Team Name"

# Hello command
python main.py hello "Your Name"
```

### Example Output

```txt
$ python main.py --help

Usage: main.py [OPTIONS] COMMAND [ARGS]...

╭─ Commands ──────────────────────────────────────────────────────────╮
│ load-database     Load data for a specific entity.                  │
│ add-to-calendar   Add matches for a specific team to the calendar.  │
│ hello             Say hello to NAME.                                │
╰─────────────────────────────────────────────────────────────────────╯
```

## 🏗️ Project Structure

```
football-fan-ai-agent/
├── db/                           # Database JSON files (mounted in Docker)
├── src/
│   ├── agents/                   # AI Agents (DeepSeek, FootballData, Gemini)
│   ├── cron/                     # Periodic job functions
│   ├── infrastructure/           # Database and logging utilities
│   └── config.py                 # Configuration constants
├── main.py                       # Main application entry point
├── scheduler.py                  # Scheduler for periodic tasks
├── Dockerfile                    # Docker image definition
├── docker-compose.yml            # Multi-service Docker configuration
├── docker-run.sh                 # Docker management script
├── Makefile                      # Alternative Docker interface
├── pyproject.toml                # Project dependencies and configuration
├── env.template                  # Environment variables template
└── README.md                     # This file
```

## ⚙️ Configuration

### Environment Variables

Create a `.env` file based on `env.template`:

```env
# Required for scheduler and data loading
FOOTBALL_DATA_API_KEY=your_football_data_api_key_here
FOOTBALL_DATA_API_BASE_URL=https://api.football-data.org/v4

# Optional: AI features
DEEPSEEK_API_KEY=your_deepseek_api_key_here

# Optional: Logging
LOG_LEVEL=INFO
```

### Supported Competitions

Currently configured for Brazilian football:
- Campeonato Brasileiro
- Libertadores
- Copa do Brasil

## 📊 Data Sources

- **Football-data.org**: Real match data, team information, and schedules
- **Local Database**: JSON-based file system database for persistence
- **Automated Updates**: Scheduled data synchronization via scheduler

## 🚨 Troubleshooting

### Docker Issues

1. **Container won't start**
   ```bash
   # Check logs
   ./docker-run.sh logs
   
   # Validate configuration
   ./test-docker.sh
   ```

2. **Scheduler not working**
   ```bash
   # Check scheduler status
   ./docker-run.sh status
   
   # View scheduler logs
   ./docker-run.sh scheduler-logs
   ```

3. **Environment variables not loading**
   - Ensure `.env` file exists in project root
   - Check variable names match `env.template`
   - Restart containers after changes

### Common Issues

1. **API Key Errors**
   - Verify API keys in `.env` file
   - Check API key validity and limits
   - Ensure correct environment variable names

2. **Database Issues**
   - Check `db/` directory permissions
   - Verify volume mounts in Docker
   - Run `./docker-run.sh load-db` to refresh data

3. **Scheduler Problems**
   - Check if scheduler container is running
   - Verify timezone settings (container uses UTC)
   - Check logs for specific error messages

## 🔧 Development

### Adding New Commands

1. **Add to main.py**
   ```python
   @app.command()
   def new_command():
       """Description of new command."""
       # Implementation here
   ```

2. **Add to Docker services**
   - Update `docker-compose.yml`
   - Add to `docker-run.sh`
   - Update `Makefile`

### Adding New Scheduled Jobs

1. **Create job function in `src/cron/jobs.py`**
2. **Schedule in `scheduler.py`**
3. **Restart scheduler service**

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test with Docker: `./test-docker.sh`
5. Submit a Pull Request

## 📝 License

This project is open source and available under the [MIT License](LICENSE).

## 🙏 Acknowledgments

- [DeepSeek](https://platform.deepseek.com/) for AI capabilities
- [Football-data.org](https://www.football-data.org/) for football data APIs
- Docker community for containerization tools

---

⚽ **Happy Football Watching!** ⚽
