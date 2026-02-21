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
        user_id = update.effective_user.id
        logger.info(f"User {user_id} started the bot.")
        await update.message.reply_text(
            "Welcome to the Weather Bot!\n\n"
            "Commands:\n"
            "/set_city <city> - Set your default city (e.g., /set_city Kaliningrad)\n"
            "/weather [city] - Get weather for [city] or your default city\n"
            "/forecast [city] - Get 3-day forecast"
        )

    async def set_city_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Set the default city for the user."""
        user_id = update.effective_user.id
        if not context.args:
            logger.warning(f"User {user_id} used /set_city without arguments.")
            await update.message.reply_text("Usage: /set_city <city>")
            return

        city = " ".join(context.args)
        context.user_data['city'] = city
        logger.info(f"User {user_id} set city to: {city}")
        await update.message.reply_text(f"Default city set to: {city}")

    async def weather_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Fetch and send current weather."""
        user_id = update.effective_user.id
        city = " ".join(context.args) if context.args else context.user_data.get('city')

        logger.info(f"User {user_id} requested weather for city: {city}")

        if not city:
            logger.info(f"User {user_id} requested weather without city or default.")
            await update.message.reply_text("Please provide a city or set a default one with /set_city <city>")
            return

        try:
            weather = await self.weather_client.get_current_weather(city)
            if weather:
                logger.info(f"Successfully fetched weather for {city} for user {user_id}.")
                await update.message.reply_text(weather.format())
            else:
                logger.warning(f"Weather not found for {city} for user {user_id}.")
                await update.message.reply_text(f"Sorry, I couldn't find weather data for {city}.")
        except Exception as e:
            logger.error(f"Error fetching weather for {city}: {e}")
            await update.message.reply_text("An error occurred while fetching weather data.")

    async def forecast_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Fetch and send 3-day forecast."""
        user_id = update.effective_user.id
        city = " ".join(context.args) if context.args else context.user_data.get('city')

        logger.info(f"User {user_id} requested forecast for city: {city}")

        if not city:
            logger.info(f"User {user_id} requested forecast without city or default.")
            await update.message.reply_text("Please provide a city or set a default one with /set_city <city>")
            return

        try:
            forecast = await self.weather_client.get_forecast(city)
            if forecast:
                logger.info(f"Successfully fetched forecast for {city} for user {user_id}.")
                await update.message.reply_text(forecast.format())
            else:
                logger.warning(f"Forecast not found for {city} for user {user_id}.")
                await update.message.reply_text(f"Sorry, I couldn't find forecast data for {city}.")
        except Exception as e:
            logger.error(f"Error fetching forecast for {city}: {e}")
            await update.message.reply_text("An error occurred while fetching forecast data.")
