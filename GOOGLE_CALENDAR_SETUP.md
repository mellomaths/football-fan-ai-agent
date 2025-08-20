# 📅 Google Calendar Integration Setup

This guide will help you set up Google Calendar integration for the Football Fan AI Agent, allowing you to automatically add football matches to your Google Calendar.

## 🚀 Quick Start

1. **Setup Google Cloud Project** (5 minutes)
2. **Download Credentials** (2 minutes)
3. **Test Integration** (3 minutes)

## 📋 Prerequisites

- Google account
- Access to Google Cloud Console
- Docker and Docker Compose installed
- Football Fan AI Agent project set up

## 🔧 Step-by-Step Setup

### Step 1: Create Google Cloud Project

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Click "Select a project" → "New Project"
3. Enter a project name (e.g., "Football Fan AI Agent")
4. Click "Create"

### Step 2: Enable Google Calendar API

1. In your project, go to "APIs & Services" → "Library"
2. Search for "Google Calendar API"
3. Click on "Google Calendar API"
4. Click "Enable"

### Step 3: Create OAuth 2.0 Credentials

1. Go to "APIs & Services" → "Credentials"
2. Click "Create Credentials" → "OAuth 2.0 Client IDs"
3. If prompted, configure the OAuth consent screen:
   - User Type: External
   - App name: "Football Fan AI Agent"
   - User support email: Your email
   - Developer contact information: Your email
4. Click "Save and Continue" through the remaining steps
5. Back to credentials, click "Create Credentials" → "OAuth 2.0 Client IDs"
6. Application type: "Desktop application"
7. Name: "Football Fan AI Agent Desktop"
8. Click "Create"
9. **Download the JSON file** and rename it to `credentials.json`

### Step 4: Place Credentials in Project

1. Copy `credentials.json` to your project root directory
2. Ensure it's in the same folder as `docker-compose.yml`

### Step 5: Test the Integration

```bash
# List available calendars
./docker-run.sh calendar-list

# Add team matches to calendar
./docker-run.sh add-team-calendar "Flamengo"

# Show setup guide
./docker-run.sh setup-calendar
```

## 🐳 Docker Commands

### Using Docker Compose Directly

```bash
# List calendars
docker-compose --profile calendar run --rm calendar-list

# Add team to calendar
docker-compose --profile calendar run --rm add-team-to-calendar

# Setup guide
docker-compose --profile calendar run --rm setup-calendar
```

### Using Make

```bash
# List calendars
make calendar-list

# Add team to calendar
make add-team-calendar TEAM='Flamengo'

# Setup guide
make setup-calendar
```

## 📁 File Structure

After setup, your project should have:

```
football-fan-ai-agent/
├── credentials.json          # Google OAuth credentials (you download this)
├── token.json               # OAuth token (created automatically)
├── docker-compose.yml       # Docker services including calendar
├── docker-run.sh            # Shell script with calendar commands
├── Makefile                 # Make targets for calendar operations
└── src/infrastructure/
    └── google_calendar.py   # Calendar integration module
```

## 🔐 Authentication Flow

1. **First Run**: Opens browser for OAuth authentication
2. **Subsequent Runs**: Uses saved token from `token.json`
3. **Token Refresh**: Automatically refreshes expired tokens

## 🎯 Available Commands

### Calendar Management

| Command | Description | Example |
|---------|-------------|---------|
| `calendar-list` | List available calendars | `./docker-run.sh calendar-list` |
| `add-team-calendar` | Add team matches to calendar | `./docker-run.sh add-team-calendar "Flamengo"` |
| `setup-calendar` | Show setup instructions | `./docker-run.sh setup-calendar` |

### Calendar Events Created

Each football match creates a calendar event with:

- **Title**: ⚽ Home Team vs Away Team
- **Description**: Competition details and team information
- **Time**: Match start time (UTC)
- **Duration**: 2 hours (configurable)
- **Reminders**: 30 minutes and 1 hour before
- **Color**: Blue (sports events)
- **Location**: Venue information (if available)

## 🚨 Troubleshooting

### Common Issues

#### 1. "Credentials file not found"

**Problem**: `credentials.json` is missing or in wrong location
**Solution**: 
```bash
# Check if file exists
ls -la credentials.json

# Download from Google Cloud Console if missing
# Place in project root directory
```

#### 2. "Authentication failed"

**Problem**: OAuth flow failed or credentials invalid
**Solution**:
```bash
# Remove old token and re-authenticate
rm token.json

# Run calendar command again
./docker-run.sh calendar-list
```

#### 3. "Calendar API not enabled"

**Problem**: Google Calendar API not enabled in project
**Solution**: Go to Google Cloud Console → APIs & Services → Library → Enable Google Calendar API

#### 4. "Permission denied"

**Problem**: OAuth consent screen not configured
**Solution**: Configure OAuth consent screen in Google Cloud Console

### Debug Commands

```bash
# Check Docker services
./docker-run.sh status

# View calendar service logs
docker-compose --profile calendar logs calendar-list

# Test calendar service directly
docker-compose --profile calendar run --rm calendar-list
```

## 🔒 Security Considerations

1. **Credentials File**: Keep `credentials.json` secure and don't commit to version control
2. **Token File**: `token.json` contains sensitive authentication data
3. **Access Scope**: Only requests calendar access, not other Google services
4. **Local Storage**: Credentials stored locally, not shared with external services

## 📚 API Limits

- **Google Calendar API**: 1,000,000 requests per day (free tier)
- **OAuth Tokens**: Valid until revoked or expired
- **Rate Limiting**: Respects Google's rate limits

## 🔄 Updating Credentials

If you need to update credentials:

1. Download new `credentials.json` from Google Cloud Console
2. Replace existing file
3. Remove `token.json` to force re-authentication
4. Run any calendar command to authenticate again

## 🎉 Success Indicators

You'll know it's working when:

- ✅ `./docker-run.sh calendar-list` shows your calendars
- ✅ `./docker-run.sh add-team-calendar "Team"` creates events
- ✅ Events appear in your Google Calendar
- ✅ No authentication errors in logs

## 📞 Getting Help

If you encounter issues:

1. Check the troubleshooting section above
2. Verify all prerequisites are met
3. Check Docker logs: `./docker-run.sh logs`
4. Ensure credentials file is in the correct location
5. Verify Google Calendar API is enabled

## 🔗 Useful Links

- [Google Cloud Console](https://console.cloud.google.com/)
- [Google Calendar API Documentation](https://developers.google.com/calendar)
- [OAuth 2.0 Setup Guide](https://developers.google.com/identity/protocols/oauth2)
- [Google Cloud Free Tier](https://cloud.google.com/free)

---

🎯 **Ready to add football matches to your calendar automatically!** ⚽
