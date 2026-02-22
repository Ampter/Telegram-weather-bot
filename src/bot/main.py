import logging
import logging.handlers
import sys
import os
import threading
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
from src.config import config
from src.weather.client import WeatherClient
from src.bot.handlers import Handlers
from src.bot.web import run_flask
from src.persistence import TextFilePersistence

# Configure logging


def setup_logging():
    log_format = '%(asctime)s - %(name)s - %(levelname)s - %(filename)s:%(lineno)d - %(message)s'
    log_level = getattr(logging, config.LOG_LEVEL)

    # Ensure log directory exists
    log_dir = os.path.dirname(config.LOG_FILE)
    if log_dir and not os.path.exists(log_dir):
        os.makedirs(log_dir)

    # Root logger configuration
    root_logger = logging.getLogger()
    root_logger.setLevel(log_level)

    # Console handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(logging.Formatter(log_format))
    root_logger.addHandler(console_handler)

    # File handler (Rotating)
    file_handler = logging.handlers.RotatingFileHandler(
        config.LOG_FILE, maxBytes=5*1024*1024, backupCount=3
    )
    file_handler.setFormatter(logging.Formatter(log_format))
    root_logger.addHandler(file_handler)


setup_logging()
logger = logging.getLogger(__name__)


async def error_handler(update: object, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Log the error and send a telegram message to notify the user."""
    error_msg = f"{type(context.error).__name__}: {str(context.error)}"
    logger.error(msg=f"Exception while handling an update: {error_msg}",
                 exc_info=context.error)

    if isinstance(update, Update) and update.effective_message:
        await update.effective_message.reply_text(
            f"An unexpected error occurred: {error_msg}\nPlease try again later."
        )


def run_bot():
    try:
        config.validate()
    except ValueError as e:
        logger.error(str(e))
        sys.exit(1)

    # Ensure persistence directory exists
    persistence_dir = os.path.dirname(config.PERSISTENCE_FILE)
    if persistence_dir:
        os.makedirs(persistence_dir, exist_ok=True)
        logger.info(f"Ensured persistence directory exists: {persistence_dir}")

    # Setup Custom Text Persistence
    persistence = TextFilePersistence(filepath=config.PERSISTENCE_FILE)

    weather_client = WeatherClient(config.OPENWEATHER_API_KEY)
    handlers = Handlers(weather_client)

    application = (
        ApplicationBuilder()
        .token(config.TELEGRAM_TOKEN)
        .persistence(persistence)
        .build()
    )

    application.add_handler(CommandHandler("start", handlers.start))
    application.add_handler(CommandHandler(
        "weather", handlers.weather_command))
    application.add_handler(CommandHandler(
        "forecast", handlers.forecast_command))
    application.add_handler(CommandHandler(
        "set_city", handlers.set_city_command))
    application.add_handler(CommandHandler(
        "miniapp", handlers.miniapp_command))

    # Register the error handler
    application.add_error_handler(error_handler)

    # Setup healthcheck server (Flask) in a separate thread
    logger.info(f"Starting healthcheck server on port {config.PORT}")
    flask_thread = threading.Thread(
        target=run_flask, args=(config.PORT,), daemon=True)
    flask_thread.start()

    logger.info("Bot started and polling...")

    # run_polling() handles initialization, starting, and stopping.
    # It also handles signals like SIGINT and SIGTERM gracefully.
    application.run_polling()


if __name__ == "__main__":
    run_bot()
