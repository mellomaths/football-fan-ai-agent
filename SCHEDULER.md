# 🕐 Football Fan AI Agent Scheduler

The scheduler service runs periodic jobs to keep your football data up-to-date automatically.

## 🚀 Quick Start

### Start the Scheduler

```bash
# Start in foreground (see logs directly)
./docker-run.sh scheduler

# Start in background
./docker-run.sh scheduler-bg

# Using make
make scheduler
make scheduler-bg
```

### Stop the Scheduler

```bash
# Stop the scheduler
./docker-run.sh scheduler-stop

# Using make
make scheduler-stop
```

### View Scheduler Logs

```bash
# View scheduler logs
./docker-run.sh scheduler-logs

# Using make
make scheduler-logs
```

## 📋 What the Scheduler Does

The scheduler automatically runs the following jobs:

### 🔄 Database Loading Job
- **Schedule**: Every Monday at 10:30 AM
- **Purpose**: Loads fresh football data from the Football Data API
- **What it loads**:
  - Competition information
  - Match data for configured competitions
  - Updates the local database

### 📅 Current Schedule
```python
# From scheduler.py
schedule.every().monday.at("10:30").do(load_database)
```

## ⚙️ Configuration

### Environment Variables

Create a `.env` file based on `env.template`:

```bash
# Copy the template
cp env.template .env

# Edit with your API keys
nano .env
```

**Required Variables:**
- `FOOTBALL_DATA_API_KEY`: Your Football Data API key
- `FOOTBALL_DATA_API_BASE_URL`: API base URL (default: https://api.football-data.org/v4)

**Optional Variables:**
- `DEEPSEEK_API_KEY`: For AI chat features
- `LOG_LEVEL`: Logging level (default: INFO)

### API Keys

1. **Football Data API**: Get a free key from [football-data.org](https://www.football-data.org/)
2. **DeepSeek API**: Get your key from [DeepSeek Platform](https://platform.deepseek.com/)

## 🐳 Docker Commands

### Direct Docker Compose

```bash
# Start scheduler
docker-compose --profile scheduler up scheduler

# Start in background
docker-compose --profile scheduler up -d scheduler

# Stop scheduler
docker-compose --profile scheduler stop scheduler

# View logs
docker-compose --profile scheduler logs -f scheduler

# Check status
docker-compose --profile scheduler ps
```

### All Services

```bash
# Start all services including scheduler
docker-compose --profile commands --profile scheduler up

# Start only scheduler and default service
docker-compose --profile default --profile scheduler up
```

## 🔧 Customization

### Modify Schedule

Edit `scheduler.py` to change when jobs run:

```python
# Example: Run every day at 9 AM
schedule.every().day.at("09:00").do(load_database)

# Example: Run every hour
schedule.every().hour.do(load_database)

# Example: Run every 30 minutes
schedule.every(30).minutes.do(load_database)
```

### Add New Jobs

Add new scheduled functions to `scheduler.py`:

```python
def my_new_job():
    """My custom job function."""
    print("Running my custom job!")

# Schedule it
schedule.every().wednesday.at("14:00").do(my_new_job)
```

## 📊 Monitoring

### Check Scheduler Status

```bash
# View all services
./docker-run.sh status

# Using make
make status
```

### View Logs

```bash
# Scheduler logs only
./docker-run.sh scheduler-logs

# All service logs
./docker-run.sh logs
```

## 🚨 Troubleshooting

### Scheduler Won't Start

1. **Check environment variables**:
   ```bash
   docker-compose --profile scheduler config
   ```

2. **Check logs**:
   ```bash
   ./docker-run.sh scheduler-logs
   ```

3. **Verify API keys**:
   - Ensure `.env` file exists
   - Check API keys are valid
   - Verify API endpoints are accessible

### Scheduler Crashes

1. **Check restart policy**: The scheduler has `restart: unless-stopped`
2. **View crash logs**: `./docker-run.sh scheduler-logs`
3. **Check resource usage**: `docker stats`

### Jobs Not Running

1. **Verify schedule**: Check `scheduler.py` for correct timing
2. **Check timezone**: Container uses UTC by default
3. **Verify job functions**: Ensure functions exist and are importable

## 🔄 Restart and Recovery

### Automatic Restart

The scheduler automatically restarts if it crashes due to:
- API failures
- Network issues
- Python exceptions

### Manual Restart

```bash
# Restart scheduler
./docker-run.sh scheduler-stop
./docker-run.sh scheduler-bg

# Using make
make scheduler-stop
make scheduler-bg
```

## 📝 Log Files

Scheduler logs are output to:
- **Console**: When running in foreground
- **Docker logs**: When running in background
- **Container stdout/stderr**: For Docker logging systems

### Log Levels

- **INFO**: General operation information
- **DEBUG**: Detailed debugging information (set `LOG_LEVEL=DEBUG`)
- **ERROR**: Error messages and exceptions

## 🎯 Best Practices

1. **Run in background** for production: `./docker-run.sh scheduler-bg`
2. **Monitor logs** regularly: `./docker-run.sh scheduler-logs`
3. **Set up alerts** for job failures
4. **Backup database** before major schedule changes
5. **Test schedule changes** in development first

## 🔗 Related Files

- `scheduler.py` - Main scheduler logic
- `src/cron/jobs.py` - Job functions
- `docker-compose.yml` - Scheduler service configuration
- `docker-run.sh` - Scheduler management commands
- `Makefile` - Alternative scheduler interface
