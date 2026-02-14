import os
import sys
from itertools import groupby

try:
    import requests
except ImportError:  # pragma: no cover - dependency unavailable in some CI sandboxes
    class _RequestsFallback:
        @staticmethod
        def get(*args, **kwargs):
            raise RuntimeError("requests is required to fetch weather data")

    requests = _RequestsFallback()

try:
    from telegram import Update
    from telegram.ext import CallbackContext, CommandHandler, Updater
except ImportError:  # pragma: no cover - dependency unavailable during offline tests
    class Update:  # minimal fallback typing shim
        pass

    class CallbackContext:
        pass

    class CommandHandler:
        def __init__(self, *args, **kwargs):
            pass

    class Updater:
        def __init__(self, *args, **kwargs):
            raise RuntimeError("python-telegram-bot is required to run the bot")

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN") or os.getenv("TELEGRAM_BOT_TOKEN")
OPENWEATHER_API_KEY = os.getenv("OPENWEATHER_API_KEY")

# Instantiate the mini app inside the function to avoid circular import
mini_app = None


def get_weather(city: str):
    if not OPENWEATHER_API_KEY:
        return "OpenWeather API key is not set."
    url = (
        "https://api.openweathermap.org/data/2.5/weather"
        f"?q={city}&appid={OPENWEATHER_API_KEY}&units=metric"
    )
    try:
        response = requests.get(url, timeout=10)
        data = response.json()
        if response.status_code != 200:
            return data.get("message", "Failed to get weather data.")
        weather = data["weather"][0]["description"].capitalize()
        temp = data["main"]["temp"]
        feels_like = data["main"]["feels_like"]
        return (
            f"Weather in {city.title()}: {weather}\n"
            f"Temperature: {temp}°C (feels like {feels_like}°C)"
        )
    except Exception as e:
        return f"Error fetching weather: {e}"


def _pick_daily_entries(forecast_list, days=3):
    key = lambda e: e["dt_txt"].split()[0]
    grouped = groupby(forecast_list, key)
    return [next(group) for _, group in grouped][:days]


def _format_daily(entry):
    date = entry["dt_txt"].split()[0]
    desc = entry["weather"][0]["description"].capitalize()
    temp = entry["main"]["temp"]
    return f"{date}: {desc}, {temp}°C"


def get_forecast(city: str):
    if not OPENWEATHER_API_KEY:
        return "OpenWeather API key is not set."
    url = (
        "https://api.openweathermap.org/data/2.5/forecast"
        f"?q={city}&appid={OPENWEATHER_API_KEY}&units=metric"
    )
    try:
        response = requests.get(url, timeout=10)
        data = response.json()
        if response.status_code != 200:
            return data.get("message", "Failed to get forecast data.")
        forecast_list = data.get("list")
        if not isinstance(forecast_list, list):
            return "Malformed forecast data received from API."
        entries = _pick_daily_entries(forecast_list)
        lines = [_format_daily(e) for e in entries]
        header = f"3-day forecast for {city.title()}:\n"
        return header + "\n".join(lines)
    except Exception as e:
        return f"Error fetching forecast: {e}"


def weather_command(update: Update, context: CallbackContext):
    if not context.args:
        update.message.reply_text("Usage: /weather <city>")
        return
    city = " ".join(context.args)
    result = get_weather(city)
    update.message.reply_text(result)


def forecast_command(update: Update, context: CallbackContext):
    if not context.args:
        update.message.reply_text("Usage: /forecast <city>")
        return
    city = " ".join(context.args)
    result = get_forecast(city)
    update.message.reply_text(result)


def miniapp_command(update: Update, context: CallbackContext):
    global mini_app
    if mini_app is None:
        from mini_app import TelegramMiniApp

        mini_app = TelegramMiniApp()
    if not context.args:
        update.message.reply_text(mini_app.render_ui())
        return
    action = context.args[0]
    if action == "set_location":
        if len(context.args) < 2:
            update.message.reply_text("Usage: /miniapp set_location <city>")
            return
        location = " ".join(context.args[1:])
        result = mini_app.set_location(location)
        update.message.reply_text(result)
    elif action == "fetch_weather":
        result = mini_app.fetch_weather()
        update.message.reply_text(result)
    else:
        update.message.reply_text(mini_app.render_ui())


def start(update: Update, context: CallbackContext):
    update.message.reply_text(
        "Welcome to the Weather Bot! Use /weather <city> to get the current weather. "
        "Use /forecast <city> for a 3-day forecast. Use /miniapp for the mini app interface."
    )


def main():
    if not TELEGRAM_TOKEN:
        print(
            "Error: TELEGRAM_TOKEN (or TELEGRAM_BOT_TOKEN) is not set. "
            "Please set one of these environment variables before running the bot.",
            file=sys.stderr,
        )
        sys.exit(1)
    updater = Updater(TELEGRAM_TOKEN, use_context=True)
    dp = updater.dispatcher
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("weather", weather_command))
    dp.add_handler(CommandHandler("forecast", forecast_command))
    dp.add_handler(CommandHandler("miniapp", miniapp_command))
    updater.start_polling()
    updater.idle()


def test_weather(city: str) -> str:
    return get_weather(city)


def test_forecast(city: str) -> str:
    return get_forecast(city)


if __name__ == "__main__":
    main()
