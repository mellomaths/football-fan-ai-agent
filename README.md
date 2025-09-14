# Football Fan AI Agent

A FastAPI-based web service that provides football match information by scraping data from ESPN. The application is designed to fetch upcoming matches for specific teams and expose them through a REST API.

## 🏗️ Architecture

The application follows a clean architecture pattern with the following structure:

```
src/
├── main.py                 # FastAPI application entry point
├── api.py                  # API router configuration
├── controllers/            # API controllers
│   └── matches_controller.py
├── models/                 # Pydantic data models
│   ├── matches_response.py
│   └── up_response.py
├── infrastructure/         # Infrastructure components
│   ├── logger.py
│   └── settings.py
└── scrappers/             # Data scraping modules
    └── espn/
        ├── espn_config.py
        ├── espn_scrapper.py
        ├── espn_scrapper_api.py
        └── espn_scrapper_html.py
```

## 🚀 Features

- **REST API**: FastAPI-based web service with automatic OpenAPI documentation
- **Match Scraping**: Fetches football match data from ESPN using both API and HTML scraping
- **Multi-Team Support**: Supports 20 Brazilian football teams with enum-based validation
- **Dual Scraping Strategy**: Uses ESPN API as primary method with HTML scraping as fallback
- **Docker Support**: Containerized application with Docker Compose
- **Health Checks**: Built-in health monitoring endpoints
- **CORS Support**: Configurable Cross-Origin Resource Sharing
- **Structured Logging**: Comprehensive logging with file rotation
- **Development Tools**: Justfile with convenient commands for linting, Docker operations, and development

## 🛠️ Technology Stack

- **Framework**: FastAPI
- **Python Version**: 3.12+
- **Web Server**: Uvicorn
- **Data Validation**: Pydantic
- **Web Scraping**: Requests + BeautifulSoup4
- **Containerization**: Docker + Docker Compose
- **Package Management**: UV
- **Database**: PostgreSQL (configured but not actively used)

## 📋 Prerequisites

- Python 3.12+
- Docker & Docker Compose (for containerized deployment)
- UV package manager
- Just (optional, for development commands)

## 🚀 Quick Start

### Using Docker (Recommended)

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd football-fan-ai-agent
   ```

2. **Run with Docker Compose**
   ```bash
   # Using Docker Compose directly
   docker-compose up --build
   
   # Or using Justfile commands
   just run
   ```

3. **Access the API**
   - API Base URL: `http://localhost:3002/football-fan`
   - Health Check: `http://localhost:3002/football-fan/up`
   - API Documentation: `http://localhost:3002/football-fan/docs`

### Local Development

1. **Install dependencies**
   ```bash
   uv sync
   ```

2. **Run the application**
   ```bash
   uv run fastapi run src/main.py --port 3000 --host 0.0.0.0
   ```

3. **Access the API**
   - API Base URL: `http://localhost:3000/football-fan`
   - Health Check: `http://localhost:3000/football-fan/up`
   - API Documentation: `http://localhost:3000/football-fan/docs`

## 📚 API Endpoints

### Health Check
```http
GET /football-fan/up
```
Returns the application status.

**Response:**
```json
{
  "status": "ok"
}
```

### Get Upcoming Matches
```http
GET /football-fan/api/v1/matches/{team_name}/upcoming
```

Fetches upcoming matches for a specific team.

**Parameters:**
- `team_name` (enum): Name of the team (supports 20 Brazilian teams including FLAMENGO, PALMEIRAS, CORINTHIANS, etc.)

**Response:**
```json
[
  {
    "date": "2025-01-15T20:00:00Z",
    "date_detail": "8:00 PM",
    "completed": false,
    "competition": "Campeonato Brasileiro Série A",
    "home_team": {
      "abbrev": "FLA",
      "display_name": "Flamengo",
      "link": "https://www.espn.com/soccer/team/_/id/819/flamengo",
      "logo": "https://a.espncdn.com/combiner/i?img=/i/teamlogos/soccer/500/819.png"
    },
    "away_team": {
      "abbrev": "BOT",
      "display_name": "Botafogo",
      "link": "https://www.espn.com/soccer/team/_/id/819/botafogo",
      "logo": "https://a.espncdn.com/combiner/i?img=/i/teamlogos/soccer/500/819.png"
    },
    "stadium": "Maracanã Stadium",
    "link": "https://www.espn.com/soccer/match/_/id/123456"
  }
]
```

## 🔧 Configuration

The application uses Pydantic Settings for configuration management. Key settings include:

### Application Settings
- **Name**: football-fan
- **Version**: 0.0.1
- **Root Path**: /football-fan

### API Settings
- **Version**: v1
- **Path**: /api/v1

### Server Settings
- **HTTP Port**: 3000 (3002 in Docker)

### CORS Settings
- **Allow Origins**: * (all origins)
- **Allow Credentials**: true
- **Allow Methods**: GET, POST, PUT, DELETE, OPTIONS

