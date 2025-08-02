import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
import requests
import os

# Set up logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN', 'YOUR_TELEGRAM_BOT_TOKEN')  # Replace with your bot token or set as env var
OPENWEATHER_API_KEY = os.getenv('OPENWEATHER_API_KEY', 'YOUR_OPENWEATHER_API_KEY')  # Replace with your API key or set as env var

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text('Hello! I am your weather bot. Use /weather <city> to get the current weather.')

async def weather(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        await update.message.reply_text('Please provide a city name. Usage: /weather <city>')
        return
    city = ' '.join(context.args)
    url = f'http://api.openweathermap.org/data/2.5/weather?q={city}&appid={OPENWEATHER_API_KEY}&units=metric'
    try:
        response = requests.get(url)
        data = response.json()
        if data.get('cod') != 200:
            await update.message.reply_text(f"Could not find weather for '{city}'. Please check the city name.")
            return
        weather_desc = data['weather'][0]['description']
        temp = data['main']['temp']
        await update.message.reply_text(f"Weather in {city}: {weather_desc}, {temp}°C")
    except Exception as e:
        logger.error(f"Error fetching weather: {e}")
        await update.message.reply_text('Sorry, there was an error fetching the weather.')

def main():
    app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()
    app.add_handler(CommandHandler('start', start))
    app.add_handler(CommandHandler('weather', weather))
    logger.info('Bot started...')
    app.run_polling()

if __name__ == '__main__':
    main()
