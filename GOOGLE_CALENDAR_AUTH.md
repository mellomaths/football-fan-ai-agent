# 🔐 Google Calendar Authentication Methods

The Football Fan AI Agent supports multiple authentication methods for Google Calendar integration. Choose the one that best fits your use case.

## 🎯 **Authentication Methods Overview**

| Method | Browser Required | Write Access | Setup Complexity | Best For |
|--------|------------------|--------------|------------------|----------|
| **OAuth 2.0** | ✅ Yes | ✅ Full | 🟡 Medium | Personal use, development |
| **Service Account** | ❌ No | ✅ Full | 🟢 Easy | Production, automation |
| **Application Default Credentials** | ❌ No | ✅ Full | 🟢 Easy | GCP environments, gcloud CLI |
| **API Key** | ❌ No | ❌ Read-only | 🟢 Easy | Read-only operations |

## 🔑 **Method 1: OAuth 2.0 (Interactive)**

**Best for**: Personal use, development, testing

### Setup Steps

1. **Go to Google Cloud Console**
   - Visit [console.cloud.google.com](https://console.cloud.google.com/)
   - Create or select a project

2. **Enable Google Calendar API**
   - Go to "APIs & Services" → "Library"
   - Search for "Google Calendar API"
   - Click "Enable"

3. **Create OAuth 2.0 Credentials**
   - Go to "APIs & Services" → "Credentials"
   - Click "Create Credentials" → "OAuth 2.0 Client IDs"
   - Configure OAuth consent screen if prompted
   - Application type: "Desktop application"
   - Download as `credentials.json`

4. **Configure Environment**
   ```env
   GOOGLE_CALENDAR_CREDENTIALS_PATH=credentials.json
   GOOGLE_CALENDAR_TOKEN_PATH=token.json
   ```

5. **First Run**
   - Run any calendar command
   - Browser will open for authentication
   - Grant calendar access permissions
   - Token will be saved automatically

### Pros & Cons
- ✅ **Full calendar access** (read/write)
- ✅ **User-specific permissions**
- ❌ **Requires browser interaction** (first time only)
- ❌ **Token expires** (but auto-refreshes)

---

## 🤖 **Method 2: Service Account (Automated)**

**Best for**: Production, automation, servers, containers

### Setup Steps

1. **Create Service Account**
   - Go to "IAM & Admin" → "Service Accounts"
   - Click "Create Service Account"
   - Name: "football-calendar-bot"
   - Description: "Automated football match calendar updates"

2. **Grant Calendar Permissions**
   - Click on the service account
   - Go to "Permissions" tab
   - Click "Grant Access"
   - Add role: "Calendar API Admin" or "Calendar API User"

3. **Create and Download Key**
   - Go to "Keys" tab
   - Click "Add Key" → "Create new key"
   - Choose "JSON"
   - Download the key file

4. **Configure Environment**
   ```env
   GOOGLE_CALENDAR_SERVICE_ACCOUNT_PATH=service-account-key.json
   ```

5. **Share Calendar with Service Account**
   - In Google Calendar, go to calendar settings
   - Under "Share with specific people"
   - Add the service account email
   - Grant "Make changes to events" permission

### Pros & Cons
- ✅ **No browser interaction** - fully automated
- ✅ **Never expires** - permanent access
- ✅ **Perfect for production** and containers
- ❌ **Requires calendar sharing** setup
- ❌ **More complex initial setup**

---

## ☁️ **Method 3: Application Default Credentials (ADC)**

**Best for**: GCP environments, gcloud CLI users, development

### Setup Steps

1. **Install Google Cloud CLI**
   ```bash
   # macOS
   brew install google-cloud-sdk
   
   # Windows
   # Download from https://cloud.google.com/sdk/docs/install
   
   # Linux
   curl https://sdk.cloud.google.com | bash
   exec -l $SHELL
   ```

2. **Authenticate with gcloud**
   ```bash
   gcloud auth login
   gcloud config set project YOUR_PROJECT_ID
   gcloud auth application-default login
   ```

3. **Configure Environment**
   ```env
   GOOGLE_CALENDAR_USE_ADC=true
   ```

4. **Verify Setup**
   ```bash
   gcloud auth application-default print-access-token
   ```

### Pros & Cons
- ✅ **No files needed** - uses system credentials
- ✅ **Automatic credential management**
- ✅ **Perfect for GCP environments**
- ❌ **Requires gcloud CLI installation**
- ❌ **User must be logged in**

---

## 🔑 **Method 4: API Key (Read-Only)**

**Best for**: Read-only operations, simple testing

### Setup Steps

1. **Create API Key**
   - Go to "APIs & Services" → "Credentials"
   - Click "Create Credentials" → "API Key"
   - Copy the generated key

2. **Configure Environment**
   ```env
   GOOGLE_CALENDAR_API_KEY=your_api_key_here
   ```

3. **Restrict API Key** (Recommended)
   - Click on the API key
   - Under "Application restrictions": "HTTP referrers"
   - Under "API restrictions": "Restrict key" → "Google Calendar API"

### Pros & Cons
- ✅ **Simplest setup** - just one key
- ✅ **No browser interaction**
- ❌ **Read-only access** - cannot create/modify events
- ❌ **Limited functionality**

---

## 🐳 **Docker Configuration**

### Volume Mounts for Different Methods

#### OAuth 2.0
```yaml
volumes:
  - ./credentials.json:/app/credentials.json:ro
  - ./token.json:/app/token.json
```

#### Service Account
```yaml
volumes:
  - ./service-account-key.json:/app/service-account-key.json:ro
```

#### Application Default Credentials
```yaml
volumes:
  - ~/.config/gcloud:/root/.config/gcloud:ro
```

#### API Key
```yaml
# No volume mounts needed - uses environment variable
```

### Environment Variables in Docker

```yaml
environment:
  - GOOGLE_CALENDAR_CREDENTIALS_PATH=/app/credentials.json
  - GOOGLE_CALENDAR_SERVICE_ACCOUNT_PATH=/app/service-account-key.json
  - GOOGLE_CALENDAR_USE_ADC=true
  - GOOGLE_CALENDAR_API_KEY=${GOOGLE_CALENDAR_API_KEY}
```

---

## 🔄 **Switching Between Methods**

### Method Priority
The system tries authentication methods in this order:
1. **Application Default Credentials** (if `GOOGLE_CALENDAR_USE_ADC=true`)
2. **Service Account** (if `GOOGLE_CALENDAR_SERVICE_ACCOUNT_PATH` is set)
3. **OAuth 2.0** (if `GOOGLE_CALENDAR_CREDENTIALS_PATH` is set)
4. **API Key** (if `GOOGLE_CALENDAR_API_KEY` is set)

### Switching Example
```bash
# Start with OAuth 2.0
GOOGLE_CALENDAR_CREDENTIALS_PATH=credentials.json

# Switch to Service Account
unset GOOGLE_CALENDAR_CREDENTIALS_PATH
GOOGLE_CALENDAR_SERVICE_ACCOUNT_PATH=service-account.json

# Switch to ADC
unset GOOGLE_CALENDAR_SERVICE_ACCOUNT_PATH
GOOGLE_CALENDAR_USE_ADC=true

# Switch to API Key
unset GOOGLE_CALENDAR_USE_ADC
GOOGLE_CALENDAR_API_KEY=your_key
```

---

## 🚨 **Troubleshooting**

### Common Issues

#### "No authentication method specified"
**Solution**: Set at least one authentication method in your `.env` file

#### "Service account authentication failed"
**Solution**: 
- Verify the service account key file exists
- Check that the service account has calendar permissions
- Ensure the calendar is shared with the service account email

#### "ADC authentication failed"
**Solution**:
- Run `gcloud auth application-default login`
- Verify `gcloud config get-value project` shows correct project
- Check that Google Calendar API is enabled

#### "API key authentication failed"
**Solution**:
- Verify the API key is correct
- Check that Google Calendar API is enabled
- Ensure API key restrictions allow Calendar API access

### Debug Commands

```bash
# Check authentication status
./docker-run.sh calendar-list

# View detailed logs
./docker-run.sh logs

# Test specific authentication method
docker-compose --profile calendar run --rm calendar-list
```

---

## 🎯 **Recommendations by Use Case**

### **Development & Testing**
- **OAuth 2.0** - Easy setup, full access, interactive

### **Production & Automation**
- **Service Account** - No user interaction, permanent access

### **GCP Environments**
- **Application Default Credentials** - Seamless integration

### **Read-Only Operations**
- **API Key** - Simple, lightweight

### **Docker Containers**
- **Service Account** - No volume mounts for credentials, secure

---

## 🔒 **Security Best Practices**

1. **Never commit credentials** to version control
2. **Use environment variables** for sensitive data
3. **Restrict API keys** to specific APIs and referrers
4. **Grant minimal permissions** to service accounts
5. **Rotate credentials** regularly in production
6. **Use IAM roles** instead of broad permissions

---

## 📚 **Additional Resources**

- [Google Cloud Console](https://console.cloud.google.com/)
- [Google Calendar API Documentation](https://developers.google.com/calendar)
- [Service Account Best Practices](https://cloud.google.com/iam/docs/best-practices-for-managing-service-account-keys)
- [Application Default Credentials](https://cloud.google.com/docs/authentication/provide-credentials-adc)
- [API Key Security](https://cloud.google.com/docs/authentication/api-keys)

---

🎯 **Choose the authentication method that best fits your needs and security requirements!** 🔐
