# 🌤️ Telegram Weather Bot

A production-ready Telegram bot that provides real-time weather updates and 3-day forecasts using the OpenWeather API. Built with Python, `python-telegram-bot` v20 (async), and Docker.

## 🚀 Features

- **Default City:** Set your home city with `/set_city` for quick access.
- **Current Weather:** Get instant weather reports for any city or your default location.
- **3-Day Forecast:** Detailed 3-day weather outlook.
- **Mini App Interface:** A simulation of a Telegram Mini App that defaults to your set city.
- **Healthcheck & Monitoring:** Built-in HTTP server for Uptime Robot or Render health checks.
- **Async Architecture:** High-performance asynchronous implementation using `python-telegram-bot` and `aiohttp`.

## 🛠️ Project Structure

```text
├── src/
│   ├── bot/          # Telegram bot logic, handlers, and health server
│   ├── weather/      # OpenWeather API client and models
│   ├── miniapp/      # Mini app business logic and user preferences
│   └── config.py     # Configuration and environment management
├── tests/            # Test suite
├── Dockerfile        # Multi-stage production Docker image
├── docker-compose.yml# Docker orchestration
└── bot.py            # Application entry point
```

## 📋 Prerequisites

- Python 3.10+
- A Telegram Bot Token (from [@BotFather](https://t.me/botfather))
- An OpenWeather API Key (from [openweathermap.org](https://openweathermap.org/appid))

## ⚙️ Setup & Installation

### Local Development

1. **Clone the repository:**
   ```bash
   git clone <repository-url>
   cd telegram-weather-bot
   ```

2. **Setup Environment:**
   ```bash
   # Create a virtual environment and activate it
   # Install dependencies
   pip install -r requirements.txt
   pip install -r requirements-dev.txt
   ```

3. **Configure environment variables:**
   Create a `.env` file from the example:
   ```bash
   cp .env.example .env
   ```
   Edit `.env` and add your tokens.

4. **Run the bot:**
   ```bash
   python bot.py
   ```

### Running with Docker

1. **Build and start the container:**
   ```bash
   docker-compose up -d --build
   ```

2. **Check logs:**
   ```bash
   docker-compose logs -f
   ```

## 🧪 Testing

The project uses `pytest` with `pytest-asyncio`.

Run tests:
```bash
export PYTHONPATH=$PYTHONPATH:$(pwd)
pytest
```

## 🤖 Usage

Once the bot is running, send the following commands:

- `/start` - Welcome message and instructions.
- `/set_city <city>` - Set your default city (e.g., `/set_city Kaliningrad`).
- `/weather [city]` - Get current weather. If no city is provided, uses your default city.
- `/forecast [city]` - Get 3-day forecast.
- `/miniapp` - Open the mini app interface (defaults to your set city).

## 🩺 Monitoring & Healthcheck

The bot runs an internal web server on port `8000` (configurable via `PORT` env var).

- **Healthcheck URL:** `http://<your-app-url>/health`
- **Uptime Robot:** Point Uptime Robot to this URL to monitor the bot's availability.

## 🔐 Security & Best Practices

- **Non-root user:** The Docker image runs as a non-privileged user.
- **Secrets Management:** Environment variables are used for all sensitive data.
- **Logging:** Structured logging for better observability.
- **Async I/O:** Efficient handling of network requests and concurrent web server.
- **Type Hinting:** Extensive use of Python type hints for maintainability.

## 📄 License

MIT
