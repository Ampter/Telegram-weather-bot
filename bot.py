import os
import requests
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN', 'YOUR_TELEGRAM_BOT_TOKEN')
OPENWEATHER_API_KEY = os.getenv('OPENWEATHER_API_KEY', 'YOUR_OPENWEATHER_API_KEY')

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text('Hello! I am your weather bot. Use /weather <city> to get the current weather.')

def get_weather(city: str):
    url = f'https://api.openweathermap.org/data/2.5/weather?q={city}&appid={OPENWEATHER_API_KEY}&units=metric'
    try:
        response = requests.get(url)
        data = response.json()
        if data.get('cod') != 200:
            return f"Could not find weather for '{city}'."
        weather = data['weather'][0]['description']
        temp = data['main']['temp']
        return f"Weather in {city}: {weather}, {temp}°C"
    except Exception as e:
        return f"Error fetching weather: {e}"

async def weather(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        await update.message.reply_text('Please provide a city name. Usage: /weather <city>')
        return
    city = ' '.join(context.args)
    weather_info = get_weather(city)
    await update.message.reply_text(weather_info)

if __name__ == '__main__':
    app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()
    app.add_handler(CommandHandler('start', start))
    app.add_handler(CommandHandler('weather', weather))
    print('Bot is running...')
    app.run_polling()