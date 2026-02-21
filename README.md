# 🌤️ Telegram Weather Bot

A production-ready Telegram bot that provides real-time weather updates and 3-day forecasts using the OpenWeather API. Built with Python, `python-telegram-bot` v20 (async), and Docker.

## 🚀 Features

- **Current Weather:** Get instant weather reports for any city.
- **3-Day Forecast:** Detailed 3-day weather outlook.
- **Mini App Interface:** A simulation of a Telegram Mini App for easy weather tracking.
- **Async Architecture:** High-performance asynchronous implementation.
- **Production Ready:** Fully containerized with Docker and Docker Compose.
- **High Test Coverage:** Comprehensive unit and integration tests.

## 🛠️ Project Structure

```text
├── src/
│   ├── bot/          # Telegram bot logic and handlers
│   ├── weather/      # OpenWeather API client and models
│   ├── miniapp/      # Mini app business logic
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

4. **Configure environment variables:**
   Create a `.env` file from the example:
   ```bash
   cp .env.example .env
   ```
   Edit `.env` and add your tokens.

5. **Run the bot:**
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
- `/weather <city>` - Get current weather (e.g., `/weather London`).
- `/forecast <city>` - Get 3-day forecast (e.g., `/forecast Tokyo`).
- `/miniapp` - Open the mini app interface simulation.

## 🔐 Security & Best Practices

- **Non-root user:** The Docker image runs as a non-privileged user.
- **Secrets Management:** Environment variables are used for all sensitive data.
- **Logging:** Structured logging for better observability.
- **Async I/O:** Efficient handling of network requests.
- **Type Hinting:** Extensive use of Python type hints for maintainability.

## 📄 License

MIT
