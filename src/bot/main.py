import logging
import sys
from telegram.ext import ApplicationBuilder, CommandHandler
from src.config import config
from src.weather.client import WeatherClient
from src.miniapp.app import TelegramMiniApp
from src.bot.handlers import Handlers

# Configure logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=getattr(logging, config.LOG_LEVEL)
)
logger = logging.getLogger(__name__)

def run_bot():
    try:
        config.validate()
    except ValueError as e:
        logger.error(str(e))
        sys.exit(1)

    weather_client = WeatherClient(config.OPENWEATHER_API_KEY)
    mini_app = TelegramMiniApp(weather_client)
    handlers = Handlers(weather_client, mini_app)

    application = ApplicationBuilder().token(config.TELEGRAM_TOKEN).build()

    application.add_handler(CommandHandler("start", handlers.start))
    application.add_handler(CommandHandler("weather", handlers.weather_command))
    application.add_handler(CommandHandler("forecast", handlers.forecast_command))
    application.add_handler(CommandHandler("miniapp", handlers.miniapp_command))

    logger.info("Bot started and polling...")
    application.run_polling()

if __name__ == "__main__":
    run_bot()
