# ⚽ Football Fan AI Agent

An intelligent AI agent powered by DeepSeek API that helps football fans search for upcoming games, get team information, and chat about football.

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
- **📅 Real-time Data**: Integration with football-data.org API (optional)

## 🛠️ Installation

### Prerequisites

- Python 3.13 or higher
- DeepSeek API key
- (Optional) Football-data.org API key for real match data

### Setup

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd football-fan-ai-agent
   ```

2. **Install dependencies using uv**
   ```bash
   uv sync
   ```

3. **Set up environment variables**
   Create a `.env` file in the project root:
   ```env
   DEEPSEEK_API_KEY=your_deepseek_api_key_here
   FOOTBALL_API_KEY=your_football_api_key_here  # Optional
   ```

4. **Get API Keys**
   - **DeepSeek API**: Sign up at [DeepSeek](https://platform.deepseek.com/) to get your API key
   - **Football API** (Optional): Get a free API key from [football-data.org](https://www.football-data.org/)

## 🎯 Usage

### Run the Application

```bash
python main.py --help
```

### Available Commands

The application provides commands to interact with the Football Data API and the AI agent. Use the following commands to perform various actions:

```bash
python main.py load-database
```
This command loads database files for competitions and matches.

```bash
python main.py add-to-calendar --team <team_name>
```
This command adds matches for a specific team to your calendar.

Here is an example of the output when you run the command:
```txt
$ python main.py --help
                                                                                                                                                                                                                                    
 Usage: main.py [OPTIONS] COMMAND [ARGS]...                                                                                                                                                                                         

╭─ Options ────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ --install-completion          Install completion for the current shell.                                                                                                                                                          │
│ --show-completion             Show completion for the current shell, to copy it or customize the installation.                                                                                                                   │
│ --help                        Show this message and exit.                                                                                                                                                                        │
╰──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
╭─ Commands ───────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ load-database     Load data for a specific entity.                                                                                                                                                                               │
│ add-to-calendar   Add matches for a specific team to the calendar.                                                                                                                                                               │
│ hello             Say hello to NAME.                                                                                                                                                                                             │
╰──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
```

## 🏗️ Project Structure

```
football-fan-ai-agent/
├── db/                    # Database JSON files
│   ├── competitions.json  # Football competitions data
│   ├── matches.json       # Football matches data
├── src/
│   ├── __init__.py        # Package initialization
│   ├── agents             # AI Agents logic (e.g., DeepSeek, FootballData, Gemini, etc.)
│   ├── cron               # Jobs for periodic tasks
├── main.py                # Main application entry point
├── scheduler.py           # Scheduler for periodic tasks
├── pyproject.toml         # Project dependencies and configuration
├── .env                   # Environment variables (create this)
└── README.md              # This file
```

## 🔧 Configuration

### Environment Variables

- `DEEPSEEK_API_KEY`: Your DeepSeek API key (optional, for future use)
- `GEMINI_API_KEY`: Your Gemini API key (optional, for future use)
- `FOOTBALL_DATA_API_KEY`: Football-data.org API key (required)
- `FOOTBALL_DATA_BASE_URL`: Base URL for football-data.org API (default: `https://api.football-data.org/v4/`)

## 📊 Data Sources

### Primary Data
- **Football-data.org**: Real match data, team information, and schedules

### Fallback Data
When the football API is unavailable, the system provides realistic mock data for demonstration purposes.

## 🚨 Troubleshooting

### Common Issues

1. **"DEEPSEEK_API_KEY not found"**
   - Ensure you have created a `.env` file
   - Check that the API key is correctly set

2. **"Error generating response"**
   - Verify your DeepSeek API key is valid
   - Check your internet connection
   - Ensure you have sufficient API credits

3. **No football data showing**
   - The system will show mock data if no football API key is provided
   - Get a free API key from football-data.org for real data

### API Limits

- **DeepSeek**: Check your plan limits at the DeepSeek platform
- **Football-data.org**: Free tier includes 100 requests per day

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📝 License

This project is open source and available under the [MIT License](LICENSE).

## 🙏 Acknowledgments

- [DeepSeek](https://platform.deepseek.com/) for providing the AI capabilities
- [Football-data.org](https://www.football-data.org/) for football data APIs
- The football community for inspiration and feedback

---

⚽ **Happy Football Watching!** ⚽
