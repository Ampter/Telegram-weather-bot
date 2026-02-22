# 🌤️ Telegram Weather Bot

A production-ready Telegram bot that provides real-time weather updates and 3-day forecasts using the OpenWeather API. Built with Python, `python-telegram-bot` v20 (async), and Docker.

## 🚀 Features

- **Default City:** Set your home city with `/set_city` for quick access.
- **Current Weather:** Get instant weather reports for any city or your default location.
- **3-Day Forecast:** Detailed 3-day weather outlook.
- **Inline Mode:** Get weather and forecasts in any chat by typing `@botname [city]`.
- **Healthcheck & Monitoring:** Built-in HTTP server for Uptime Robot or Render health checks.
- **Async Architecture:** High-performance asynchronous implementation using `python-telegram-bot` and `Flask`.

## 🛠️ Project Structure

```text
├── src/
│   ├── bot/          # Telegram bot logic, handlers, and health server
│   ├── weather/      # OpenWeather API client and models
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
- `@botname [city]` - Inline mode to get weather or forecast in any chat.

## 🩺 Monitoring & Healthcheck

The bot runs an internal web server to provide a healthcheck endpoint. This is essential for keeping the bot alive on platforms like Render and for external monitoring.

### Setup Uptime Robot

1. Log in to [Uptime Robot](https://uptimerobot.com/).
2. Click **Add New Monitor**.
3. **Monitor Type:** Select `HTTP(s)`.
4. **Friendly Name:** `Telegram Weather Bot`.
5. **URL (or IP):** Enter your deployed application URL followed by `/health` (e.g., `https://your-app.onrender.com/health`).
6. **Monitoring Interval:** `5 minutes` is usually sufficient.
7. Click **Create Monitor**.

### Setup on Render

1. Deploy as a **Web Service**.
2. Render will automatically provide a `PORT` environment variable (defaults to `10000` in our app to match Render).
3. Under **Settings**, set the **Health Check Path** to `/health`.
4. Ensure `TELEGRAM_TOKEN` and `OPENWEATHER_API_KEY` are added to **Environment Variables**.

## 🔐 Security & Best Practices

- **Non-root user:** The Docker image runs as a non-privileged user.
- **Secrets Management:** Environment variables are used for all sensitive data.
- **Logging:** Structured logging for better observability.
- **Async I/O:** Efficient handling of network requests and concurrent web server.
- **Type Hinting:** Extensive use of Python type hints for maintainability.

## 📄 License

MIT
