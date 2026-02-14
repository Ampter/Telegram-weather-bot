# Telegram Weather Bot

A Telegram bot that provides current weather and a 3-day forecast for any city using the OpenWeather API.

## Features

- `/weather <city>` for current weather
- `/forecast <city>` for 3-day forecast
- `/miniapp` command for a simple mini app style interface

## Requirements

- Python 3.10+
- Telegram bot token from [BotFather](https://t.me/botfather)
- OpenWeather API key from [openweathermap.org](https://openweathermap.org/appid)

## Local setup

1. Clone this repository.
2. Install dependencies:

```bash
pip install -r requirements.txt
```

3. Set environment variables:

```bash
export TELEGRAM_TOKEN=your_telegram_bot_token
export OPENWEATHER_API_KEY=your_openweather_api_key
```

> The app also supports `TELEGRAM_BOT_TOKEN` as a fallback alias for `TELEGRAM_TOKEN`.

4. Run:

```bash
python bot.py
```

## Usage

- `/start`
- `/weather London`
- `/forecast Tokyo`
- `/miniapp`

## Docker

Build image:

```bash
docker build -t telegram-weather-bot .
```

Run container:

```bash
docker run --rm \
  -e TELEGRAM_TOKEN=your_telegram_bot_token \
  -e OPENWEATHER_API_KEY=your_openweather_api_key \
  telegram-weather-bot
```

## Testing

Run tests locally:

```bash
pytest -q
```

A GitHub Actions workflow is included at `.github/workflows/tests.yml` and runs tests on pushes and pull requests.
