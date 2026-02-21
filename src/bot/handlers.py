import logging
from telegram import Update
from telegram.ext import ContextTypes
from src.weather.client import WeatherClient

logger = logging.getLogger(__name__)


class Handlers:
    """Class containing all Telegram command handlers."""

    def __init__(self, weather_client: WeatherClient):
        self.weather_client = weather_client

    async def start(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Send a message when the command /start is issued."""
        logger.info(f"User {update.effective_user.id} triggered /start")
        await update.message.reply_text(
            "Welcome to the Weather Bot!\n\n"
            "Commands:\n"
            "/set_city <city> - Set your default city (e.g., /set_city Kaliningrad)\n"
            "/weather [city] - Get weather for [city] or your default city\n"
            "/forecast [city] - Get 3-day forecast"
        )

    async def set_city_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Set the default city for the user."""
        logger.info(f"User {update.effective_user.id} triggered /set_city")
        if not context.args:
            await update.message.reply_text("Usage: /set_city <city>")
            return

        city = " ".join(context.args)
        context.user_data['city'] = city
        await update.message.reply_text(f"Default city set to: {city}")

    async def weather_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Fetch and send current weather."""
        logger.info(f"User {update.effective_user.id} triggered /weather")
        city = " ".join(
            context.args) if context.args else context.user_data.get('city')

        if not city:
            await update.message.reply_text("Please provide a city or set a default one with /set_city <city>")
            return

        weather = await self.weather_client.get_current_weather(city)
        if weather:
            await update.message.reply_text(weather.format())
        else:
            await update.message.reply_text(f"Sorry, I couldn't find weather data for {city}.")

    async def forecast_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Fetch and send 3-day forecast."""
        logger.info(f"User {update.effective_user.id} triggered /forecast")
        city = " ".join(
            context.args) if context.args else context.user_data.get('city')

        if not city:
            await update.message.reply_text("Please provide a city or set a default one with /set_city <city>")
            return

        forecast = await self.weather_client.get_forecast(city)
        if forecast:
            await update.message.reply_text(forecast.format())
        else:
            await update.message.reply_text(f"Sorry, I couldn't find forecast data for {city}.")