### Logger Settings
- **Level**: TRACE
- **File**: app.log
- **Max Bytes**: 1MB
- **Backup Count**: 5

## 🏗️ Scraping Strategy

The application uses a dual scraping approach with **HTML scraping as the primary method**:

### 1. HTML Scraping (Primary)
- **Endpoint**: `https://www.espn.com/soccer/team/fixtures/_/id/{team_id}/{team_name}`
- **Method**: Web scraping with BeautifulSoup + JSON extraction
- **Advantages**: More comprehensive data, includes team logos and links
- **Implementation**: `EspnScrapperHTML`

### 2. ESPN API (Fallback)
- **Endpoint**: `https://site.api.espn.com/apis/site/v2/sports/soccer/bra.1/teams/{team_id}/schedule`
- **Method**: Direct API calls
- **Advantages**: Fast, reliable, structured data
- **Implementation**: `EspnScrapperApi`

### Team Configuration
- **Dynamic URLs**: Team-specific URLs generated using team IDs from `EspnConfig`
- **Team IDs**: 20 Brazilian teams with unique ESPN team identifiers
- **Flexible Support**: Easy to add new teams by updating the configuration

## 🐳 Docker Configuration

### Dockerfile
- **Base Image**: Python 3.12-slim
- **Package Manager**: UV
- **Port**: 3000
- **Workers**: 4

### Docker Compose
- **Service Name**: football-fan-api
- **External Port**: 3002
- **Health Check**: HTTP GET /up
- **Environment**: production

## 📊 Monitoring

### Health Checks
The application includes built-in health monitoring:
- **Endpoint**: `/up`
- **Method**: GET
- **Response**: JSON with status
- **Docker Health Check**: Configured in docker-compose.yaml

### Logging
- **File**: app.log
- **Level**: TRACE
- **Rotation**: 1MB files, 5 backups
- **Format**: Structured with timestamps and process info

## 🔍 Development

### Development Commands (Justfile)
The project includes a `Justfile` with convenient development commands:

```bash
# Show all available commands
just help

# Run all linters with auto-fix
just lint-fix

# Run individual linters
just lint-ruff-fix
just lint-black-fix
just lint-isort-fix

# Run all linters (check only)
just lint

# Docker operations
just build          # Build Docker image
just run            # Run with Docker Compose
just status         # Check container status
just logs           # Show container logs
just stop           # Stop all containers
```

### Code Quality Tools
- **Black**: Code formatting
- **Flake8**: Linting
- **Pylint**: Advanced linting
- **Ruff**: Fast linting
- **isort**: Import sorting

### Manual Commands
```bash
# Format code
uv run black src/

# Lint code
uv run flake8 src/

# Type checking
uv run pylint src/
```

## 🌐 Supported Teams

The application now supports **20 Brazilian football teams** from Serie A and other competitions:

### Serie A Teams
- **Flamengo** (Team ID: 819)
- **Palmeiras** (Team ID: 2029)
- **Cruzeiro** (Team ID: 2022)
- **Bahia** (Team ID: 9967)
- **Botafogo** (Team ID: 6086)
- **São Paulo** (Team ID: 2026)
- **Bragantino** (Team ID: 6079)
- **Corinthians** (Team ID: 874)
- **Fluminense** (Team ID: 3445)
- **Internacional** (Team ID: 1936)
- **Ceará** (Team ID: 9969)
- **Grêmio** (Team ID: 6273)
- **Atlético-MG** (Team ID: 7632)
- **Vasco** (Team ID: 3454)
- **Santos** (Team ID: 2674)
- **Vitória** (Team ID: 3457)
- **Juventude** (Team ID: 6270)
- **Fortaleza** (Team ID: 6272)
- **Sport** (Team ID: 7631)
- **Mirassol** (Team ID: 9169)

### Team Validation
The API now uses **enum-based team validation** through the `Team` enum in `src/models/matches_request.py`, ensuring only valid team names are accepted.

**Example API calls:**
```bash
# Valid team names
GET /football-fan/api/v1/matches/FLAMENGO/upcoming
GET /football-fan/api/v1/matches/PALMEIRAS/upcoming
GET /football-fan/api/v1/matches/CORINTHIANS/upcoming

# Invalid team names will return validation errors
GET /football-fan/api/v1/matches/INVALID_TEAM/upcoming
```

## 🔧 Environment Variables

The application supports the following environment variables:

```bash
# Environment
PY_ENV=production

# Database
POSTGRES__HOST=localhost
POSTGRES__PORT=5432
POSTGRES__DATABASE_NAME=postgres
POSTGRES__USERNAME=postgres
POSTGRES__PASSWORD=postgres

# CORS
CORS__ALLOW_ORIGINS=["*"]
CORS__ALLOW_CREDENTIALS=true
```

## 📝 License

This project is part of the Football Fan AI Agent system.

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Run tests and linting
5. Submit a pull request

## 📞 Support

For issues and questions, please create an issue in the repository.