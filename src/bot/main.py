import logging
import sys
import asyncio
import threading
from telegram.ext import ApplicationBuilder, CommandHandler
from src.config import config
from src.weather.client import WeatherClient
from src.miniapp.app import TelegramMiniApp
from src.bot.handlers import Handlers
from src.bot.web import run_flask

# Configure logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=getattr(logging, config.LOG_LEVEL)
)
logger = logging.getLogger(__name__)

async def run_bot():
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
    application.add_handler(CommandHandler("set_city", handlers.set_city_command))

    # Setup healthcheck server (Flask) in a separate thread
    logger.info(f"Starting healthcheck server on port {config.PORT}")
    flask_thread = threading.Thread(target=run_flask, args=(config.PORT,), daemon=True)
    flask_thread.start()

    logger.info("Bot started and polling...")

    async with application:
        await application.initialize()
        await application.start()
        await application.updater.start_polling()

        # Keep the coroutine running
        while True:
            await asyncio.sleep(3600)
