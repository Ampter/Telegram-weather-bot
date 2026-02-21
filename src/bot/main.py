import logging
import sys
import os
import threading
from telegram.ext import ApplicationBuilder, CommandHandler
from src.config import config
from src.weather.client import WeatherClient
from src.bot.handlers import Handlers
from src.bot.web import run_flask
from src.persistence import TextFilePersistence

# Configure logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=getattr(logging, config.LOG_LEVEL)
)
logger = logging.getLogger(__name__)

def run_bot():
    logger.info("Initializing bot...")
    try:
        config.validate()
        logger.info("Configuration validated.")
    except ValueError as e:
        logger.error(f"Configuration error: {e}")
        sys.exit(1)

    # Ensure persistence directory exists
    persistence_dir = os.path.dirname(config.PERSISTENCE_FILE)
    if persistence_dir and not os.path.exists(persistence_dir):
        os.makedirs(persistence_dir, exist_ok=True)
        logger.info(f"Created persistence directory: {persistence_dir}")

    # Setup Custom Text Persistence
    logger.info(f"Loading persistence from {config.PERSISTENCE_FILE}")
    persistence = TextFilePersistence(filepath=config.PERSISTENCE_FILE)

    weather_client = WeatherClient(config.OPENWEATHER_API_KEY)
    handlers = Handlers(weather_client)

    logger.info("Building application...")
    application = (
        ApplicationBuilder()
        .token(config.TELEGRAM_TOKEN)
        .persistence(persistence)
        .build()
    )

    application.add_handler(CommandHandler("start", handlers.start))
    application.add_handler(CommandHandler("weather", handlers.weather_command))
    application.add_handler(CommandHandler("forecast", handlers.forecast_command))
    application.add_handler(CommandHandler("set_city", handlers.set_city_command))

    # Setup healthcheck server (Flask) in a separate thread
    logger.info(f"Starting healthcheck server on port {config.PORT}")
    flask_thread = threading.Thread(target=run_flask, args=(config.PORT,), daemon=True)
    flask_thread.start()

    logger.info("Bot started and polling...")
    application.run_polling()

if __name__ == "__main__":
    run_bot()
