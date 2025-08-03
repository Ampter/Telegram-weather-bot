import os
import requests
from telegram import Update, Bot
from telegram.ext import Updater, CommandHandler, CallbackContext

TELEGRAM_TOKEN = os.getenv("OPENWEATHER_API_KEY")
OPENWEATHER_API_KEY = os.getenv("OPENWEATHER_API_KEY")

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

def get_forecast(city: str):
    if not OPENWEATHER_API_KEY:
        return "OpenWeather API key is not set."
    url = f"https://api.openweathermap.org/data/2.5/forecast?q={city}&appid={OPENWEATHER_API_KEY}&units=metric"
    try:
        response = requests.get(url)
        data = response.json()
        if response.status_code != 200:
            return data.get("message", "Failed to get forecast data.")
        forecast_list = data["list"]
        days = {}
        for entry in forecast_list:
            date = entry["dt_txt"].split(" ")[0]
            if date not in days:
                days[date] = entry
            if len(days) == 3:
                break
        result = f"3-day forecast for {city.title()}:\n"
        for date, entry in days.items():
            weather = entry["weather"][0]["description"].capitalize()
            temp = entry["main"]["temp"]
            result += f"{date}: {weather}, {temp}°C\n"
        return result.strip()
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

def start(update: Update, context: CallbackContext):
    update.message.reply_text("Welcome to the Weather Bot! Use /weather <city> to get the current weather. Use /forecast <city> for a 3-day forecast.")

def main():
    updater = Updater(TELEGRAM_TOKEN, use_context=True)
    dp = updater.dispatcher
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("weather", weather_command))
    dp.add_handler(CommandHandler("forecast", forecast_command))
    updater.start_polling()
    updater.idle()

# Expose for import and testing
def test_weather(city: str) -> str:
    return get_weather(city)

def test_forecast(city: str) -> str:
    return get_forecast(city)

if __name__ == "__main__":
    main()
