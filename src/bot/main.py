import logging
import sys
import asyncio
from aiohttp import web
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

async def health_check(request):
    return web.Response(text="OK", status=200)

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

    # Setup healthcheck server
    app = web.Application()
    app.router.add_get('/health', health_check)
    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner, '0.0.0.0', config.PORT)

    logger.info(f"Starting healthcheck server on port {config.PORT}")
    await site.start()

    logger.info("Bot started and polling...")

    async with application:
        await application.initialize()
        await application.start()
        await application.updater.start_polling()

        # Keep the coroutine running
        while True:
            await asyncio.sleep(3600)
