import os
import sys
import requests
from itertools import groupby
from telegram import Update, Bot
from telegram.ext import Updater, CommandHandler, CallbackContext
from mini_app import TelegramMiniApp

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
OPENWEATHER_API_KEY = os.getenv("OPENWEATHER_API_KEY")

# Instantiate the mini app
mini_app = TelegramMiniApp()

def get_weather(city: str):
    if not OPENWEATHER_API_KEY:
        return "OpenWeather API key is not set."
    url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={OPENWEATHER_API_KEY}&units=metric"
    try:
        response = requests.get(url)
        data = response.json()
        if response.status_code != 200:
            return data.get("message", "Failed to get weather data.")
        weather = data["weather"][0]["description"].capitalize()
        temp = data["main"]["temp"]
        feels_like = data["main"]["feels_like"]
        return f"Weather in {city.title()}: {weather}\nTemperature: {temp}°C (feels like {feels_like}°C)"
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
    url = f"https://api.openweathermap.org/data/2.5/forecast?q={city}&appid={OPENWEATHER_API_KEY}&units=metric"
    try:
        response = requests.get(url)
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
    if not context.args:
        update.message.reply_text(mini_app.render_ui())
        return
    action = context.args[0]
    if action == 'set_location':
        if len(context.args) < 2:
            update.message.reply_text("Usage: /miniapp set_location <city>")
            return
        location = " ".join(context.args[1:])
        result = mini_app.set_location(location)
        update.message.reply_text(result)
    elif action == 'fetch_weather':
        result = mini_app.fetch_weather()
        update.message.reply_text(result)
    else:
        update.message.reply_text(mini_app.render_ui())

def start(update: Update, context: CallbackContext):
    update.message.reply_text("Welcome to the Weather Bot! Use /weather <city> to get the current weather. Use /forecast <city> for a 3-day forecast. Use /miniapp for the mini app interface.")

def main():
    if not TELEGRAM_TOKEN:
        print("Error: TELEGRAM_TOKEN is not set. Please set the TELEGRAM_TOKEN environment variable or configuration value before running the bot.", file=sys.stderr)
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
